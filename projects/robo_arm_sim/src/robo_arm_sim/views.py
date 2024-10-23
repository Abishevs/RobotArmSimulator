import logging
import json
from typing import Dict, List, Optional

from PySide6.QtWidgets import ( QHBoxLayout, QLabel, QMainWindow, QPushButton, QWidget, QVBoxLayout)
from PySide6.QtGui import (QColor, QVector3D)
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6 import QtGui
from PySide6.QtCore import QTimer, Signal, Slot
from PySide6.QtGui import QColor, QVector3D
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtWebSockets import QWebSocket, QWebSocketProtocol
from commonlib.enums import Identifier, MessageType
from robo_arm_sim.constants import THETA_UNICODE

from robo_arm_sim.entities import ArmSegment, BasePlate, EndEffector
from robo_arm_sim.robotic_arm import RoboticArm
from robo_arm_sim.ui.ui_angle_controll_widget import Ui_SegmentControllWidget
from robo_arm_sim.ui.ui_mainwindow import Ui_MainWindow
from commonlib.json_schema import validate_message

# Init logger
logger = logging.getLogger(__name__)


class WebSocketClient(QWidget):
    on_recieved_command = Signal(str)

    def __init__(self, robot_arm, host: str = "ws://localhost:8000", ):
        super().__init__()
        self.host = host
        self.websocket = QWebSocket()
        self.websocket.connected.connect(self.on_connected)
        self.websocket.disconnected.connect(self.on_disconnected)
        self.websocket.textMessageReceived.connect(self.on_text_message_received)
        self.websocket.errorOccurred.connect(self.on_error)

        self.robotic_arm: RoboticArm = robot_arm
        self.identifier: Identifier = Identifier.GUI

        self.host_text = QLabel(f"Server IP: '{self.host}'")

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.host_text)
        self.main_layout.addWidget(self.connect_button)

    @Slot(int, int)
    def send_position_update(self, index, angle):
        positions = self.robotic_arm.get_current_positions()
        data = {
                "messageType": MessageType.POSITIONUPDATE.value,
                "identifier": self.identifier.value,
                "payload": positions
                }

        try:
            validate_message(data)
        except Exception as e:
            logger.error(e)

        else:
            self.send_data(data)

    def send_data(self, data: Dict):
        if self.websocket.isValid():
            self.websocket.sendTextMessage(json.dumps(data))

    @Slot(QWebSocketProtocol.CloseCode)
    def on_error(self, error_code):
        logger.error(f"Error code: {error_code}")

    def toggle_connection(self):
        if not self.websocket.isValid():
            self.websocket.open(self.host)
            self.connect_button.setText("Connecting...")
        else:
            self.websocket.close()
            
    def connect_to_server(self):
        self.websocket.open(self.host)
        data = {
                "identifier": self.identifier.value
                }
        self.send_data(data)

    def disconnect_from_server(self):
        self.websocket.disconnect(self.websocket)
        
    @Slot()
    def on_connected(self):
        logger.info("Connected to server")
        data =  {
                "messageType": "positionUpdate",
                "identifier": self.identifier.value,
                }

        try:
            validate_message(data)
        except Exception as e:
            logger.error(e)
        else:
            self.send_data(data)
            self.connect_button.setText("Disconnect")
        
    @Slot()
    def on_disconnected(self):
        logger.info("Disconnected from server")
        self.connect_button.setText("Connect")
        self.identifier = Identifier.GUI
        
    @Slot(str)
    def on_text_message_received(self, message):
        logger.info(f"Message from server: {message}")
        self.on_recieved_command.emit(message)
        data = json.loads(message)
        try:
            validate_message(data)
        except Exception as e:
            logger.error(e)
        else:
            # Validated thus safe to assign
            # identifier = data.get("identifier")
            positions = data.get("payload", {}).get("positions", [])
            logger.debug(f"Postions to update: {positions}")
            try:
                # if identifier  and identifier != self.identifier.value:
                #     self.identifier = Identifier(data["identifier"])
                if positions:
                    for pos in positions:
                        index = pos.get("jointId", 0) - 1 
                        logger.debug(index)
                        new_angle = pos.get("currentAngle", 0)
                        logger.debug(index)
                        if 0 <= index < len(self.robotic_arm.segments):
                            self.robotic_arm.update_angle(index, float(new_angle))
                            logger.debug(f"new_angle: {self.robotic_arm.get_seg(index).theta}")
                        else:
                            logger.warning(f"Invalid jointId: {index + 1}")

            except Exception as e:
                logger.error(e)


