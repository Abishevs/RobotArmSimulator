import sys
from typing import List
import numpy as np
import time
import math
from itertools import tee, zip_longest

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QSlider, QLineEdit, QLabel, QPushButton)
from PySide6.QtCore import (Qt, QTimer, Property, QObject, QPropertyAnimation, Signal)


from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import ( QMatrix4x4, QColor, QQuaternion, QVector3D)

# from PySide6.QtCore import Qt
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DExtras import Qt3DExtras


#

"""
World scale 1:10 , 10mm IRL 1 unit in 3D scene.
"""

class JointTransformController(QObject):
    def __init__(self, parent:Qt3DCore.QTransform):
        super().__init__(parent)
        self._target = None | Qt3DCore.QTransform
        self._matrix = QMatrix4x4()
        self._angle = 0
        self._jointP = QVector3D()
        self._axis = QVector3D(0,0,1)

    def setTarget(self, t):
        self._target = t

    def getTarget(self):
        return self._target

    def setRotationPoint(self, point: QVector3D):
        self._jointP = point
        self.updateMatrix()

    def getRotationPoint(self):
        return self._jointP

    def setAngle(self, angle):
        if self._angle != angle:
            self._angle = angle
            self.updateMatrix()
            self.angleChanged.emit()


    def getAngle(self):
        return self._angle

    def updateMatrix(self):
        self._matrix.setToIdentity()
        self._matrix.scale(0.1)
        # 1) Translate to new rotation point
        self._matrix.translate(self._jointP)
        # 2) Rotate
        rotation = QQuaternion.fromAxisAndAngle(self._axis, self._angle)
        self._matrix.rotate(rotation)
        if self._target is not None:
            self._target.setMatrix(self._matrix)

        # print(f"X: {p.x()}, Y:{p.y()}")

    angleChanged = Signal()
    angle = Property(float, getAngle, setAngle, notify=angleChanged)

class BaseEntity(Qt3DCore.QEntity):
    """Default Base for robotic arm. For connecting the first element
    """
    def __init__(self,
                 parent,
                 scale:float = 0.1,
                 rotation:float = -90,
                 color:str="blue",
                 sizeX:float=100,
                 sizeZ:float=100,
                 pivotP:QVector3D=QVector3D(0,0,0)
                 ) -> None:
        super().__init__(parent)
        self.color = color
        self.sizeX = sizeX
        self.sizeZ = sizeZ
        self.pivotP = pivotP
        self.scale = scale
        self.rotation = rotation
        self.material = Qt3DExtras.QPhongMaterial()
        self.material.setDiffuse(QColor(self.color))

        # Base 
        self.base_plateMesh = Qt3DExtras.QCuboidMesh()
        self.base_plateMesh.setXExtent(self.sizeX)  # Length of the base
        self.base_plateMesh.setYExtent(15)  # Base thinkes is halv to the pivotP
        self.base_plateMesh.setZExtent(self.sizeZ)  # Depth of of the base 

        self.base_plate_transform = Qt3DCore.QTransform()
        self.base_plate_transform.setScale(self.scale)
        self.base_plate_transform.setTranslation(QVector3D(0, -1.5, 0))  # Set at origin

        self.base_plate_entity = Qt3DCore.QEntity(self)
        self.base_plate_entity.addComponent(self.base_plateMesh)
        self.base_plate_entity.addComponent(self.material)
        self.base_plate_entity.addComponent(self.base_plate_transform)

        self.extender_mesh = Qt3DExtras.QCuboidMesh()
        self.extender_mesh.setXExtent(10)  # Length of the base
        self.extender_mesh.setYExtent(15)  # extender thinkes is halv to the pivotP
        self.extender_mesh.setZExtent(10)  # Depth of of the extender
        
        self.extender_entity = Qt3DCore.QEntity(self) 
        self.extender_transform = Qt3DCore.QTransform()
        self.extender_transform.setTranslation(QVector3D(0, self.pivotP.y(), 0))
        self.extender_transform.setScale(self.scale)
        # self.extender_transform.setRotationZ(self.rotation)
        
        self.extender_entity.addComponent(self.material)
        self.extender_entity.addComponent(self.extender_mesh)
        self.extender_entity.addComponent(self.extender_transform)

    def get_pivotP(self) -> QVector3D:
        return self.pivotP

    def set_pivotP(self, pivotP:QVector3D):
        self.pivotP = pivotP

