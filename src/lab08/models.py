"""
Модуль models.py содержит определение класса Student с использованием @dataclass.
Класс включает валидацию данных, методы для работы с объектами и сериализации.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import Optional, Dict, Any
import re


@dataclass
class Student:
    """
    Класс Student представляет студента с основными атрибутами:
    - ФИО
    - Дата рождения
    - Группа
    - Средний балл
    
    Используется декоратор @dataclass для автоматической генерации
    методов __init__, __repr__, __eq__ и других.
    """
    
    # Поля класса с аннотациями типов
    fio: str           # ФИО студента
    birthdate: str     # Дата рождения в формате YYYY-MM-DD
    group: str         # Учебная группа
    gpa: float         # Средний балл (0-5)
    
    def __post_init__(self):
        """
        Метод __post_init__ вызывается автоматически после __init__.
        Используется для валидации данных при создании объекта.
        """
        self._validate_birthdate()
        self._validate_gpa()
    
    def _validate_birthdate(self) -> None:
        """
        Валидация формата даты рождения.
        Проверяет, что дата соответствует формату YYYY-MM-DD
        и является корректной датой.
        
        Raises:
            ValueError: если формат даты некорректен
        """
        # Регулярное выражение для проверки формата YYYY-MM-DD
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        
        if not re.match(date_pattern, self.birthdate):
            raise ValueError(f"Неверный формат даты: {self.birthdate}. "
                           f"Ожидается формат: YYYY-MM-DD")
        
        try:
            # Пробуем преобразовать строку в объект datetime
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Некорректная дата: {self.birthdate}. "
                           f"Ошибка: {str(e)}")
    
    def _validate_gpa(self) -> None:
        """
        Валидация среднего балла.
        Проверяет, что GPA находится в диапазоне от 0 до 5.
        
        Raises:
            ValueError: если GPA выходит за допустимые пределы
        """
        if not (0 <= self.gpa <= 5):
            raise ValueError(f"Средний балл должен быть в диапазоне от 0 до 5. "
                           f"Получено: {self.gpa}")
    
    def age(self) -> int:
        """
        Вычисляет текущий возраст студента в полных годах
        на основе даты рождения.
        
        Returns:
            int: количество полных лет студента
        """
        # Преобразуем строку с датой рождения в объект date
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        
        # Получаем текущую дату
        today = date.today()
        
        # Вычисляем возраст
        age = today.year - birth_date.year
        
        # Корректируем возраст, если день рождения в этом году еще не наступил
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует объект Student в словарь.
        Этот метод используется для преобразования объекта
        в формат, пригодный для сохранения в JSON.
        
        Returns:
            Dict[str, Any]: словарь с данными студента
        """
        # Используем стандартную функцию asdict из dataclasses
        # Она автоматически преобразует все поля dataclass в словарь
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """
        Создает объект Student из словаря (десериализация).
        Это классовый метод, который можно вызывать без создания экземпляра.
        
        Args:
            data (Dict[str, Any]): словарь с данными студента
            
        Returns:
            Student: новый объект Student
            
        Raises:
            ValueError: если в словаре отсутствуют обязательные поля
        """
        # Проверяем наличие всех обязательных полей
        required_fields = ['fio', 'birthdate', 'group', 'gpa']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")
        
        # Создаем и возвращаем новый объект Student
        # Валидация произойдет автоматически в __post_init__
        return cls(
            fio=data['fio'],
            birthdate=data['birthdate'],
            group=data['group'],
            gpa=float(data['gpa'])  # Преобразуем к float на всякий случай
        )
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Student.
        Используется при выводе с помощью print() или str().
        
        Returns:
            str: форматированная строка с информацией о студенте
        """
        return (f"Студент: {self.fio}\n"
                f"Группа: {self.group}\n"
                f"Дата рождения: {self.birthdate} (Возраст: {self.age()} лет)\n"
                f"Средний балл: {self.gpa:.2f}")


# Пример использования класса (для тестирования)
if __name__ == "__main__":
    # Создаем объект Student
    student = Student(
        fio="Иванов Иван Иванович",
        birthdate="2000-05-15",
        group="SE-01",
        gpa=4.5
    )
    
    print("Создан объект Student:")
    print(student)
    print()
    
    # Тестируем преобразование в словарь
    student_dict = student.to_dict()
    print("Объект преобразован в словарь:")
    print(student_dict)
    print()
    
    # Тестируем создание из словаря
    new_student = Student.from_dict(student_dict)
    print("Создан новый объект из словаря:")
    print(new_student)