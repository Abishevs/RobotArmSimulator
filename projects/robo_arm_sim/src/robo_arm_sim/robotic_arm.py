import logging
import math
from typing import List

import numpy as np
from PySide6.QtCore import (QObject, QPropertyAnimation, Signal)
from PySide6.QtGui import (QVector3D)

from robo_arm_sim.entities import ArmSegment, BasePlate

logger = logging.getLogger(__name__)


class RoboticArm(QObject):
    angle_updated = Signal(int, float)
    # length_updated = Signal(int, float)

    def __init__(self):
        self.base: BasePlate
        self.segments: List[ArmSegment] = []
        logger.debug("Initilised RoboticArmController")

    def add_base(self, base: BasePlate):
        self.base = base

    def add_segment(self, segment):
        self.segments.append(segment)

    def get_seg(self, index: int):
        seg = self.segments[index]
        return seg

    def get_angle(self, index: int) -> float:
        """ Theta range 0-180 """
        seg = self.get_seg(index)
        return seg.theta * 2 if index == 0 else seg.theta + 90

    def set_angle(self, index: int, angle: float):
        """Theta range 0-180"""
        seg = self.get_seg(index)
        new_angle = angle / 2 if index == 0 else angle - 90
        seg.theta = new_angle
        self.forward_kinematics()

    def get_length(self, index: int) -> float:
        return self.get_seg(index).length

    def update_length(self, index: int, length: float):
        seg = self.segments[index]
        seg.set_length(length)
        logger.debug(f"seg {seg.name} length: {seg.length}")
        self.forward_kinematics()
        # self.lengthUpdated.emit(index, length)

    def update_angle(self, index: int, angle: float):
        self.set_angle(index, angle)
        self.forward_kinematics()
        # self.angleUpdated.emit(index, angle)
        EF = self.segments[-1]
        logger.debug(f"End effectors x,y: {EF.get_endp_str()}. Theta: {EF.get_theta_str()}")

    def forward_kinematics(self):
        """Calculate new postions and updates it gets called on angle changes
        """
        first_seg = self.segments[0]
        cummulativ_angle = first_seg.theta  # Initiate angle
        # get base jointP
        prev_x, prev_y = first_seg.jointP.x(), first_seg.jointP.y()

        for i, seg in enumerate(self.segments):
            cummulativ_angle += seg.theta
            logger.debug(f"seg: {seg.name}: Theta: {self.get_angle(i)}")

            # Calc curr seg endP
            dx = seg.length * math.cos(np.deg2rad(cummulativ_angle))
            dy = seg.length * math.sin(np.deg2rad(cummulativ_angle))
            new_x, new_y = prev_x + dx, prev_y + dy

            # set newEndP
            new_endP = QVector3D(new_x, new_y, 0)
            seg.endP = new_endP

            # apply transformation
            seg.controller.set_rotation_point(seg.jointP)
            logger.debug(f"seg: {seg.name}: jointP: {seg.jointP}")
            seg.controller.set_angle(cummulativ_angle)

            # set currents seg endP as next seg JointP
            if i < len(self.segments) - 1:
                self.segments[i + 1].jointP = seg.endP

            prev_x, prev_y = new_x, new_y

    def get_current_positions(self):
        """Returns a dict of currentAngles"""
        current_angles = {"positions": []}
        for i, _ in enumerate(self.segments):
            current_angle = {"jointId": i + 1, "currentAngle": self.get_angle(i)}
            current_angles["positions"].append(current_angle)

        return current_angles

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
