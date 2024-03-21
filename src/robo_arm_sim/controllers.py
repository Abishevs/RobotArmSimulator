from PySide6.QtCore import (Property, QObject, Signal)
from PySide6.QtGui import ( QMatrix4x4, QQuaternion, QVector3D)
from PySide6.Qt3DCore import Qt3DCore

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


