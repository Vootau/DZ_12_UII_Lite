import os
import jsonschema
import logging
import json
from jsonschema import validate

# Настройка логгера
logger = logging.getLogger(__name__)

# JSON Schema для валидации
json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "path": {"type": "string"},
            "size": {"type": "integer"},
            "created_at": {"type": "string", "format": "date-time"},
            "modified_at": {"type": "string", "format": "date-time"}
        },
        "required": ["name", "path", "size", "created_at", "modified_at"]
    }
}

# Проверка JSON-данных по схеме
def validate_json(json_data, schema=json_schema):
    try:
        validate(instance=json_data, schema=schema)
        logger.info("JSON data validation successful.")
    except jsonschema.exceptions.ValidationError as err:
        logger.error(f"Validation error: {err.message}")

# Абсолютный путь к файлу
FILE_PATH = os.path.join(DATA_PROCEED_DIR, 'file_info.json')

# Проверяем существование файла
if not os.path.exists(FILE_PATH):
    logger.error(f"File does not exist: {FILE_PATH}")
else:
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        file_info_data = json.load(f)
    validate_json(file_info_data)