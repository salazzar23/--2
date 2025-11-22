"""
Вспомогательные функции для работы с файлами
"""
import json
import csv
from pathlib import Path


def read_json_file(file_path: str) -> list:
    """
    Читает JSON файл и возвращает данные
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    
    if path.suffix.lower() != '.json':
        raise ValueError(f"Неверный тип файла: ожидается .json, получен {path.suffix}")
    
    with path.open('r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")
    
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список объектов")
    
    if len(data) == 0:
        raise ValueError("Пустой JSON")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("JSON должен содержать список словарей")
    
    return data


def read_csv_file(file_path: str) -> tuple[list, list]:
    """
    Читает CSV файл и возвращает заголовки и данные
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    
    if path.suffix.lower() != '.csv':
        raise ValueError(f"Неверный тип файла: ожидается .csv, получен {path.suffix}")
    
    with path.open('r', encoding='utf-8', newline='') as f:
        # Автоопределение разделителя
        sample = f.read(1024)
        f.seek(0)
        
        try:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            has_header = sniffer.has_header(sample)
        except csv.Error:
            dialect = csv.excel
            has_header = True
        
        if not has_header:
            raise ValueError("CSV файл должен содержать заголовок")
        
        reader = csv.DictReader(f, dialect=dialect)
        headers = reader.fieldnames
        
        if not headers:
            raise ValueError("CSV файл не содержит заголовков")
        
        data = list(reader)
    
    if len(data) == 0:
        raise ValueError("Пустой CSV файл")
    
    return headers, data


def ensure_output_directory(file_path: str) -> None:
    """
    Создает директорию для выходного файла если она не существует
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)