from PySide6.QtGui import (QColor, QVector3D)
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras

from robo_arm_sim.controllers import JointTransformController

class GenericEntity:
    def __init__(self, 
                 parent = None, 
                 color: str = "yellow",
                 scale: float = 0.1,
                 name: str = "Base",
                 position: QVector3D = QVector3D(0,0,0),
                 jointP: QVector3D = QVector3D(0,0,0)) -> None:
        self.entity = Qt3DCore.QEntity(parent)
        self.color = color
        self.scale = scale    # 3D worlds scale
        self.name = name     # Identifier
        self.position = position # mesh local origin position in 3D world
        self.jointP = jointP   # Pivot point for next segment to attach to 

        # Setup material
        self.material = Qt3DExtras.QPhongMaterial()
        self.material.setDiffuse(QColor(self.color))

        # Setup transformations
        self.transform = Qt3DCore.QTransform()
        self.transform.setTranslation(self.position)
        
        self.entity.addComponent(self.material)
        self.entity.addComponent(self.transform)

    def add_mesh(self, mesh):
        self.mesh = mesh
        self.entity.addComponent(self.mesh)

    def get_jointP(self):
        return self.pivotP

    def set_jointP(self, new_pivotP: QVector3D):
        self.pivotP = new_pivotP

    def set_position(self, new_position: QVector3D):
        self.position = new_position
        self.transform.setTranslation(self.position)

class Joint(GenericEntity):
    def __init__(self, 
                 parent = None,
                 color: str = "red",
                 scale: float = 0.1,
                 name: str = "Joint",
                 radius: float = 8,
                 length: float = 15,
                 position: QVector3D = QVector3D(0, 0, 0),
                 jointP: QVector3D = QVector3D(0, 0, 0)) -> None:
        super().__init__(parent, color, scale, name, position, jointP)
        self.radius = radius
        self.length = length

        jointMesh = Qt3DExtras.QCylinderMesh()
        jointMesh.setRadius(self.radius)  # Adjust the size of the joint
        jointMesh.setLength(self.length)
        self.add_mesh(jointMesh)
        self.transform.setRotationX(90)

class ArmSegment(GenericEntity):
    def __init__(self,
                 parent = None,
                 color: str = "yellow",
                 scale: float = 0.1,
                 name: str = "Base",
                 theta: float = 0,
                 length: float = 50,
                 position: QVector3D = QVector3D(0, 0, 0),
                 jointP: QVector3D = QVector3D(0, 0, 0)) -> None:
        super().__init__(parent, color, scale, name, position, jointP)
        self.theta = theta
        self.length = length

        self.joint = Joint(parent=self.entity, jointP=self.jointP)  

        # Cuboid (Arm segment)
        self.cuboidMesh = Qt3DExtras.QCuboidMesh()
        self.cuboidMesh.setXExtent(self.length)  # Length of the arm segment
        self.cuboidMesh.setYExtent(9)  # Thickness of the arm segment
        self.cuboidMesh.setZExtent(9)  # Depth of the arm segment

        # Transform
        self.cuboidTransform = Qt3DCore.QTransform()
        self.cuboidTransform.setTranslation(QVector3D(self.length / 2, 0, 0))  # Position the cuboid next to the sphere

        # Entity
        self.cuboidEntity = Qt3DCore.QEntity(self.entity)
        self.cuboidEntity.addComponent(self.cuboidMesh)
        self.cuboidEntity.addComponent(self.material)
        self.cuboidEntity.addComponent(self.cuboidTransform)

        self.segment_transform = Qt3DCore.QTransform()
        self.segment_transform.setTranslation(self.jointP)

        self.controller = JointTransformController(self.segment_transform)
        self.controller.setTarget(self.segment_transform)
        self.controller.setRotationPoint(self.jointP)

        self.entity.addComponent(self.material)
        self.entity.addComponent(self.segment_transform)

class BasePlate(Qt3DCore.QEntity):
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

class EndEffector(GenericEntity):
    def __init__(self, 
                 parent = None,
                 theta: float = 0,
                 length: float = 15,
                 color: str = "yellow",
                 scale: float = 0.1,
                 name: str = "Base",
                 position: QVector3D = QVector3D(0, 0, 0),
                 jointP: QVector3D = QVector3D(0, 0, 0)) -> None:
        super().__init__(parent, color, scale, name, position, jointP)
        self.theta = theta
        self.length = length

        self.joint = Joint(parent=self.entity, jointP=self.jointP)

        # Plate
        self.cuboidMesh = Qt3DExtras.QCuboidMesh()
        self.cuboidMesh.setXExtent(40)  
        self.cuboidMesh.setYExtent(10)  
        self.cuboidMesh.setZExtent(10)  

        # Transform
        self.cuboidTransform = Qt3DCore.QTransform()
        self.cuboidTransform.setTranslation(QVector3D(20, 0, 0))  # Position the cuboid next to the sphere
        # self.cuboidTransform.setTranslation(QVector3D(5,0,0))

        # Entity
        self.cuboidEntity = Qt3DCore.QEntity(self.entity)
        self.cuboidEntity.addComponent(self.cuboidMesh)
        self.cuboidEntity.addComponent(self.material)
        self.cuboidEntity.addComponent(self.cuboidTransform)

        self.segment_transform = Qt3DCore.QTransform()
        self.segment_transform.setTranslation(self.jointP)

        self.controller = JointTransformController(self.segment_transform)
        self.controller.setTarget(self.segment_transform)
        self.controller.setRotationPoint(self.jointP)

        self.entity.addComponent(self.material)
        self.entity.addComponent(self.segment_transform)

