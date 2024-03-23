import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pathlib import Path

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
        'command': command_payload_schema,
        'error': error_payload_schema,
        'positionUpdate': positionUpdate_payload_schema
        }

def validate_message(message):
    # Validate the general structure
    try:
        validate(instance=message, schema=general_schema)
    except ValidationError as e:
        return f"General validation error: {e}", False

    # Extract message type and payload
    message_type = message["messageType"]
    payload = message["payload"]

    # Get the corresponding payload schema based on message type
    payload_schema = json_payload_map.get(message_type)

    if not payload_schema:
        return f"Unknown messageType: {message_type}", False

    # Validate the payload
    try:
        validate(instance=payload, schema=payload_schema)
    except ValidationError as e:
        return f"Payload validation error: {e}", False

    return "valid", True 