class ArmSegment(Qt3DCore.QEntity):
    """Def robotic arm segment an model for 3D Scene
    """
    def __init__(self, 
                 parent=None,
                 jointP:QVector3D=QVector3D(0,0,0),
                 path_to_model="stl/base.stl",
                 name="Base",
                 color="blue",
                 length=50, 
                 theta=0, 
                 ):
        super().__init__(parent)
        self.name = name
        self.color = color
        self.length = length
        self.theta = theta  # Rotation in degrees
        self.jointP = jointP
        self.endP:QVector3D = QVector3D(0,0,0)
        self.setupModel(path_to_model)

    def get_endP(self) -> QVector3D:
        x = self.jointP.x() + self.length * math.cos(np.deg2rad(self.theta))
        y = self.jointP.y() + self.length * math.sin(np.deg2rad(self.theta))
        endP = QVector3D(x,y, self.jointP.z())
        return endP

    def set_endP(self, angle:float):
        x = self.jointP.x() + self.length * math.cos(np.deg2rad(self.theta) + np.deg2rad(angle))
        y = self.jointP.y() + self.length * math.sin(np.deg2rad(self.theta) + np.deg2rad(angle))
        # x = self.jointP.x() + self.length * math.cos(self.theta + angle)
        # y = self.jointP.y() + self.length * math.sin(self.theta + angle)
        endP = QVector3D(x,y, self.jointP.z())
        self.endP = endP
        print(endP)
        return endP

    # def set_jointP(self, point:QVector3D):
    #     self.jointP = point

    # def calculate_end_position(self):
    #     # This is a simplified placeholder calculation
        # theta = np.radians(self.theta_degrees)
    #     orientation = np.array([np.cos(theta), np.sin(theta), 0])
    #     return self.position + self.length * orientation

    def setupModel(self, path:str):
        # Load local model
        # data = QtCore.QUrl.fromLocalFile(path)

        # Mesh STL
        # self.segment_mesh = Qt3DRender.QMesh()
        # self.segment_mesh.setMeshName(self.name)
        # self.segment_mesh.setSource(data)

        # self.material = Qt3DExtras.QPhongMaterial()
        # self.material.setDiffuse(QColor(self.color))

                # Material for the segment
        self.material = Qt3DExtras.QPhongMaterial()
        self.material.setDiffuse(QColor(self.color))

        # Sphere (Joint)
        self.sphereMesh = Qt3DExtras.QSphereMesh()
        self.sphereMesh.setRadius(5)  # Adjust the size of the joint

        self.sphereTransform = Qt3DCore.QTransform()
        # self.sphereTransform.setTranslation(self.jointP)  # Position of the joint
        self.sphereTransform.setTranslation(QVector3D(0,0,0))  # Position of the joint

        self.sphereEntity = Qt3DCore.QEntity(self)
        self.sphereEntity.addComponent(self.sphereMesh)
        self.sphereEntity.addComponent(self.material)
        self.sphereEntity.addComponent(self.sphereTransform)

        # Cuboid (Arm segment)
        self.cuboidMesh = Qt3DExtras.QCuboidMesh()
        self.cuboidMesh.setXExtent(self.length)  # Length of the arm segment
        self.cuboidMesh.setYExtent(9)  # Thickness of the arm segment
        self.cuboidMesh.setZExtent(9)  # Depth of the arm segment

        self.cuboidTransform = Qt3DCore.QTransform()
        self.cuboidTransform.setTranslation(QVector3D(self.length / 2, 0, 0))  # Position the cuboid next to the sphere

        self.cuboidEntity = Qt3DCore.QEntity(self)
        self.cuboidEntity.addComponent(self.cuboidMesh)
        self.cuboidEntity.addComponent(self.material)
        self.cuboidEntity.addComponent(self.cuboidTransform)


        self.segment_transform = Qt3DCore.QTransform()
        self.segment_transform.setTranslation(self.jointP)

        self.controller = JointTransformController(self.segment_transform)
        self.controller.setTarget(self.segment_transform)
        self.controller.setRotationPoint(self.jointP)
        # self.controller.setAngle(45)
        # print(f"Start pos: {self.jointP}")
        # self.sphereRotateTransformAnimation = QPropertyAnimation(self.segment_transform)
        # self.sphereRotateTransformAnimation.setTargetObject(self.controller)
        # self.sphereRotateTransformAnimation.setPropertyName(b"angle")
        # self.sphereRotateTransformAnimation.setStartValue(0)
        # self.sphereRotateTransformAnimation.setEndValue(360)
        # self.sphereRotateTransformAnimation.setDuration(10000)
        # self.sphereRotateTransformAnimation.setLoopCount(-1)
        # self.sphereRotateTransformAnimation.start()

        # self.addComponent(self.segment_mesh)
        self.addComponent(self.material)
        self.addComponent(self.segment_transform)

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip_longest(a, b)
    

