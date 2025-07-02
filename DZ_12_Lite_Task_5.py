import json
import logging
import os
from datetime import datetime

import jsonschema
from jsonschema import validate

# Основные константы для путей
ROOT_DIR = "main_dir/"
LOGS_DIR = ROOT_DIR + "logs/"
DATA_PROCEED_DIR = ROOT_DIR + "data/processed/"

# Создаем директорию logs, если она ещё не существует
os.makedirs(LOGS_DIR, exist_ok=True)

# Настройка логгера
log_file_path = LOGS_DIR + "fileinfo.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='UTF-8'
)
logger = logging.getLogger(__name__)


class FileInfo:
    def __init__(self, path):
        logger.info(f"Processing file at {path}.")
        self.path = path
        self.name = os.path.basename(path)
        try:
            stats = os.stat(self.path)
            self.size = stats.st_size
            self.created_at = datetime.fromtimestamp(stats.st_ctime).isoformat()
            self.modified_at = datetime.fromtimestamp(stats.st_mtime).isoformat()
        except OSError as e:
            logger.error(f"Error processing file {path}: {e}")
            raise

    def to_dict(self):
        return {
            'name': self.name,
            'path': self.path,
            'size': self.size,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }


# Собираем информацию о файлах
def collect_file_info(directory):
    file_infos = []
    for root, _, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            try:
                info = FileInfo(full_path)
                file_infos.append(info.to_dict())
            except Exception as e:
                logger.error(f"Failed to process file {full_path}: {e}")
    return file_infos


# Сохраняем собранные данные в JSON
def save_to_json(file_list, output_filename='file_info.json'):
    output_path = os.path.join(DATA_PROCEED_DIR, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(file_list, f, ensure_ascii=False, indent=4)


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


if __name__ == "__main__":
    # Используем рабочий каталог proceed/
    directory = DATA_PROCEED_DIR
    infos = collect_file_info(directory)
    save_to_json(infos)