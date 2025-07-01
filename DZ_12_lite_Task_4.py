import os
import logging
import time
import zipfile

# Настройка глобальных констант
SOURCE_DIR = 'main_dir/data/'              # Каталог, откуда берутся файлы
BACKUP_DIR = 'main_dir/backups/'           # Место сохранения резервных копий
ARCHIVE_NAME_TEMPLATE = 'backup_%Y%m%d.zip'  # Шаблон названия архива
LOG_FILE_PATH = 'main_dir/logs/backup_log.log'  # Путь к файлу логов

# Настройка логирования
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Функционал создания архива
def create_backup_archive(source_dir, target_dir):
    current_time = time.strftime('%Y%m%d')
    archive_name = ARCHIVE_NAME_TEMPLATE.replace('%Y%m%d', current_time)
    full_archive_path = os.path.join(target_dir, archive_name)

    # Проверяем наличие целевой директории и создаем ее, если нужно
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Создаем ZIP-архив
    with zipfile.ZipFile(full_archive_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for folder, subfolders, files in os.walk(source_dir):
            relative_folder = os.path.relpath(folder, source_dir)
            for file in files:
                absolute_file_path = os.path.join(folder, file)
                arcname = os.path.join(relative_folder, file)
                zf.write(absolute_file_path, arcname)

    logging.info(f"Создан архив {archive_name}.")

# Главная точка входа
if __name__ == '__main__':
    try:
        create_backup_archive(SOURCE_DIR, BACKUP_DIR)
        logging.info("Резервное копирование выполнено успешно!")
    except Exception as ex:
        logging.error(f"Возникла ошибка: {ex}")