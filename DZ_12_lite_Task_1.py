import os
from datetime import datetime

# Функция для записи сообщений в лог файл
def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_dir = os.path.join('main_dir', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, 'creation_log.txt')
    with open(log_file_path, 'a') as f:
        f.write(f'{timestamp}: {message}\n')

# Создаем основную директорию для хранения всей структуры в задании
main_dir = 'main_dir'
os.makedirs(main_dir, exist_ok=True)

# Проверка и создание необходимых папок
directories_to_create = [
    'data',
    'data/raw',
    'data/processed',
    'backups',
    'output'
]

for directory in directories_to_create:
    full_path = os.path.join(main_dir, directory)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        log_message(f'Создана директория {full_path}')
    else:
        log_message(f'Директория {full_path} уже существует.')

# Создание нескольких тестовых файлов в каталоге data/raw
files_to_create = {
    'file_utf8.txt': ('UTF-8', 'Привет! Это русский текст.'),
    'file_iso.txt': ('ISO-8859-1', 'Hello! This is English text.'),
}

for filename, (encoding, content) in files_to_create.items():
    file_path = os.path.join('main_dir/data', 'raw', filename)
    try:
        with open(file_path, 'a', encoding=encoding) as f:
            f.write(content)
        log_message(f'Файл {filename} успешно записан ({encoding}).')
    except Exception as e:
        log_message(f'Ошибка при создании файла {filename}: {str(e)}')