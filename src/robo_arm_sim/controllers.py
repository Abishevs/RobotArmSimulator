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

from robo_arm_sim.entities import ArmSegment, BaseEntity


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

