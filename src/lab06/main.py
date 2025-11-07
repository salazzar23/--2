import argparse
import sys
from pathlib import Path

# === Добавляем путь, чтобы Python видел lab05 ===
sys.path.append(str(Path(__file__).resolve().parents[1]))

from lab05.json_csv import json_to_csv, csv_to_json
from lab05.csv_xlsx import csv_to_xlsx


def main():
    parser = argparse.ArgumentParser(description="Инструмент для работы с форматами данных")
    subparsers = parser.add_subparsers(dest="command")

    # --- JSON → CSV ---
    json2csv_parser = subparsers.add_parser("json2csv", help="Преобразовать JSON → CSV")
    json2csv_parser.add_argument("--in", dest="input", required=True, help="Входной JSON-файл")
    json2csv_parser.add_argument("--out", dest="output", required=True, help="Выходной CSV-файл")

    # --- CSV → JSON ---
    csv2json_parser = subparsers.add_parser("csv2json", help="Преобразовать CSV → JSON")
    csv2json_parser.add_argument("--in", dest="input", required=True, help="Входной CSV-файл")
    csv2json_parser.add_argument("--out", dest="output", required=True, help="Выходной JSON-файл")

    # --- CSV → XLSX ---
    csv2xlsx_parser = subparsers.add_parser("csv2xlsx", help="Преобразовать CSV → XLSX")
    csv2xlsx_parser.add_argument("--in", dest="input", required=True, help="Входной CSV-файл")
    csv2xlsx_parser.add_argument("--out", dest="output", required=True, help="Выходной XLSX-файл")

    args = parser.parse_args()

    if args.command == "json2csv":
        json_to_csv(args.input, args.output)
    elif args.command == "csv2json":
        csv_to_json(args.input, args.output)
    elif args.command == "csv2xlsx":
        csv_to_xlsx(args.input, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()