class RoboticArm(QObject):
    def __init__(self):
        self.base: BaseEntity
        self.segments: List[ArmSegment] = []

    def add_base(self, base: BaseEntity):
        self.base = base

    def add_segment(self, segment):
        self.segments.append(segment)

    def update_angle(self, angle:float):
        print(f"Got angle: {angle}")
        seg1 = self.segments[0]
        seg1.controller.setAngle(angle)
        self.forward_kinematics()
        # for seg in self.segments:
        #     # seg.controller.setAngle(angle)
        #     seg.controller.updateMatrix()
        # seg2 = self.segments[1]
        # seg2.controller.setRotationPoint(seg2.endP)
        # for seg in self.segments:
        #     seg.controller.setRotationPoint(seg.endP)

    def forward_kinematics(self):
        # Calculate new postions and updates it gets called on angle changes
        # x = self.jointP.x() + self.length * math.cos(np.deg2rad(self.theta))
        # y = self.jointP.y() + self.length * math.sin(np.deg2rad(self.theta))
        # endP = QVector3D(x,y, self.jointP.z())
        # angle = 0
        cummulativ_angle = 0
        prev_endP = QVector3D(0,0,0)
        for i, seg in enumerate(self.segments):
            print(f"index: {i}, cummultive_angle_before: {cummulativ_angle}")
            prev_seg = self.segments[i-1]
            cummulativ_angle += seg.controller.getAngle()
            print(f"index: {i}, cummultive_angle: {cummulativ_angle}")
            new_x = prev_endP.x() + seg.length * math.cos(np.deg2rad(cummulativ_angle))
            new_y = prev_endP.y() + seg.length * math.sin(np.deg2rad(cummulativ_angle))
            # new_x = prev_endP.x() + prev_seg.length * math.cos(np.deg2rad(cummulativ_angle))
            # new_y = prev_endP.y() + prev_seg.length * math.sin(np.deg2rad(cummulativ_angle))
            # print(cummulativ_angle)
            newP = QVector3D(new_x,new_y,0)
            seg.jointP = prev_endP
            seg.endP  = newP

            seg.controller.setRotationPoint(seg.jointP)
            seg.controller.setAngle(cummulativ_angle)
            print(f"name: {seg.name}, newx: {new_x}, newY: {new_y}, Theta: {seg.controller.getAngle()}")
            prev_endP = newP
            # if seg != self.segments[0]:
            #     seg.controller.setRotationPoint(seg.jointP)
            # pos = seg.set_endP(cummulativ_angle)
            # print(f"X: {seg.jointP.x()}, Y:{seg.jointP.y()}")
            # if seg != self.segments[-1]:
            #     self.segments[self.segments.index(seg) + 1].jointP = seg.endP
                # print(f"X: {seg.jointP.x()}, Y:{seg.jointP.y()}")
            # current_pos = seg.jointP
            # seg.controller.updateMatrix()

    def animate(self):
        for seg in self.segments:
            animation = QPropertyAnimation(seg.segment_transform)
            animation.setTargetObject(seg.controller)
            animation.setPropertyName(b"angle")
            animation.setStartValue(0)
            animation.setEndValue(360)
            animation.setDuration(10000)
            animation.setLoopCount(-1)
            animation.start()

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
        # segment1 = ArmSegment(parent=self.rootEntity,
        #                                       path_to_model="3DModels/segment1.stl",
        #                                       position=QVector3D(0, 0, 0),
        #                                       )
        # # print(base.children())
        # self.robot_arm.add_segment(segment1)
        # segment2 = ArmSegment(self.rootEntity,
        #                                       path_to_model="3DModels/segment2.stl",
        #                                       position=QVector3D(0, 0, 0),
        #                                       )
        # self.robot_arm.add_segment(segment2)
        # end_effector = ArmSegment(self.rootEntity,
        #                                       path_to_model="3DModels/end_effector.stl",
        #                                       position=QVector3D(0, 0, -2),
        #                                       )
        # self.robot_arm.add_segment(end_effector)

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
        self.container.setMinimumSize(400, 300)

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


# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

