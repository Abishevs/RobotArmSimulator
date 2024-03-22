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

from robo_arm_sim.entities import ArmSegment, BasePlate, EndEffector
from robo_arm_sim.robotic_arm import RoboticArm
from robo_arm_sim.ui.ui_angle_controll_widget import Ui_SegmentControllWidget
from robo_arm_sim.ui.ui_mainwindow import Ui_MainWindow
from commons.logger import LoggerConfig as Log

class WebSocketClient(QWidget):
    onRecievedCommand = Signal(str)

    def __init__(self, host: str = "ws://localhost:4203"):
        super().__init__()
        self.host = host
        self.websocket = QWebSocket()
        self.websocket.connected.connect(self.on_connected)
        self.websocket.disconnected.connect(self.on_disconnected)
        self.websocket.textMessageReceived.connect(self.on_text_message_received)
        self.websocket.errorOccurred.connect(self.on_error)

        self.host_text = QLabel(f"Server IP: '{self.host}'")

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.host_text)
        self.main_layout.addWidget(self.connect_button)
        
    @Slot(QWebSocketProtocol.CloseCode)
    def on_error(self, error_code):
        # print(f"Error code: {error_code}")
        Log.err(f"Error code: {error_code}")

    def toggle_connection(self):
        if not self.websocket.isValid():
            self.websocket.open(self.host)
            self.connect_button.setText("Connecting...")
        else:
            self.websocket.close()
            
    def connect_to_server(self):
        self.websocket.open(self.host)

    def disconnect_from_server(self):
        self.websocket.disconnect(self.websocket)
        
    @Slot()
    def on_connected(self):
        Log.info("Connected to server")
        self.websocket.sendTextMessage("Hello, server!")
        self.connect_button.setText("Disconnect")
        
    @Slot()
    def on_disconnected(self):
        Log.info("Disconnected from server")
        self.connect_button.setText("Connect")
        
    @Slot(str)
    def on_text_message_received(self, message):
        self.onRecievedCommand.emit(message)
        Log.info(f"Message from server: {message}")

class SimWindow(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super().__init__()
        self.rootEntity = Qt3DCore.QEntity()
        self.defaultFrameGraph().setClearColor(QtGui.QColor("black"))
        self.setup_models()
        self.setup_scene()

    def setup_scene(self):
        # Camera setup
        self.camera().lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 100.0)
        self.camera().setPosition(QtGui.QVector3D(-40, 25, -50))
        self.camera().setViewCenter(QtGui.QVector3D(0, 0, 0))

        # Setup models
        self.setup_models() 
        self.setupGroundPlane()

        # Camera controller
        self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        self.camController.setCamera(self.camera())

        # light source
        lightEntity = Qt3DCore.QEntity(self.rootEntity)
        light = Qt3DRender.QDirectionalLight(lightEntity)
        light.setColor("white")
        light.setIntensity(1.5)  # Adjust intensity as needed
        light.setWorldDirection(QVector3D(1, -1, 1))  # Adjust direction as needed
        lightEntity.addComponent(light)

        self.setRootEntity(self.rootEntity)
        # self.robot_arm.animate()


    def setup_models(self):
        self.robot_arm = RoboticArm()
        base = BasePlate(self.rootEntity)
        self.robot_arm.add_base(base)
        self.robot_arm.add_segment(ArmSegment(self.rootEntity,
                                              name="Segment1",
                                              color="yellow",
                                              length=50,
                                              jointP=QVector3D(0, 0, 0),
                                              ))
        self.robot_arm.add_segment(ArmSegment(self.rootEntity,
                                              name="Segment2",
                                              color="cyan",
                                              length=100,
                                              # theta=90,
                                              jointP=QVector3D(50, 0, 0),
                                              ))
        # self.robot_arm.add_segment(ArmSegment(self.rootEntity,
        #                                       name="Segment3",
        #                                       color="red",
        #                                       length=100,
        #                                       # theta=180,
        #                                       jointP=QVector3D(150, 0, 0),
        #                                       ))
        self.robot_arm.add_segment(EndEffector(self.rootEntity,
                                              name="End_effector",
                                              color="green",
                                              # theta=180,
                                              jointP=QVector3D(150, 0, 0),
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
    angleChanged = Signal(int, float)

    def __init__(self,
                 segment_id:int, 
                 name:str="Segment1",
                 min_angle:int = -90,
                 max_angle:int = 90,
                 angle_step:int = 1,
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
        self.ui.angle_label.setText(f"Theta_{self.segment_id + 1}")
        self.ui.length_label.setText(f"Length_{self.segment_id + 1}")
        self.ui.title.setText(self.name)

        self.ui.angle_slider.setMinimum(self.min_angle)
        self.ui.angle_slider.setMaximum(self.max_angle)
        self.ui.angle_slider.valueChanged.connect(self.emit_angle_change)

        # setup buttons
        self.timer = QTimer()
        self.ui.right_inc_btn.clicked.connect(self.increment_angle)
        self.ui.right_inc_btn.pressed.connect(self.start_increasing_angle)
        self.ui.right_inc_btn.released.connect(self.stop_timer)
        

        self.ui.left_inc_btn.clicked.connect(self.decrement_angle)
        self.ui.left_inc_btn.pressed.connect(self.start_decreasing_angle)
        self.ui.left_inc_btn.released.connect(self.stop_timer)

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

    def emit_angle_change(self, angle):
        self.angleChanged.emit(self.segment_id, angle)

    def set_max_angle(self, max_angle:int):
        self.max_angle = max_angle
        self.ui.angle_slider.setMaximum(self.max_angle)

    def set_min_angle(self, min_angle:int):
        self.min_angle = min_angle
        self.ui.angle_slider.setMaximum(self.min_angle)

class ControlPanel(QWidget):
    angleChanged = Signal(int, float)
    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.main_layout = QVBoxLayout()

        # self.angleSlider1.setValue(45) # TODO: impl get curr pos
        self.add_segment_controller(0, 
                                    name="Segment 1",
                                    min_angle=0,
                                    max_angle=90)
        self.add_segment_controller(1, name="Segment 2")
        self.add_segment_controller(2, name="End Effector")

        self.setLayout(self.main_layout)

    def add_segment_controller(self, segment_id, **kwargs):
        segment_controll = SegmentControllWidget(segment_id, parent=self, **kwargs)
        segment_controll.angleChanged.connect(self.emit_angle_change)
        self.main_layout.addWidget(segment_controll)

    def emit_angle_change(self, index, value):
        self.angleChanged.emit(index, value)

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


        # WS Client
        self.ws_client = WebSocketClient()
        self.ws_client.onRecievedCommand.connect(self.handle_command)
        botom_bar = QVBoxLayout(self.ui.bottom_menubar)
        botom_bar.addWidget(self.ws_client)

        # TopBar
        top_bar = QHBoxLayout(self.ui.top_bar)
        self.reciev_label = QLabel("Nothing yet")
        top_bar.addWidget(self.reciev_label)
        
        # self.sim_window.setup_scene()

        # Signals-slots
        self.controlPanel.angleChanged.connect(self.sim_window.robot_arm.update_angle)
        # self.sim_window.robot_arm.update_angle(0, 45)

    @Slot(str)
    def handle_command(self, msg):
        self.reciev_label.setText(f"Got from server: {msg}")

