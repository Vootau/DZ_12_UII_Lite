import json
import os
from datetime import datetime


class TaskReportGenerator:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name, difficulties=None, execution_time=0.0, conclusions_and_improvements=None):
        """
        Добавляет задание в отчет.

        :param task_name: Название задания
        :param difficulties: Список трудностей и путей их преодоления
        :param execution_time: Время выполнения задания в секундах
        :param conclusions_and_improvements: Выводы и рекомендации по улучшению
        """
        if not isinstance(difficulties, list):
            difficulties = ["Нет трудностей"]

        if not isinstance(conclusions_and_improvements, str):
            conclusions_and_improvements = "Нет выводов и предложений"

        task_report = {
            'task_name': task_name,
            'difficulties': difficulties,
            'execution_time': f"{execution_time:.2f} секунд",
            'conclusions_and_improvements': conclusions_and_improvements
        }
        self.tasks.append(task_report)

    def generate_json_report(self, filename="report.json"):
        """Генерация отчета в формате JSON"""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump({'tasks': self.tasks}, file, ensure_ascii=False, indent=4)


# Пример использования класса
if __name__ == "__main__":
    # переходим в директорию исполнения текущего скрипта
    base_dir = os.path.dirname(os.path.abspath(__file__))
    new_dir = os.path.join(base_dir, "main_dir")
    os.chdir(new_dir)


    # Создаем объект генератора отчётов
    generator = TaskReportGenerator()

    start_time = datetime.now()  # Начало первого задания
    generator.add_task(
        task_name="Задание 1: Управление проектной структурой и файловой системой",
        difficulties=["Проблемы с созданием и сохранением заданных папок в нужном месте. Проблема сохранения логирования."],
        execution_time=(datetime.now() - start_time).total_seconds(),
        conclusions_and_improvements="Создание всей структуры папок по заданию в единой корневой директории."
    )

    start_time = datetime.now()  # Начало второго задания
    generator.add_task(
        task_name="Задание 2: Чтение, преобразование и сериализация данных",
        difficulties=["Ошибки в коде, проблемы с указанием директории."],
        execution_time=(datetime.now() - start_time).total_seconds(),
        conclusions_and_improvements="Внедрение единой системы логирования и объявление констант с указанием пути к файлам."
    )

    start_time = datetime.now()  # Начало третьего задания
    generator.add_task(
        task_name="Задание 3: Работа с резервными копиями и восстановлением данных",
        difficulties=["Проблемы с реализацией проверки контрольных сумм при валидации"],
        execution_time=(datetime.now() - start_time).total_seconds(),
        conclusions_and_improvements="Решено с использованием стандартных библиотек путем простого перебора."
    )


    start_time = datetime.now()  # Начало четвертого задания
    generator.add_task(
        task_name="Задание 4: Дополнительные задачи с сериализацией и JSON Schema",
        difficulties=["Все те же проблемы при выполнении и сохранении в нужных директориях"],
        execution_time=(datetime.now() - start_time).total_seconds(),
        conclusions_and_improvements="Необходимо учить матчасть((((("
    )

    start_time = datetime.now()  # Начало пятого задания
    generator.add_task(
        task_name="Задание 5: Отчёт и анализ проделанной работы",
        difficulties=["Вообще непонятно как делать отчет, если задачи уже выполнены. Необходимо было сначала создавать генератор отчетов для учета времени работы над задачей."],
        execution_time=(datetime.now() - start_time).total_seconds(),
        conclusions_and_improvements="Выполнять следующие ДЗ не по порядку, а после составления плана по итогам анализа всего задания целиком"
    )

    # Генерируем отчет в разных форматах
    generator.generate_json_report("report.json")
