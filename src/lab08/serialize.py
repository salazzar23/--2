"""
Модуль serialize.py содержит функции для сериализации
и десериализации объектов Student в формат JSON.
"""

import json
from typing import List
from pathlib import Path
from .models import Student


def students_to_json(students: List[Student], path: str) -> None:
    """
    Сериализует список объектов Student в JSON файл.
    
    Args:
        students (List[Student]): список объектов Student для сериализации
        path (str): путь к файлу для сохранения
        
    Raises:
        TypeError: если передан не список или элементы не являются Student
        IOError: если произошла ошибка при записи файла
    """
    # Проверяем, что передан список
    if not isinstance(students, list):
        raise TypeError("Функция ожидает список объектов Student")
    
    # Проверяем, что все элементы списка являются объектами Student
    for i, student in enumerate(students):
        if not isinstance(student, Student):
            raise TypeError(f"Элемент с индексом {i} не является объектом Student")
    
    try:
        # Преобразуем каждый объект Student в словарь
        data = [student.to_dict() for student in students]
        
        # Создаем директорию, если она не существует
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Записываем данные в JSON файл
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Данные успешно сохранены в файл: {path}")
        print(f"Сохранено записей: {len(students)}")
        
    except Exception as e:
        raise IOError(f"Ошибка при записи файла {path}: {str(e)}")


def students_from_json(path: str) -> List[Student]:
    """
    Десериализует JSON файл в список объектов Student.
    
    Args:
        path (str): путь к JSON файлу
        
    Returns:
        List[Student]: список объектов Student
        
    Raises:
        FileNotFoundError: если файл не существует
        json.JSONDecodeError: если файл содержит некорректный JSON
        ValueError: если данные в файле некорректны
    """
    try:
        # Читаем JSON файл
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Проверяем, что данные представляют собой список
        if not isinstance(data, list):
            raise ValueError("JSON файл должен содержать список")
        
        # Создаем объекты Student из данных
        students = []
        errors = []
        
        for i, item in enumerate(data):
            try:
                student = Student.from_dict(item)
                students.append(student)
            except Exception as e:
                errors.append(f"Запись {i}: {str(e)}")
        
        # Если были ошибки, выводим их
        if errors:
            print("При чтении файла возникли следующие ошибки:")
            for error in errors:
                print(f"  - {error}")
        
        print(f"Успешно загружено записей: {len(students)} из {len(data)}")
        
        return students
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Некорректный JSON в файле {path}", e.doc, e.pos)


# Пример использования функций (для тестирования)
if __name__ == "__main__":
    try:
        # Создаем тестовые данные
        test_students = [
            Student(
                fio="Петров Петр Петрович",
                birthdate="2001-03-20",
                group="SE-01",
                gpa=4.2
            ),
            Student(
                fio="Сидорова Анна Владимировна",
                birthdate="2002-07-10",
                group="AI-02",
                gpa=4.8
            ),
            Student(
                fio="Козлов Дмитрий Сергеевич",
                birthdate="2000-11-30",
                group="CS-03",
                gpa=3.9
            )
        ]
        
        # Тестируем сериализацию
        output_path = "data/lab08/students_output.json"
        students_to_json(test_students, output_path)
        
        # Тестируем десериализацию
        loaded_students = students_from_json(output_path)
        
        print("\nЗагруженные студенты:")
        for student in loaded_students:
            print("-" * 40)
            print(student)
            
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")