from PySide6.QtCore import (Property, QObject, Signal)
from PySide6.QtGui import ( QMatrix4x4, QQuaternion, QVector3D)
from PySide6.Qt3DCore import Qt3DCore

class JointTransformController(QObject):
    """
    Handles 3D scene segment position and rotation via a single 4x4Matrix
    """
    def __init__(self, parent:Qt3DCore.QTransform):
        super().__init__(parent)
        self._target = None | Qt3DCore.QTransform
        self._matrix = QMatrix4x4()
        self._angle = 0
        self._jointP = QVector3D()
        self._axis = QVector3D(0,0,1)

    def set_target(self, t):
        self._target = t

    def get_target(self):
        return self._target

    def set_rotation_point(self, point: QVector3D):
        self._jointP = point
        self.update_matrix()

    def get_rotation_point(self):
        return self._jointP

    def set_angle(self, angle):
        if self._angle != angle:
            self._angle = angle
            self.update_matrix()
            self.angle_changed.emit()


    def get_angle(self):
        return self._angle

    def update_matrix(self):
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

    angle_changed = Signal()
    angle = Property(float, get_angle, set_angle, notify=angle_changed)


