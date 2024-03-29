import json
from pathlib import Path
from typing import Dict

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from commonlib.enums import MessageType

from commonlib.errors import (GeneralValidationError,
                              PayloadValidationError,
                              UnknownMessageTypeError,
                              UnknownIdentifierTypeError)

SCHEMA_DIR = Path(__file__).parent.parent / 'json_schemas'

def load_schema(schema_name):
    schema_path = SCHEMA_DIR / f'{schema_name}.json'
    print(schema_path)
    with open(schema_path, 'r') as schema_file:
        return json.load(schema_file)


general_schema = load_schema('general')
command_payload_schema = load_schema('command')
error_payload_schema = load_schema('error')
positionUpdate_payload_schema = load_schema('positionUpdate')


json_payload_map = {
        MessageType.COMMAND.value: command_payload_schema,
        MessageType.ERROR.value: error_payload_schema,
        MessageType.POSITIONUPDATE.value: positionUpdate_payload_schema
        }

def validate_message(message: Dict):
    """Validates python dict against a defined json schema"""
    # Validate the general structure
    try:
        validate(instance=message, schema=general_schema)
    except ValidationError as e:
        raise GeneralValidationError(f"General validation error: {e}")

    # Validate only if payload is passed
    if "payload" in message:
        # Extract message type and payload
        message_type = message.get("messageType")
        payload = message.get("payload")

        
        # Get the corresponding payload schema based on message type
        payload_schema = json_payload_map.get(message_type)

        if not payload_schema:
            raise UnknownMessageTypeError("Unknown messageType: {message_type}")

        # Validate the payload
        try:
            validate(instance=payload, schema=payload_schema)
        except ValidationError as e:
            raise PayloadValidationError("Payload validation error: {e}")
