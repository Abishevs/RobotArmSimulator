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

from robo_arm_sim.controllers import JointTransformController

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

