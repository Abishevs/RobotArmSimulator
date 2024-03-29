class MessageValidationError(Exception):
    """Base class for message validation errors."""
    pass

class GeneralValidationError(MessageValidationError):
    """Raised for general JSON structure validation errors."""
    pass

class UnknownMessageTypeError(MessageValidationError):
    """Raised when an unknown message type is encountered."""
    pass

class UnknownIdentifierTypeError(MessageValidationError):
    """Raised when identifier is unkown type"""
    pass

class PayloadValidationError(MessageValidationError):
    """Raised for errors validating the specific payload of a message."""
    pass

