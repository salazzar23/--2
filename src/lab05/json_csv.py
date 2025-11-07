# src/lab05/json_csv.py
import json
import csv
from pathlib import Path
from typing import List, Dict

def json_to_csv(json_path: Path, csv_path: Path) -> None:
    """Преобразует JSON-файл (список словарей) в CSV"""
    if not json_path.exists():
        raise FileNotFoundError(f"Файл JSON '{json_path}' не найден")
    
    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)
    
    if not data or not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        raise ValueError("Пустой JSON или некорректная структура")
    
    # Определяем заголовки
    headers = list(data[0].keys())
    
    csv_path.parent.mkdir(parents=True, exist_ok=True)  # создаём папки
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"✅ JSON -> CSV сохранён: {csv_path}")


def csv_to_json(csv_path: Path, json_path: Path) -> None:
    """Преобразует CSV в JSON (список словарей)"""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV-файл '{csv_path}' не найден")
    
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        raise ValueError("CSV пуст или нет заголовка")
    
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"✅ CSV -> JSON сохранён: {json_path}")


if __name__ == "__main__":
    # Пути относительно директории src/lab05
    BASE_DIR = Path(__file__).parent.parent  # поднимаемся к python_lab/
    json_path = BASE_DIR / "data/samples/people.json"
    csv_path = BASE_DIR / "data/out/people.csv"

    print("=== JSON -> CSV ===")
    try:
        json_to_csv(json_path, csv_path)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n=== CSV -> JSON ===")
    try:
        csv_to_json(csv_path, json_path.parent / "people_from_csv.json")
    except Exception as e:
        print(f"❌ Ошибка: {e}")