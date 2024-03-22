from functools import partial
from PySide6.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QSlider, QLineEdit, QLabel, QPushButton)
from PySide6.QtCore import (Qt, Signal)
from PySide6 import QtGui
from PySide6.QtGui import (QColor, QVector3D)
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6 import QtGui
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QVector3D
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow, QSlider, QWidget

from robo_arm_sim.entities import ArmSegment, BasePlate, EndEffector
from robo_arm_sim.robotic_arm import RoboticArm

class SimWindow(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super().__init__()
        self.rootEntity = Qt3DCore.QEntity()
        self.defaultFrameGraph().setClearColor(QtGui.QColor("black"))


        # Camera setup
        self.camera().lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 100.0)
        self.camera().setPosition(QtGui.QVector3D(-40, 25, -50))
        self.camera().setViewCenter(QtGui.QVector3D(0, 0, 0))

        # Setup models
        self.setupModels() 
        self.setupGroundPlane()

        # Camera controller
        self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        self.camController.setCamera(self.camera())

        # light source
        lightEntity = Qt3DCore.QEntity(self.rootEntity)
        light = Qt3DRender.QDirectionalLight(lightEntity)
        light.setColor("white")
        light.setIntensity(1)  # Adjust intensity as needed
        light.setWorldDirection(QVector3D(1, -1, 1))  # Adjust direction as needed
        lightEntity.addComponent(light)

        self.setRootEntity(self.rootEntity)
        # self.robot_arm.animate()

    def setupModels(self):
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

class ControlPanel(QWidget):
    angleChanged = Signal(int, float)
    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.layout = QVBoxLayout()

        # Example control: slider for angle
        self.angleSlider1 = QSlider(Qt.Orientation.Horizontal)
        self.angleSlider1.setMinimum(0)
        self.angleSlider1.setSingleStep(1)
        self.angleSlider1.setMaximum(90)
        self.angleSlider1.setValue(45) # TODO: impl get curr pos
        self.layout.addWidget(self.angleSlider1)

        # Example control: slider for angle
        self.angleSlider2 = QSlider(Qt.Orientation.Horizontal)
        self.angleSlider2.setMinimum(-90)
        self.angleSlider2.setMaximum(90)
        self.layout.addWidget(self.angleSlider2)

        self.angleSlider3 = QSlider(Qt.Orientation.Horizontal)
        self.angleSlider3.setMinimum(-90)
        self.angleSlider3.setMaximum(90)
        self.layout.addWidget(self.angleSlider3)


        # Example control: line edit for length
        self.lengthInput = QLineEdit()
        self.layout.addWidget(QLabel("Length:"))
        self.layout.addWidget(self.lengthInput)
        
        # Signal
        self.angleSlider1.valueChanged.connect(partial(self.emit_angle_change, 0))
        self.angleSlider2.valueChanged.connect(partial(self.emit_angle_change, 1))
        self.angleSlider3.valueChanged.connect(partial(self.emit_angle_change, 2))

        self.setLayout(self.layout)

    def emit_angle_change(self, index, value):
        self.angleChanged.emit(index, value)

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
        self.view.robot_arm.update_angle(0, 45)

        # Add widgets to the layout
        self.mainLayout.addWidget(self.container, 1)  # The '1' gives it a stretch factor to take up more space
        self.mainLayout.addWidget(self.controlPanel)

        # Set the layout on the main widget and make it the central widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
