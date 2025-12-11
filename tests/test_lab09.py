"""
Тестирование лабораторной работы 9.
"""

import os
import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lab09.group import Group, create_sample_data
from src.lab08.models import Student


def test_crud_operations():
    """Тестирование CRUD операций."""
    print("=== Тест 1: Создание и инициализация группы ===")
    
    # Удаляем старый файл если есть
    csv_path = "data/lab09/test_students.csv"
    if Path(csv_path).exists():
        Path(csv_path).unlink()
    
    # Создаем новую группу
    group = Group(csv_path)
    print(f"Создана группа с файлом: {csv_path}")
    print(f"Количество студентов: {len(group.list())}")
    print()
    
    print("=== Тест 2: Добавление студентов ===")
    
    # Добавляем студентов
    students_to_add = [
        Student("Иванов Иван Иванович", "2000-05-15", "SE-01", 4.5),
        Student("Петрова Мария Сергеевна", "2001-08-22", "AI-02", 4.8),
        Student("Сидоров Алексей Петрович", "1999-12-10", "CS-03", 3.7),
        Student("Ковалева Елена Владимировна", "2002-03-30", "DA-04", 4.9),
    ]
    
    for student in students_to_add:
        group.add(student)
        print(f"Добавлен: {student.fio}")
    
    print(f"Всего студентов: {len(group.list())}")
    print()
    
    print("=== Тест 3: Просмотр списка студентов ===")
    all_students = group.list()
    for i, student in enumerate(all_students, 1):
        print(f"{i}. {student.fio}, {student.group}, GPA: {student.gpa}, Возраст: {student.age()}")
    print()
    
    print("=== Тест 4: Поиск студентов ===")
    
    # Поиск по подстроке
    print("Поиск 'ов':")
    found = group.find("ов")
    for student in found:
        print(f"  - {student.fio}")
    
    print("\nПоиск 'Петр':")
    found = group.find("Петр")
    for student in found:
        print(f"  - {student.fio}")
    print()
    
    print("=== Тест 5: Обновление студента ===")
    
    # Обновляем данные студента
    updated = group.update("Иванов Иван Иванович", gpa=4.9, group="SE-02")
    if updated:
        print("Данные Иванова обновлены:")
        ivan = group.find("Иванов")[0]
        print(f"  - {ivan.fio}, {ivan.group}, GPA: {ivan.gpa}")
    print()
    
    print("=== Тест 6: Удаление студента ===")
    
    # Удаляем студента
    removed = group.remove("Сидоров Алексей Петрович")
    if removed:
        print("Сидоров удален")
    
    print(f"Осталось студентов: {len(group.list())}")
    print()
    
    print("=== Тест 7: Статистика группы ===")
    stats = group.stats()
    
    print(f"Общее количество: {stats['count']}")
    print(f"Минимальный GPA: {stats['min_gpa']:.2f}")
    print(f"Максимальный GPA: {stats['max_gpa']:.2f}")
    print(f"Средний GPA: {stats['avg_gpa']:.2f}")
    
    print("\nРаспределение по группам:")
    for group_name, count in stats['groups'].items():
        print(f"  - {group_name}: {count} студентов")
    
    print("\nТоп 5 студентов:")
    for i, student in enumerate(stats['top_5_students'], 1):
        print(f"  {i}. {student['fio']} - {student['gpa']} ({student['group']})")
    
    print("\n=== Тест 8: Обработка ошибок ===")
    
    # Попытка добавить существующего студента
    try:
        group.add(Student("Иванов Иван Иванович", "2000-05-15", "SE-01", 4.5))
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")
    
    # Попытка обновить несуществующего студента
    updated = group.update("Несуществующий Студент", gpa=5.0)
    if not updated:
        print("Студент 'Несуществующий Студент' не найден (ожидаемо)")
    
    return group


def test_sample_data():
    """Тестирование создания примерных данных."""
    print("\n=== Тест создания примерных данных ===")
    
    csv_path = "data/lab09/sample_students.csv"
    
    # Удаляем старый файл если есть
    if Path(csv_path).exists():
        Path(csv_path).unlink()
    
    # Создаем примерные данные
    create_sample_data(csv_path)
    
    # Проверяем
    group = Group(csv_path)
    print(f"Создан файл: {csv_path}")
    print(f"Количество студентов: {len(group.list())}")
    
    # Показываем несколько студентов
    print("\nПервые 3 студента:")
    for student in group.list()[:3]:
        print(f"  - {student.fio}, {student.group}, GPA: {student.gpa}")
    
    return group


def main():
    """Основная функция тестирования."""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ЛАБОРАТОРНОЙ РАБОТЫ 9")
    print("=" * 60)
    
    try:
        # Тестируем CRUD операции
        test_group = test_crud_operations()
        
        # Тестируем создание примерных данных
        sample_group = test_sample_data()
        
        print("\n" + "=" * 60)
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 60)
        
        # Показываем пути к файлам
        print("\nСозданные файлы:")
        print(f"1. {test_group.path.absolute()}")
        print(f"2. {sample_group.path.absolute()}")
        
    except Exception as e:
        print(f"\nОшибка при тестировании: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()