class SimWindow(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super().__init__()
        self.rootEntity = Qt3DCore.QEntity()
        self.defaultFrameGraph().setClearColor(QtGui.QColor("black"))
        self.robot_arm = RoboticArm() 
        self.setup_models()
        logger.debug("Initilised SimWinodw")
        # self.setup_scene()

    def get_robot_arm(self):
        return self.robot_arm

    def setup_scene(self):
        # Camera setup
        self.camera().lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 100.0)
        self.camera().setPosition(QtGui.QVector3D(-40, 25, -50))
        self.camera().setViewCenter(QtGui.QVector3D(0, 0, 0))

        # Setup models
        # self.setup_models() 
        self.setupGroundPlane()

        # Camera controller
        self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        self.camController.setCamera(self.camera())

        # light source
        self.lightEntity = Qt3DCore.QEntity(self.rootEntity)
        self.light = Qt3DRender.QDirectionalLight(self.lightEntity)
        self.light.setColor("white")
        self.light.setIntensity(1.5)  # Adjust intensity as needed
        self.light.setWorldDirection(QVector3D(1, -1, 1))  # Adjust direction as needed
        self.lightEntity.addComponent(self.light)

        self.setRootEntity(self.rootEntity)
        # self.robot_arm.animate()


    def setup_models(self):
        base = BasePlate(self.rootEntity)
        self.robot_arm.add_base(base)
        self.robot_arm.add_segment(ArmSegment(self.rootEntity,
                                              name = "Segment1",
                                              color = "yellow",
                                              length = 50,
                                              theta = 0,
                                              jointP = QVector3D(0, 0, 0),
                                              ))
        self.robot_arm.add_segment(ArmSegment(self.rootEntity,
                                              name = "Segment2",
                                              color = "cyan",
                                              length = 100,
                                              theta = 0,
                                              jointP = QVector3D(50, 0, 0),
                                              ))
        # self.robot_arm.add_segment(ArmSegment(self.rootEntity,
        #                                       name="Segment3",
        #                                       color="red",
        #                                       length=100,
                                                # theta=180,
        #                                       jointP=QVector3D(150, 0, 0),
        #                                       ))
        self.robot_arm.add_segment(EndEffector(self.rootEntity,
                                              name = "End_effector",
                                              color = "green",
                                              theta = 0,
                                              jointP = QVector3D(150, 0, 0),
                                              ))

    def setupGroundPlane(self):
        self.groundEntity = Qt3DCore.QEntity(self.rootEntity)
        self.groundMesh = Qt3DExtras.QCuboidMesh()
        self.groundMesh.setXExtent(50.0)
        self.groundMesh.setYExtent(0.1)
        self.groundMesh.setZExtent(50.0)
        self.groundMaterial = Qt3DExtras.QPhongMaterial(self.rootEntity)
        self.groundMaterial.setDiffuse(QColor("lightgrey"))
        self.groundTransform = Qt3DCore.QTransform()
        self.groundTransform.setTranslation(QVector3D(0, -2.5, 0))
        self.groundEntity.addComponent(self.groundMesh)
        self.groundEntity.addComponent(self.groundMaterial)
        self.groundEntity.addComponent(self.groundTransform)

