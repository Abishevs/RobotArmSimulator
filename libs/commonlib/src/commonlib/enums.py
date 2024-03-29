from enum import Enum

class ErrorCode(Enum):
    SERVER_ERROR = 500

class Identifier(Enum):
    GUI = "gui"
    MANAGED = "managed"
    CONTROLLER = "controller"
    VIEWER = "viewer"

class MessageType(Enum):
    COMMAND = "command"
    ERROR = "error"
    POSITIONUPDATE = "positionUpdate"
