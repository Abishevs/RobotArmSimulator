from typing import List
import numpy as np
import math

from PySide6.QtCore import (QObject, QPropertyAnimation)
from PySide6.QtGui import (QVector3D)

from robo_arm_sim.entities import ArmSegment, BasePlate
from commonlib.logger import LoggerConfig as Log

class RoboticArm(QObject):
    def __init__(self):
        self.base: BasePlate
        self.segments: List[ArmSegment] = []

    def add_base(self, base: BasePlate):
        self.base = base

    def add_segment(self, segment):
        self.segments.append(segment)

    def update_angle(self, index:int, angle:float):
        seg = self.segments[index]
        seg.theta = angle
        self.forward_kinematics()
        EF = self.segments[-1]
        Log.debug(f"End effectors x,y: {EF.get_endp_str()}. Theta: {EF.get_theta_str()}")

    def forward_kinematics(self):
        """Calculate new postions and updates it gets called on angle changes"""
        first_seg = self.segments[0]
        cummulativ_angle = first_seg.theta # Initiate angle
        prev_x, prev_y = first_seg.jointP.x(), first_seg.jointP.y() # get base jointP

        for i, seg in enumerate(self.segments):
            cummulativ_angle += seg.theta

            # Calc curr seg endP
            new_x = prev_x + seg.length * math.cos(np.deg2rad(cummulativ_angle))
            new_y = prev_y + seg.length * math.sin(np.deg2rad(cummulativ_angle))

            # set newEndP
            new_endP = QVector3D(new_x,new_y,0)
            seg.endP = new_endP

            # apply transformation
            seg.controller.setRotationPoint(seg.jointP)
            seg.controller.setAngle(cummulativ_angle)

            # set currents seg endP as next seg JointP
            if i < len(self.segments) - 1:
                self.segments[i + 1].jointP = seg.endP

            prev_x, prev_y = new_x, new_y
        
    def animate(self):
        for seg in self.segments:
            animation = QPropertyAnimation(seg.controller)
            animation.setTargetObject(seg.controller)
            animation.setPropertyName(b"angle")
            animation.setStartValue(0)
            animation.setEndValue(360)
            animation.setDuration(10000)
            animation.setLoopCount(-1)
            animation.start()
