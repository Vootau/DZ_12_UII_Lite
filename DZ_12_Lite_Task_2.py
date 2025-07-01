import os
import chardet
import logging


# Настройка логирования
LOGS_DIR = "main_dir/logs/"
log_filename = os.path.join(LOGS_DIR, "processing.log")

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Директории для сырых и обработанных данных
RAW_DIR = 'main_dir/data/raw/'
PROCESSED_DIR = 'main_dir/data/processed/'

CODECS = ["cp1252", "cp437", "utf-16be", "utf-16", "windows-1251"]  # Расширенный набор кодировок


def find_correct_codec(file_path):
    """
    Перебирает известные кодировки и находит первую работающую для данного файла.
    Возвращает корректную кодировку или None, если никакая не подошла.
    """
    encodings_to_try = []

    # Первоначальная проверка с помощью chardet
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        detection_result = chardet.detect(raw_data)
        proposed_encoding = detection_result.get('encoding')
        encodings_to_try.append(proposed_encoding)

    # Добавляем остальные тестируемые кодировки
    encodings_to_try.extend(CODECS)

    for codec in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=codec) as file:
                file.read()  # Просто читаем весь файл, проверяя возможность
            logging.info(f"Успешно определена кодировка '{codec}' для файла '{file_path}'.")
            return codec
        except UnicodeDecodeError:
            logging.debug(f"Кодировка '{codec}' не подошла для файла '{file_path}'.")
            continue

    logging.error(f"Ни одна из кодировок не подошла для файла '{file_path}'.")
    return None


def process_file(file_name):
    # Полный путь к файлу в исходной директории
    input_file_path = os.path.join(RAW_DIR, file_name)

    # Определение кодировки файла
    encoding = find_correct_codec(input_file_path)

    # Чтение файла с определенной кодировкой
    with open(input_file_path, 'r', encoding=encoding) as infile:
        content = infile.read()

    # Изменение регистра букв
    transformed_content = content.swapcase()

    # Имя нового файла с суффиксом _processed
    output_file_name = f"processed_{file_name}"
    output_file_path = os.path.join(PROCESSED_DIR, output_file_name)

    # Запись обработанного файла
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(transformed_content)


if __name__ == "__main__":
    # Список всех файлов в директории RAW_DIR
    files = os.listdir(RAW_DIR)
    if len(files) == 0:
        logging.warning("Нет файлов для обработки в директории %s.", RAW_DIR)
        print("Нет файлов для обработки.")
    else:
        for file in files:
            print(f'Обрабатываю файл {file}')
            try:
                process_file(file)
            except Exception as e:
                logging.error(f"Ошибка при обработке файла {file}: {e}")
                print(f"Произошла ошибка при обработке файла {file}: {e}")