class SegmentControllWidget(QWidget):
    angle_changed = Signal(int, float)
    length_changed = Signal(int, float) 

    def __init__(self,
                 segment_id: int, 
                 name: str = "Segment1",
                 min_angle:int = 0,
                 max_angle:int = 180,
                 angle_step:int = 4,
                 parent = None) -> None:
        super(SegmentControllWidget, self).__init__(parent)
        self.segment_id = segment_id
        self.name = name 
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.angle_step = angle_step

        # setup UI
        self.ui = Ui_SegmentControllWidget()
        self.ui.setupUi(self)

        # Setup slider
        # self.ui.angle_label = QLabel(f"Theta_{self.segment_id + 1}")
        self.str_id = f"{self.segment_id + 1}"
        self.ui.angle_label.setText(f"{THETA_UNICODE}<sub>{self.str_id}</sub>")
        self.ui.length_label.setText(f"L<sub>{self.str_id}</sub>")
        self.ui.title.setText(self.name)

        self.ui.angle_slider.setMinimum(self.min_angle)
        self.ui.angle_slider.setMaximum(self.max_angle)
        self.ui.angle_slider.valueChanged.connect(self.emit_angle_change)

        # Rigth btn
        self.timer = QTimer()
        self.ui.right_inc_btn.clicked.connect(self.increment_angle)
        self.ui.right_inc_btn.pressed.connect(self.start_increasing_angle)
        self.ui.right_inc_btn.released.connect(self.stop_timer)

        # Left btn
        self.ui.left_inc_btn.clicked.connect(self.decrement_angle)
        self.ui.left_inc_btn.pressed.connect(self.start_decreasing_angle)
        self.ui.left_inc_btn.released.connect(self.stop_timer)

        # angle spinbox
        self.ui.angle_spinbox.valueChanged.connect(self.emit_angle_change)
        self.set_max_angle(self.max_angle)
        self.set_min_angle(self.min_angle)

        # Length spingbox
        self.ui.length_spinbox.valueChanged.connect(self.emit_length_change)
        self.ui.length_spinbox.setMaximum(200)
        self.ui.length_spinbox.setMinimum(10)

        logger.debug("Intilised segmentController")

    def start_increasing_angle(self):
        self.timer.timeout.connect(self.increment_angle)
        self.timer.start()

    def start_decreasing_angle(self):
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.decrement_angle)
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def increment_angle(self):
        self.ui.angle_slider.setValue(self.ui.angle_slider.value() + self.angle_step)

    def decrement_angle(self):
        self.ui.angle_slider.setValue(self.ui.angle_slider.value() - self.angle_step)

    def on_angle_update(self, angle):
        self.ui.angle_slider.setValue(angle)

    def set_angle(self, angle: float):
        self.ui.angle_slider.setValue(int(angle))
        self.ui.angle_spinbox.setValue(angle)

    def emit_angle_change(self, angle):
        self.set_angle(angle)
        self.angle_changed.emit(self.segment_id, angle)

    def set_length(self, length: float):
        self.ui.length_spinbox.setValue(length)

    def emit_length_change(self, length):
        logger.debug(f"New length: {length}")
        self.length_changed.emit(self.segment_id, length)

    def set_max_angle(self, max_angle:int):
        self.max_angle = max_angle
        self.ui.angle_spinbox.setMaximum(self.max_angle)
        self.ui.angle_slider.setMaximum(self.max_angle)

    def set_min_angle(self, min_angle:int):
        self.min_angle = min_angle
        self.ui.angle_spinbox.setMinimum(self.min_angle)
        self.ui.angle_slider.setMinimum(self.min_angle)

