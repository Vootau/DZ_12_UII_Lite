import json
import os
from datetime import datetime
import logging

# Настраиваем логирование
LOGS_DIR = "main_dir/logs/"
LOG_FILE_PATH = os.path.join(LOGS_DIR,'logging_output.log')
OUTPUT_JSON_PATH = 'main_dir/output/processed_data.json'
DATA_DIRECTORY = 'main_dir/data/processed/'

# Структура уровней логирования
LOG_LEVELS = {
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO
}

# Настроим базовую конфигурацию логирования
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Собираем информацию обо всех файлах в директории
def collect_file_info(directory):
    all_files_info = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(root, filename)

            try:
                # Попытка считывания файла
                with open(full_path, 'r', encoding='utf-8') as file:
                    original_text = file.read()
                    modified_text = original_text.swapcase()  # меняем регистр
                    size_in_bytes = os.path.getsize(full_path)
                    last_modified_time = datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()

                    # Формируем объект с информацией о файле
                    file_info = {
                        'filename': filename,
                        'original_text': original_text,
                        'modified_text': modified_text,
                        'size_in_bytes': size_in_bytes,
                        'last_modified': last_modified_time
                    }

                    all_files_info.append(file_info)
                    log_message(level=3, message=f"Файл {filename} успешно обработан.")
            except FileNotFoundError:
                log_message(level=1, message=f"Файл {full_path} не найден.")
            except OSError as err:
                log_message(level=1, message=f"Ошибка при доступе к файлу {full_path}: {err.strerror}")
            except UnicodeDecodeError:
                log_message(level=2, message=f"Не удалось считать файл {full_path} в кодировке utf-8.")

    return all_files_info


# Логирование события
def log_message(level, message):
    logging.log(LOG_LEVELS[level], message)


# Главный сценарий выполнения
if __name__ == '__main__':
    collected_data = collect_file_info(DATA_DIRECTORY)

    # Сохраняем собранные данные в JSON-файл
    if not os.path.exists('main_dir/output'):
        os.mkdir('main_dir/output')

    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as out_json:
        json.dump(collected_data, out_json, ensure_ascii=False, indent=4)

    log_message(level=3, message="Все файлы обработаны и сохранены в JSON.")