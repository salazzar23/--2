"""
Реализация базовых структур данных: Stack (стек) и Queue (очередь).
"""

from collections import deque
from typing import Any, Optional


class Stack:
    """
    Структура данных "Стек" (LIFO - Last In, First Out).
    Реализована на основе встроенного списка Python.
    
    Особенности:
    - push(): O(1) - добавление элемента на вершину стека
    - pop(): O(1) - удаление элемента с вершины стека
    - peek(): O(1) - просмотр вершины стека
    """
    
    def __init__(self) -> None:
        """Инициализация пустого стека."""
        self._data: list[Any] = []
    
    def push(self, item: Any) -> None:
        """
        Добавить элемент на вершину стека.
        
        Args:
            item: Элемент для добавления
        
        Time Complexity: O(1)
        """
        self._data.append(item)
    
    def pop(self) -> Any:
        """
        Удалить и вернуть элемент с вершины стека.
        
        Returns:
            Элемент с вершины стека
        
        Raises:
            IndexError: Если стек пуст
        
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Невозможно извлечь элемент из пустого стека")
        return self._data.pop()
    
    def peek(self) -> Optional[Any]:
        """
        Вернуть элемент с вершины стека без удаления.
        
        Returns:
            Элемент с вершины стека или None, если стек пуст
        
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self._data[-1]
    
    def is_empty(self) -> bool:
        """
        Проверить, пуст ли стек.
        
        Returns:
            True если стек пуст, иначе False
        
        Time Complexity: O(1)
        """
        return len(self._data) == 0
    
    def __len__(self) -> int:
        """
        Количество элементов в стеке.
        
        Returns:
            Количество элементов
        
        Time Complexity: O(1)
        """
        return len(self._data)
    
    def __repr__(self) -> str:
        """
        Строковое представление стека.
        
        Returns:
            Строка вида Stack([элементы])
        """
        return f"Stack({self._data})"
    
    def __str__(self) -> str:
        """
        Красивое строковое представление стека.
        
        Returns:
            Строка с элементами стека
        """
        return f"Стек (размер: {len(self)}): {self._data}"


class Queue:
    """
    Структура данных "Очередь" (FIFO - First In, First Out).
    Реализована на основе collections.deque для эффективности.
    
    Особенности:
    - enqueue(): O(1) - добавление элемента в конец очереди
    - dequeue(): O(1) - удаление элемента из начала очереди
    - peek(): O(1) - просмотр первого элемента очереди
    """
    
    def __init__(self) -> None:
        """Инициализация пустой очереди."""
        self._data: deque[Any] = deque()
    
    def enqueue(self, item: Any) -> None:
        """
        Добавить элемент в конец очереди.
        
        Args:
            item: Элемент для добавления
        
        Time Complexity: O(1)
        """
        self._data.append(item)
    
    def dequeue(self) -> Any:
        """
        Удалить и вернуть элемент из начала очереди.
        
        Returns:
            Первый элемент очереди
        
        Raises:
            IndexError: Если очередь пуста
        
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Невозможно извлечь элемент из пустой очереди")
        return self._data.popleft()
    
    def peek(self) -> Optional[Any]:
        """
        Вернуть первый элемент очереди без удаления.
        
        Returns:
            Первый элемент очереди или None, если очередь пуста
        
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self._data[0]
    
    def is_empty(self) -> bool:
        """
        Проверить, пуста ли очередь.
        
        Returns:
            True если очередь пуста, иначе False
        
        Time Complexity: O(1)
        """
        return len(self._data) == 0
    
    def __len__(self) -> int:
        """
        Количество элементов в очереди.
        
        Returns:
            Количество элементов
        
        Time Complexity: O(1)
        """
        return len(self._data)
    
    def __repr__(self) -> str:
        """
        Строковое представление очереди.
        
        Returns:
            Строка вида Queue([элементы])
        """
        return f"Queue({list(self._data)})"
    
    def __str__(self) -> str:
        """
        Красивое строковое представление очереди.
        
        Returns:
            Строка с элементами очереди
        """
        return f"Очередь (размер: {len(self)}): {list(self._data)}"


# Демонстрационный код для тестирования
if __name__ == "__main__":
    print("=== Тестирование Stack ===")
    stack = Stack()
    
    print("Добавляем элементы в стек...")
    for i in range(5):
        stack.push(f"Элемент {i}")
        print(f"Добавлен: {stack.peek()}")
    
    print(f"\nСтек: {stack}")
    print(f"Размер стека: {len(stack)}")
    
    print("\nИзвлекаем элементы из стека...")
    while not stack.is_empty():
        print(f"Извлечен: {stack.pop()}")
    
    print(f"\nСтек пуст? {stack.is_empty()}")
    
    print("\n" + "="*40 + "\n")
    print("=== Тестирование Queue ===")
    queue = Queue()
    
    print("Добавляем элементы в очередь...")
    for i in range(5):
        queue.enqueue(f"Задача {i}")
        print(f"Добавлен: 'Задача {i}', Первый в очереди: {queue.peek()}")
    
    print(f"\nОчередь: {queue}")
    print(f"Размер очереди: {len(queue)}")
    
    print("\nОбрабатываем элементы из очереди...")
    while not queue.is_empty():
        print(f"Обработана: {queue.dequeue()}")
    
    print(f"\nОчередь пуста? {queue.is_empty()}")