class ControlPanel(QWidget):
    angle_changed = Signal(int, float)
    length_changed = Signal(int, float)

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.segment_controllers: List[SegmentControllWidget] = [] 
        self.position_frames: List = []

        # Connect Signal to Slots

        self.main_layout = QVBoxLayout()

        # self.angleSlider1.setValue(45) # TODO: impl get curr pos
        self.add_segment_controller(0, name="Segment 1",
                                    min_angle=0,
                                    max_angle=180)
        self.add_segment_controller(1, name="Segment 2")
        self.add_segment_controller(2, name="End Effector")

        self.setLayout(self.main_layout)

        logger.debug("Initilised ControlPanel")

    def set_top_bar(self, top_bar):
        self.top_bar = top_bar
        for i, seg_controller in enumerate(self.segment_controllers):
            seg = self.robot_arm.get_seg(seg_controller.segment_id)
            recieve_label = QLabel(seg.pretty_str(i))
            self.position_frames.append(recieve_label)
            self.top_bar.addWidget(recieve_label)

    def set_robot_arm_controller(self, robot_arm:RoboticArm):
        self.robot_arm = robot_arm
        for i, segment_controller in enumerate(self.segment_controllers):
            length = self.robot_arm.get_length(i)
            angle = self.robot_arm.get_angle(i)
            segment_controller.set_length(length)
            segment_controller.set_angle(angle)
            print(f"Initial angle: {angle} Degrees")

    def add_segment_controller(self, segment_id, **kwargs):
        segment_controll = SegmentControllWidget(segment_id, parent=self, **kwargs)
        segment_controll.angle_changed.connect(self.emit_angle_change)
        segment_controll.length_changed.connect(self.emit_length_change)
        # segment_controll.set_length(self.robot_arm.segments[segment_id].length)
        self.segment_controllers.append(segment_controll)
        self.main_layout.addWidget(segment_controll)

    def on_length_updated(self, index, value):
        segment_controller = self.segment_controllers[index]
        segment_controller.set_length(value)

    def update_seg_label(self):
        for index, _ in enumerate(self.segment_controllers):
            seg = self.robot_arm.get_seg(index)
            position_label = self.position_frames[index]
            logger.debug(index)
            position_label.setText(seg.pretty_str(index))

    def emit_angle_change(self, index, value):
        self.angle_changed.emit(index, value)
        self.update_seg_label()

    def emit_length_change(self, index, value):
        self.length_changed.emit(index, value)
        self.update_seg_label()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robotic Arm Simulator")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Simulation 3D Window
        self.sim_window = SimWindow()
        self.sim_container = QWidget.createWindowContainer(self.sim_window, self)
        sim_layout = QVBoxLayout(self.ui.sim_container)
        sim_layout.addWidget(self.sim_container)
        self.statusBar().showMessage("Hello??", 3000)

        # Control panel
        self.controlPanel = ControlPanel()
        right_sidebar_layout = QVBoxLayout(self.ui.right_sidebar)
        right_sidebar_layout.addWidget(self.controlPanel)

        
        # setup lightning, camera etc
        self.sim_window.setup_scene()

        # self.sim_window.robot_arm.update_angle(0, 45)
        # WS Client

        self.ws_client = WebSocketClient(self.sim_window.get_robot_arm())
        # self.ws_client.set_robot_arm(self.sim_window.get_robot_arm())
        self.controlPanel.angle_changed.connect(self.ws_client.send_position_update)
        # self.sim_window.robot_arm.angleUpdated.connect(self.ws_client.send_position_update)
        # self.ws_client.onRecievedCommand.connect(self.handle_command)
        botom_bar = QVBoxLayout(self.ui.bottom_menubar)
        botom_bar.addWidget(self.ws_client)

        self.controlPanel.set_robot_arm_controller(self.sim_window.robot_arm)
        # Signals-slots
        self.controlPanel.angle_changed.connect(self.sim_window.robot_arm.update_angle)
        self.controlPanel.length_changed.connect(self.sim_window.robot_arm.update_length)


        # TopBar
        top_bar = QHBoxLayout(self.ui.top_bar)
        self.controlPanel.set_top_bar(top_bar)


        logger.debug("Intislised MainWindow")

    def complete_setup(self):
        pass
