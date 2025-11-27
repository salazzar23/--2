# Импорт необходимых модулей
import argparse  # Для парсинга аргументов командной строки
import sys       # Для работы с системными функциями
import os        # Для работы с файловой системой
# Импорт модулей конвертеров и утилит
from . import converters  # Модуль для конвертации файлов
from . import utils       # Модуль с вспомогательными функциями

# Основная функция приложения
def main():
    # Создание основного парсера аргументов
    parser = argparse.ArgumentParser(description="Утилита для работы с файлами")
    # Добавление подпарсеров для различных команд
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    
    # Команда cat - вывод содержимого файла
    p1 = subparsers.add_parser("cat", help="Вывод содержимого файла с номерами строк")
    # Добавление аргумента для входного файла
    p1.add_argument("--input", dest="input", required=True, help="Входной файл")
    # Добавление флага для показа номеров строк
    p1.add_argument("-n", "--numbers", action="store_true", help="Показать номера строк")
    
    # Команда stats - статистика по словам
    p2 = subparsers.add_parser("stats", help="Статистика по словам в файле")
    # Добавление аргумента для входного файла
    p2.add_argument("--input", dest="input", required=True, help="Входной файл")
    # Добавление аргумента для количества топ-слов
    p2.add_argument("--top", type=int, default=10, help="Количество топ-слов")
    
    # Команда json2csv - конвертация из JSON в CSV
    p3 = subparsers.add_parser("json2csv", help="Конвертация JSON в CSV")
    # Добавление аргумента для входного JSON файла
    p3.add_argument("--input", dest="input", required=True, help="Входной JSON файл")
    # Добавление аргумента для выходного CSV файла
    p3.add_argument("--out", dest="output", required=True, help="Выходной CSV файл")
    
    # Команда csv2json - конвертация из CSV в JSON
    p4 = subparsers.add_parser("csv2json", help="Конвертация CSV в JSON")
    # Добавление аргумента для входного CSV файла
    p4.add_argument("--input", dest="input", required=True, help="Входной CSV файл")
    # Добавление аргумента для выходного JSON файла
    p4.add_argument("--out", dest="output", required=True, help="Выходной JSON файл")
    
    # Команда csv2xlsx - конвертация из CSV в XLSX
    p5 = subparsers.add_parser("csv2xlsx", help="Конвертация CSV в XLSX")
    # Добавление аргумента для входного CSV файла
    p5.add_argument("--input", dest="input", required=True, help="Входной CSV файл")
    # Добавление аргумента для выходного XLSX файла
    p5.add_argument("--out", dest="output", required=True, help="Выходной XLSX файл")
    
    # Парсинг аргументов командной строки
    args = parser.parse_args()
    
    # Обработка команд с обработкой исключений
    try:
        # Если команда cat - выводим содержимое файла
        if args.command == "cat":
            # Вызов функции вывода файла с номерами строк
            utils.cat_file(args.input, args.numbers)
        # Если команда stats - показываем статистику
        elif args.command == "stats":
            # Вызов функции показа статистики по словам
            utils.show_stats(args.input, args.top)
        # Если команда json2csv - конвертируем JSON в CSV
        elif args.command == "json2csv":
            # Вызов функции конвертации JSON в CSV
            converters.json_to_csv(args.input, args.output)
        # Если команда csv2json - конвертируем CSV в JSON
        elif args.command == "csv2json":
            # Вызов функции конвертации CSV в JSON
            converters.csv_to_json(args.input, args.output)
        # Если команда csv2xlsx - конвертируем CSV в XLSX
        elif args.command == "csv2xlsx":
            # Вызов функции конвертации CSV в XLSX
            converters.csv_to_xlsx(args.input, args.output)
        # Если команда не указана - показываем справку
        else:
            # Вывод справки по использованию
            parser.print_help()
    # Обработка ошибки отсутствия файла
    except FileNotFoundError as e:
        # Вывод сообщения об ошибке в stderr
        print(f"Ошибка: Файл не найден - {e}", file=sys.stderr)
        # Завершение программы с кодом ошибки 1
        sys.exit(1)
    # Обработка всех остальных исключений
    except Exception as e:
        # Вывод общего сообщения об ошибке
        print(f"Ошибка: {e}", file=sys.stderr)
        # Завершение программы с кодом ошибки 1
        sys.exit(1)