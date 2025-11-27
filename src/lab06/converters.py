# Импорт необходимых модулей
import json  # Для работы с JSON форматом
import csv   # Для работы с CSV форматом
import os    # Для работы с файловой системой
# Импорт функции валидации файла
from .utils import validate_file_exists

# Функция конвертации JSON в CSV
def json_to_csv(input_file, output_file):
    """Конвертация JSON в CSV"""
    # Проверка существования входного файла
    validate_file_exists(input_file)
    
    # Открытие JSON файла для чтения
    with open(input_file, 'r', encoding='utf-8') as f:
        # Загрузка данных из JSON файла
        data = json.load(f)
    
    # Проверка что данные являются списком словарей
    if isinstance(data, list) and len(data) > 0:
        # Получение названий полей из первого элемента
        fieldnames = data[0].keys()
        # Открытие CSV файла для записи
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # Создание DictWriter для записи словарей в CSV
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            # Запись заголовка CSV
            writer.writeheader()
            # Запись всех строк данных
            writer.writerows(data)
    else:
        # Выбрасывание ошибки если JSON неверного формата
        raise ValueError("JSON должен содержать список словарей")

# Функция конвертации CSV в JSON
def csv_to_json(input_file, output_file):
    """Конвертация CSV в JSON"""
    # Проверка существования входного файла
    validate_file_exists(input_file)
    
    # Создание пустого списка для данных
    data = []
    # Открытие CSV файла для чтения
    with open(input_file, 'r', encoding='utf-8') as f:
        # Создание DictReader для чтения CSV как словарей
        reader = csv.DictReader(f)
        # Чтение каждой строки CSV
        for row in reader:
            # Добавление строки в список данных
            data.append(row)
    
    # Открытие JSON файла для записи
    with open(output_file, 'w', encoding='utf-8') as f:
        # Запись данных в JSON с форматированием
        json.dump(data, f, ensure_ascii=False, indent=2)

# Функция конвертации CSV в XLSX (эмуляция)
def csv_to_xlsx(input_file, output_file):
    """Конвертация CSV в XLSX (используя только стандартные библиотеки)"""
    # Проверка существования входного файла
    validate_file_exists(input_file)
    
    # Создание пустого списка для данных
    data = []
    # Открытие CSV файла для чтения
    with open(input_file, 'r', encoding='utf-8') as f:
        # Создание reader для чтения CSV
        reader = csv.reader(f)
        # Чтение каждой строки CSV
        for row in reader:
            # Добавление строки в список данных
            data.append(row)
    
    # Эмуляция XLSX файла (в реальном проекте использовалась бы библиотека)
    # Открытие выходного файла для записи
    with open(output_file, 'w', encoding='utf-8') as f:
        # Запись заголовка эмуляции
        f.write("XLSX Emulation - CSV data:\n")
        # Запись разделительной линии
        f.write("=" * 50 + "\n")
        # Запись каждой строки данных с разделителями
        for row in data:
            f.write(" | ".join(row) + "\n")
    
    # Вывод информационного сообщения
    print(f"Внимание: В режиме без внешних библиотек создан текстовый файл")
    # Вывод пояснения о ограничениях
    print(f"В реальном проекте здесь был бы настоящий XLSX файл")