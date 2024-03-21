from PySide6.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QSlider, QLineEdit, QLabel, QPushButton)
from PySide6.QtCore import (Qt, Signal)
from PySide6 import QtGui
from PySide6.QtGui import (QColor, QVector3D)
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6 import QtGui
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QVector3D
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow, QSlider, QWidget

from robo_arm_sim.entities import ArmSegment, BaseEntity
from robo_arm_sim.robotic_arm import RoboticArm

class SimWindow(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super().__init__()
        self.rootEntity = Qt3DCore.QEntity()
        self.defaultFrameGraph().setClearColor(QtGui.QColor("white"))


        # Camera setup
        self.camera().lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 100.0)
        self.camera().setPosition(QtGui.QVector3D(30, 20, 50))
        self.camera().setViewCenter(QtGui.QVector3D(0, 0, 0))

        # Setup models
        self.setupModels() 
        # offset_vec = QVector3D(-1, 2, -1)
        # rot_angle = QVector3D(0,0,90)
        # self.robot_arm.segments[1].segment_transform.setTranslation(-offset_vec)
        # rotation = QQuaternion.fromAxisAndAngle(QVector3D(0,0,1), 45)
        # self.robot_arm.segments[1].segment_transform.setRotation(rotation)
        # self.robot_arm.segments[1].segment_transform.tr(rotation)
        # self.robot_arm.segments[1].segment_transform.setTranslation(offset_vec)
        self.setupGroundPlane()

        # Camera controller
        camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        camController.setCamera(self.camera())

        self.setRootEntity(self.rootEntity)
        # self.show()
        # self.robot_arm.animate()

        # self.setupDebugCube()



    def setupModels(self):
        self.robot_arm = RoboticArm()
        base = BaseEntity(self.rootEntity)
        self.robot_arm.add_base(base)
        self.robot_arm.add_segment(ArmSegment(self.rootEntity,
                                              name="Segment1",
                                              color="yellow",
                                              length=50,
                                              path_to_model="stl/segment1.stl",
                                              jointP=QVector3D(0, 0, 0),
                                              # position=QVector3D(0, 0, 0),
                                              ))
        self.robot_arm.add_segment(ArmSegment(self.rootEntity,
                                              name="Segment2",
                                              color="red",
                                              length=100,
                                              path_to_model="stl/segment2.stl",
                                              jointP=QVector3D(50, 0, 0),
                                              ))
        self.robot_arm.add_segment(ArmSegment(self.rootEntity,
                                              name="End_effector",
                                              color="blue",
                                              path_to_model="stl/end_effector.stl",
                                              length=100,
                                              jointP=QVector3D(150, 0, 0),
                                              ))

    def setupGroundPlane(self):
        self.groundEntity = Qt3DCore.QEntity(self.rootEntity)
        self.groundMesh = Qt3DExtras.QCuboidMesh()
        self.groundMesh.setXExtent(100.0)
        self.groundMesh.setYExtent(0.1)
        self.groundMesh.setZExtent(100.0)
        self.groundMaterial = Qt3DExtras.QPhongMaterial(self.rootEntity)
        self.groundMaterial.setDiffuse(QColor("lightgrey"))
        self.groundTransform = Qt3DCore.QTransform()
        self.groundTransform.setTranslation(QVector3D(0, -3, 0))
        self.groundEntity.addComponent(self.groundMesh)
        self.groundEntity.addComponent(self.groundMaterial)
        self.groundEntity.addComponent(self.groundTransform)

class ControlPanel(QWidget):
    angleChanged = Signal(float)
    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.layout = QVBoxLayout()

        # Example control: slider for angle
        self.angleSlider = QSlider(Qt.Orientation.Horizontal)
        self.angleSlider.setMinimum(0)
        self.angleSlider.setMaximum(180)
        self.layout.addWidget(self.angleSlider)

        # Example control: line edit for length
        self.lengthInput = QLineEdit()
        self.layout.addWidget(QLabel("Length:"))
        self.layout.addWidget(self.lengthInput)
        
        # Signal
        self.angleSlider.valueChanged.connect(self.emit_angle_change)

        self.setLayout(self.layout)

    def emit_angle_change(self, value):
        self.angleChanged.emit(value)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robotic Arm Simulator")
        # Main widget and layout
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()

        # SimWindow
        self.view = SimWindow()

        # Create a container widget for the Qt 3D window
        self.container = QWidget.createWindowContainer(self.view)
        self.container.setMinimumSize(800, 800)

        # Set the scene root entity

        # Control panel
        self.controlPanel = ControlPanel()


        # Signals-slots
        self.controlPanel.angleChanged.connect(self.view.robot_arm.update_angle)

        # Add widgets to the layout
        self.mainLayout.addWidget(self.container, 1)  # The '1' gives it a stretch factor to take up more space
        self.mainLayout.addWidget(self.controlPanel)

        # Set the layout on the main widget and make it the central widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
