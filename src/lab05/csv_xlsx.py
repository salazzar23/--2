# src/lab05/csv_xlsx.py
import csv
from pathlib import Path
from openpyxl import Workbook

def csv_to_xlsx(csv_path: Path, xlsx_path: Path) -> None:
    """Конвертирует CSV в XLSX"""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV-файл '{csv_path}' не найден")
    
    xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    with csv_path.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            ws.append(row)

    # Автоширина колонок
    for col in ws.columns:
        max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        max_len = max(max_len, 8)
        ws.column_dimensions[col[0].column_letter].width = max_len

    wb.save(xlsx_path)
    print(f"✅ CSV -> XLSX сохранён: {xlsx_path}")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent
    csv_path = BASE_DIR / "data/samples/cities.csv"
    xlsx_path = BASE_DIR / "data/out/cities.xlsx"

    try:
        csv_to_xlsx(csv_path, xlsx_path)
    except Exception as e:
        print(f"❌ Ошибка: {e}")