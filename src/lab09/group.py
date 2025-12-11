"""
Модуль group.py содержит класс Group для работы с базой данных студентов в формате CSV.
Реализует CRUD-операции: Create, Read, Update, Delete.
"""

import csv
from pathlib import Path
from typing import List, Optional, Dict, Any
from ..lab08.models import Student


class Group:
    """
    Класс Group представляет группу студентов с возможностью CRUD-операций.
    Данные хранятся в CSV файле.
    
    Attributes:
        path (Path): Путь к CSV файлу с данными студентов
    """
    
    # Заголовок CSV файла
    CSV_HEADER = ["fio", "birthdate", "group", "gpa"]
    
    def __init__(self, storage_path: str) -> None:
        """
        Инициализация группы студентов.
        
        Args:
            storage_path (str): Путь к CSV файлу для хранения данных
            
        Raises:
            ValueError: Если путь некорректен
        """
        self.path = Path(storage_path)
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self) -> None:
        """
        Создает CSV файл с заголовком, если он не существует.
        Если файл существует, проверяет корректность заголовка.
        """
        if not self.path.exists():
            # Создаем директорию если ее нет
            self.path.parent.mkdir(parents=True, exist_ok=True)
            
            # Создаем файл с заголовком
            with open(self.path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
                writer.writeheader()
            
            print(f"Создан новый CSV файл: {self.path}")
        else:
            # Проверяем корректность существующего файла
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    if reader.fieldnames != self.CSV_HEADER:
                        raise ValueError(
                            f"Некорректный заголовок CSV файла. "
                            f"Ожидается: {self.CSV_HEADER}, "
                            f"получено: {reader.fieldnames}"
                        )
            except Exception as e:
                raise ValueError(f"Ошибка чтения CSV файла {self.path}: {str(e)}")
    
    def _read_all_rows(self) -> List[Dict[str, str]]:
        """
        Читает все строки из CSV файла.
        
        Returns:
            List[Dict[str, str]]: Список словарей с данными студентов
            
        Raises:
            ValueError: Если формат файла некорректен
        """
        rows = []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
        except Exception as e:
            raise ValueError(f"Ошибка чтения CSV файла: {str(e)}")
        
        return rows
    
    def _write_all_rows(self, rows: List[Dict[str, str]]) -> None:
        """
        Записывает все строки в CSV файл.
        
        Args:
            rows (List[Dict[str, str]]): Список словарей с данными студентов
        """
        with open(self.path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
            writer.writeheader()
            writer.writerows(rows)
    
    def list(self) -> List[Student]:
        """
        Возвращает список всех студентов.
        
        Returns:
            List[Student]: Список объектов Student
            
        Raises:
            ValueError: Если данные в CSV некорректны
        """
        rows = self._read_all_rows()
        students = []
        
        for i, row in enumerate(rows, start=2):  # Начинаем с 2, т.к. 1 строка - заголовок
            try:
                # Валидируем и преобразуем gpa к float
                row['gpa'] = float(row['gpa'])
                student = Student.from_dict(row)
                students.append(student)
            except Exception as e:
                raise ValueError(
                    f"Ошибка в строке {i} файла {self.path}: {str(e)}. "
                    f"Данные: {row}"
                )
        
        return students
    
    def add(self, student: Student) -> None:
        """
        Добавляет нового студента в базу данных.
        
        Args:
            student (Student): Объект Student для добавления
            
        Raises:
            ValueError: Если студент с таким ФИО уже существует
            TypeError: Если передан не объект Student
        """
        if not isinstance(student, Student):
            raise TypeError(f"Ожидается объект Student, получено: {type(student)}")
        
        # Проверяем, нет ли уже студента с таким ФИО
        existing_students = self.list()
        for existing in existing_students:
            if existing.fio.lower() == student.fio.lower():
                raise ValueError(f"Студент с ФИО '{student.fio}' уже существует")
        
        # Добавляем нового студента
        rows = self._read_all_rows()
        rows.append(student.to_dict())
        self._write_all_rows(rows)
        
        print(f"Добавлен студент: {student.fio}")
    
    def find(self, substr: str, case_sensitive: bool = False) -> List[Student]:
        """
        Ищет студентов по подстроке в ФИО.
        
        Args:
            substr (str): Подстрока для поиска
            case_sensitive (bool): Учитывать регистр при поиске
            
        Returns:
            List[Student]: Список найденных студентов
        """
        if not substr:
            return []
        
        all_students = self.list()
        found_students = []
        
        search_substr = substr if case_sensitive else substr.lower()
        
        for student in all_students:
            student_fio = student.fio if case_sensitive else student.fio.lower()
            if search_substr in student_fio:
                found_students.append(student)
        
        return found_students
    
    def remove(self, fio: str) -> bool:
        """
        Удаляет студента по ФИО.
        
        Args:
            fio (str): ФИО студента для удаления
            
        Returns:
            bool: True если студент был удален, False если не найден
            
        Raises:
            ValueError: Если передана пустая строка
        """
        if not fio:
            raise ValueError("ФИО не может быть пустой строкой")
        
        rows = self._read_all_rows()
        initial_count = len(rows)
        
        # Фильтруем строки, оставляя только тех, у кого ФИО не совпадает
        rows = [row for row in rows if row['fio'].lower() != fio.lower()]
        
        if len(rows) < initial_count:
            self._write_all_rows(rows)
            print(f"Удален студент: {fio}")
            return True
        else:
            print(f"Студент с ФИО '{fio}' не найден")
            return False
    
    def update(self, fio: str, **fields) -> bool:
        """
        Обновляет поля существующего студента.
        
        Args:
            fio (str): ФИО студента для обновления
            **fields: Поля для обновления (fio, birthdate, group, gpa)
            
        Returns:
            bool: True если студент был обновлен, False если не найден
            
        Raises:
            ValueError: Если переданы некорректные поля
        """
        if not fio:
            raise ValueError("ФИО не может быть пустой строкой")
        
        # Проверяем, что все поля корректны
        valid_fields = {'fio', 'birthdate', 'group', 'gpa'}
        invalid_fields = set(fields.keys()) - valid_fields
        if invalid_fields:
            raise ValueError(f"Некорректные поля: {invalid_fields}. Допустимые поля: {valid_fields}")
        
        rows = self._read_all_rows()
        updated = False
        
        for i, row in enumerate(rows):
            if row['fio'].lower() == fio.lower():
                # Обновляем поля
                for key, value in fields.items():
                    rows[i][key] = str(value)  # Все значения храним как строки
                
                # Проверяем корректность обновленных данных
                try:
                    # Временная валидация
                    temp_row = rows[i].copy()
                    temp_row['gpa'] = float(temp_row['gpa'])
                    Student.from_dict(temp_row)
                    
                    updated = True
                    print(f"Обновлен студент: {fio}")
                    break
                except Exception as e:
                    raise ValueError(f"Некорректные данные при обновлении: {str(e)}")
        
        if updated:
            self._write_all_rows(rows)
        
        return updated
    
    def stats(self) -> Dict[str, Any]:
        """
        Возвращает статистику по группе.
        
        Returns:
            Dict[str, Any]: Словарь со статистикой
            
        Структура:
        {
            "count": общее количество студентов,
            "min_gpa": минимальный GPA,
            "max_gpa": максимальный GPA,
            "avg_gpa": средний GPA,
            "groups": распределение по группам,
            "top_5_students": топ 5 студентов по GPA
        }
        """
        students = self.list()
        
        if not students:
            return {
                "count": 0,
                "min_gpa": None,
                "max_gpa": None,
                "avg_gpa": None,
                "groups": {},
                "top_5_students": []
            }
        
        # Основная статистика
        gpa_values = [student.gpa for student in students]
        
        # Распределение по группам
        groups_dist = {}
        for student in students:
            group = student.group
            groups_dist[group] = groups_dist.get(group, 0) + 1
        
        # Топ 5 студентов по GPA
        sorted_students = sorted(students, key=lambda s: s.gpa, reverse=True)
        top_5 = [
            {"fio": s.fio, "gpa": s.gpa, "group": s.group}
            for s in sorted_students[:5]
        ]
        
        return {
            "count": len(students),
            "min_gpa": min(gpa_values),
            "max_gpa": max(gpa_values),
            "avg_gpa": sum(gpa_values) / len(gpa_values),
            "groups": groups_dist,
            "top_5_students": top_5
        }
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление группы.
        
        Returns:
            str: Информация о группе
        """
        students = self.list()
        return (f"Группа (файл: {self.path})\n"
                f"Количество студентов: {len(students)}\n"
                f"Путь к данным: {self.path.absolute()}")


# Функция для быстрого создания тестовых данных
def create_sample_data(csv_path: str) -> None:
    """
    Создает CSV файл с тестовыми данными студентов.
    
    Args:
        csv_path (str): Путь к CSV файлу
    """
    sample_students = [
        Student("Иванов Иван Иванович", "2000-05-15", "SE-01", 4.5),
        Student("Петрова Мария Сергеевна", "2001-08-22", "AI-02", 4.8),
        Student("Сидоров Алексей Петрович", "1999-12-10", "CS-03", 3.7),
        Student("Ковалева Елена Владимировна", "2002-03-30", "DA-04", 4.9),
        Student("Новиков Дмитрий Александрович", "2000-11-05", "SE-01", 4.2),
        Student("Смирнова Ольга Игоревна", "2001-07-18", "AI-02", 4.6),
        Student("Кузнецов Андрей Сергеевич", "1998-09-25", "CS-03", 3.9),
        Student("Васильева Анна Петровна", "2003-01-14", "DA-04", 4.7),
    ]
    
    group = Group(csv_path)
    for student in sample_students:
        try:
            group.add(student)
        except ValueError as e:
            print(f"Пропущен студент {student.fio}: {e}")


if __name__ == "__main__":
    # Пример использования
    print("=== Тестирование класса Group ===")
    
    # Создаем тестовую группу
    csv_path = "data/lab09/students.csv"
    group = Group(csv_path)
    
    # Выводим информацию о группе
    print(group)
    print()
    
    # Показываем список студентов
    print("Список всех студентов:")
    for student in group.list():
        print(f"  - {student.fio}, {student.group}, GPA: {student.gpa}")
    print()
    
    # Тестируем поиск
    print("Поиск студентов с 'Иванов':")
    found = group.find("Иванов")
    for student in found:
        print(f"  - {student.fio}")
    
    # Тестируем статистику
    print("\nСтатистика группы:")
    stats = group.stats()
    for key, value in stats.items():
        if key == "top_5_students":
            print(f"  {key}:")
            for s in value:
                print(f"    - {s['fio']} (GPA: {s['gpa']})")
        elif key == "groups":
            print(f"  {key}:")
            for g, count in value.items():
                print(f"    - {g}: {count} студентов")
        else:
            print(f"  {key}: {value}")