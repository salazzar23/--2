# Импорт необходимых модулей
import os        # Для работы с файловой системой
import re        # Для регулярных выражений
# Импорт Counter для подсчета частоты элементов
from collections import Counter

# Функция проверки существования файла
def validate_file_exists(filepath):
    """Проверка существования файла"""
    # Проверка существования файла по пути
    if not os.path.exists(filepath):
        # Выбрасывание исключения если файл не найден
        raise FileNotFoundError(filepath)

# Функция чтения файла построчно
def read_file_lines(filepath):
    """Чтение файла построчно с валидацией"""
    # Проверка что файл существует
    validate_file_exists(filepath)
    # Открытие файла для чтения с UTF-8 кодировкой
    with open(filepath, 'r', encoding='utf-8') as f:
        # Чтение всех строк файла и возврат
        return f.readlines()

# Функция вывода содержимого файла (аналог cat)
def cat_file(filepath, show_numbers=False):
    """Вывод содержимого файла с номерами строк"""
    # Чтение всех строк файла
    lines = read_file_lines(filepath)
    # Перебор строк с нумерацией начиная с 1
    for i, line in enumerate(lines, 1):
        # Если нужно показывать номера строк
        if show_numbers:
            # Вывод номера строки и содержимого с табуляцией
            print(f"{i:6d}\t{line.rstrip()}")
        else:
            # Вывод только содержимого строки
            print(line.rstrip())

# Функция извлечения слов из текста
def extract_words(text):
    """Извлечение слов из текста"""
    # Поиск всех слов (кириллических и латинских) в нижнем регистре
    words = re.findall(r'\b[a-zA-Zа-яА-Я]+\b', text.lower())
    # Возврат списка найденных слов
    return words

# Функция показа статистики по словам
def show_stats(filepath, top_n=10):
    """Показать статистику по словам в файле"""
    # Проверка существования файла
    validate_file_exists(filepath)
    
    # Открытие файла для чтения
    with open(filepath, 'r', encoding='utf-8') as f:
        # Чтение всего содержимого файла
        text = f.read()
    
    # Извлечение слов из текста
    words = extract_words(text)
    # Подсчет частоты слов с помощью Counter
    word_counts = Counter(words)
    
    # Вывод общей статистики
    print(f"Всего слов: {len(words)}")
    # Вывод количества уникальных слов
    print(f"Уникальных слов: {len(word_counts)}")
    # Вывод заголовка для топ-слов
    print(f"\nТоп-{top_n} самых частых слов:")
    # Вывод разделительной линии
    print("-" * 30)
    
    # Перебор самых частых слов
    for word, count in word_counts.most_common(top_n):
        # Вывод слова и количества его вхождений с форматированием
        print(f"{word:<20} {count:>4}")