import os
import logging
import hashlib
import zipfile
import glob

# Глобальные настройки
SOURCE_DIR = 'main_dir/data/'          # Рабочий каталог для резервного копирования
BACKUP_DIR = os.path.normpath('main_dir/backups/')       # Место хранения резервных копий
LOG_FILE_PATH = 'main_dir/logs/restore_log.log'  # Файл логов

# Настройка логирования
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='UTF-8'
)

# Функция вычисляет MD5-хеш файла
def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

# Проверяет целостность восстановленного файла путем сравнения хешей
def verify_integrity(original_file_path, restored_file_path):
    original_hash = calculate_md5(original_file_path)
    restored_hash = calculate_md5(restored_file_path)
    return original_hash == restored_hash

# Процесс восстановления данных
def restore_latest_backup():
    # Найдем самый свежий архив
    archives = sorted(glob.glob(os.path.join(BACKUP_DIR, '*.zip')), key=os.path.getmtime, reverse=True)
    latest_archive = archives[0] if archives else None

    if not latest_archive:
        logging.error("Нет доступных архивов для восстановления.")
        return

    logging.info(f"Начинаем восстановление из архива {latest_archive}.")

    # Прямо распаковываем архив в исходную директорию
    with zipfile.ZipFile(latest_archive, 'r') as zf:
        zf.extractall(SOURCE_DIR)

    # Проверяем целостность файлов после восстановления
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            abs_file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(abs_file_path, SOURCE_DIR)
            archived_file_path = os.path.join(SOURCE_DIR, rel_file_path)

            # Сравниваем хеши только тех файлов, которые находятся в исходной директории
            if os.path.exists(archived_file_path):
                integrity_check = verify_integrity(archived_file_path, abs_file_path)
                if integrity_check:
                    logging.info(f"Контрольная сумма файла {rel_file_path} совпадает.")
                else:
                    logging.error(f"ОШИБКА: Контрольная сумма файла {rel_file_path} отличается.")
            else:
                logging.warning(f"Не найдена копия оригинального файла {rel_file_path} для проверки.")

    logging.info("Завершили восстановление данных.")

# Точка входа
if __name__ == '__main__':
    restore_latest_backup()