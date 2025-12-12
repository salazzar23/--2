"""
Реализация односвязного списка (Singly Linked List).
"""

from typing import Any, Optional, Iterator


class Node:
    """
    Узел односвязного списка.
    
    Атрибуты:
        value: Значение узла
        next: Ссылка на следующий узел или None
    """
    
    def __init__(self, value: Any, next_node: Optional['Node'] = None) -> None:
        """
        Инициализация узла.
        
        Args:
            value: Значение узла
            next_node: Следующий узел (по умолчанию None)
        """
        self.value: Any = value
        self.next: Optional[Node] = next_node
    
    def __repr__(self) -> str:
        """Строковое представление узла."""
        return f"Node({self.value})"


class SinglyLinkedList:
    """
    Односвязный список.
    
    Особенности:
    - prepend(): O(1) - вставка в начало
    - append(): O(1) с tail, O(n) без tail - вставка в конец
    - insert(): O(n) в худшем случае - вставка по индексу
    - remove(): O(n) - удаление по значению
    """
    
    def __init__(self) -> None:
        """Инициализация пустого списка."""
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0
    
    def append(self, value: Any) -> None:
        """
        Добавить элемент в конец списка.
        
        Args:
            value: Значение для добавления
        
        Time Complexity: O(1) благодаря tail
        """
        new_node = Node(value)
        
        if self.is_empty():
            # Если список пуст, новый узел становится и head, и tail
            self.head = new_node
            self.tail = new_node
        else:
            # Добавляем в конец и обновляем tail
            self.tail.next = new_node
            self.tail = new_node
        
        self._size += 1
    
    def prepend(self, value: Any) -> None:
        """
        Добавить элемент в начало списка.
        
        Args:
            value: Значение для добавления
        
        Time Complexity: O(1)
        """
        new_node = Node(value)
        
        if self.is_empty():
            # Если список пуст, новый узел становится и head, и tail
            self.head = new_node
            self.tail = new_node
        else:
            # Добавляем в начало
            new_node.next = self.head
            self.head = new_node
        
        self._size += 1
    
    def insert(self, idx: int, value: Any) -> None:
        """
        Вставить элемент по указанному индексу.
        
        Args:
            idx: Индекс для вставки
            value: Значение для вставки
        
        Raises:
            IndexError: Если индекс вне допустимого диапазона
        
        Time Complexity: O(n) в худшем случае
        """
        if idx < 0 or idx > self._size:
            raise IndexError(f"Индекс {idx} вне диапазона [0, {self._size}]")
        
        if idx == 0:
            # Вставка в начало
            self.prepend(value)
        elif idx == self._size:
            # Вставка в конец
            self.append(value)
        else:
            # Вставка в середину
            new_node = Node(value)
            current = self.head
            for _ in range(idx - 1):
                current = current.next
            
            new_node.next = current.next
            current.next = new_node
            self._size += 1
    
    def remove(self, value: Any) -> bool:
        """
        Удалить первое вхождение указанного значения.
        
        Args:
            value: Значение для удаления
        
        Returns:
            True если элемент был удален, иначе False
        
        Time Complexity: O(n)
        """
        if self.is_empty():
            return False
        
        # Специальный случай: удаление первого элемента
        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            
            # Если список стал пустым, обновляем tail
            if self.head is None:
                self.tail = None
            return True
        
        # Поиск узла, предшествующего удаляемому
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                # Найден узел для удаления
                current.next = current.next.next
                self._size -= 1
                
                # Если удалили последний элемент, обновляем tail
                if current.next is None:
                    self.tail = current
                return True
            
            current = current.next
        
        return False
    
    def remove_at(self, idx: int) -> Any:
        """
        Удалить элемент по индексу.
        
        Args:
            idx: Индекс удаляемого элемента
        
        Returns:
            Значение удаленного элемента
        
        Raises:
            IndexError: Если индекс вне допустимого диапазона
        
        Time Complexity: O(n)
        """
        if idx < 0 or idx >= self._size:
            raise IndexError(f"Индекс {idx} вне диапазона [0, {self._size - 1}]")
        
        # Специальный случай: удаление первого элемента
        if idx == 0:
            value = self.head.value
            self.head = self.head.next
            self._size -= 1
            
            # Если список стал пустым, обновляем tail
            if self.head is None:
                self.tail = None
            return value
        
        # Удаление из середины или конца
        current = self.head
        for _ in range(idx - 1):
            current = current.next
        
        value = current.next.value
        current.next = current.next.next
        self._size -= 1
        
        # Если удалили последний элемент, обновляем tail
        if current.next is None:
            self.tail = current
        
        return value
    
    def search(self, value: Any) -> bool:
        """
        Проверить наличие значения в списке.
        
        Args:
            value: Искомое значение
        
        Returns:
            True если значение найдено, иначе False
        
        Time Complexity: O(n)
        """
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False
    
    def get(self, idx: int) -> Any:
        """
        Получить значение по индексу.
        
        Args:
            idx: Индекс элемента
        
        Returns:
            Значение элемента
        
        Raises:
            IndexError: Если индекс вне допустимого диапазона
        
        Time Complexity: O(n)
        """
        if idx < 0 or idx >= self._size:
            raise IndexError(f"Индекс {idx} вне диапазона [0, {self._size - 1}]")
        
        current = self.head
        for _ in range(idx):
            current = current.next
        
        return current.value
    
    def is_empty(self) -> bool:
        """
        Проверить, пуст ли список.
        
        Returns:
            True если список пуст, иначе False
        
        Time Complexity: O(1)
        """
        return self._size == 0
    
    def clear(self) -> None:
        """Очистить список. Time Complexity: O(1)"""
        self.head = None
        self.tail = None
        self._size = 0
    
    def __len__(self) -> int:
        """
        Количество элементов в списке.
        
        Returns:
            Количество элементов
        
        Time Complexity: O(1)
        """
        return self._size
    
    def __iter__(self) -> Iterator[Any]:
        """
        Итератор по значениям списка.
        
        Returns:
            Итератор
        
        Time Complexity: O(n) для полного обхода
        """
        current = self.head
        while current is not None:
            yield current.value
            current = current.next
    
    def __repr__(self) -> str:
        """
        Строковое представление списка.
        
        Returns:
            Строка вида SinglyLinkedList([элементы])
        """
        values = list(self)
        return f"SinglyLinkedList({values})"
    
    def __str__(self) -> str:
        """
        Красивое текстовое представление связей.
        
        Returns:
            Строка вида [A] -> [B] -> [C] -> None
        """
        parts = []
        current = self.head
        
        while current is not None:
            parts.append(f"[{current.value}]")
            current = current.next
        
        if parts:
            return " -> ".join(parts) + " -> None"
        else:
            return "Пустой список"


# Демонстрационный код для тестирования
if __name__ == "__main__":
    print("=== Тестирование SinglyLinkedList ===")
    sll = SinglyLinkedList()
    
    print("1. Добавление элементов в конец (append):")
    for i in range(1, 4):
        sll.append(i)
        print(f"   Добавлен {i}: {sll}")
    
    print(f"\n2. Размер списка: {len(sll)}")
    print(f"   Список пуст? {sll.is_empty()}")
    
    print("\n3. Добавление элементов в начало (prepend):")
    sll.prepend(0)
    print(f"   Добавлен 0 в начало: {sll}")
    
    print("\n4. Вставка по индексу (insert):")
    sll.insert(2, 2.5)
    print(f"   Вставлен 2.5 на позицию 2: {sll}")
    
    print("\n5. Поиск элементов (search):")
    for value in [2.5, 10]:
        found = sll.search(value)
        print(f"   {value} в списке? {found}")
    
    print("\n6. Получение элементов по индексу (get):")
    for i in range(len(sll)):
        print(f"   Индекс {i}: {sll.get(i)}")
    
    print("\n7. Итерация по списку:")
    print("   Элементы: ", end="")
    for item in sll:
        print(item, end=" ")
    print()
    
    print("\n8. Удаление по значению (remove):")
    removed = sll.remove(2.5)
    print(f"   Удален 2.5? {removed}")
    print(f"   Список после удаления: {sll}")
    
    print("\n9. Удаление по индексу (remove_at):")
    value = sll.remove_at(2)
    print(f"   Удален элемент с индексом 2: {value}")
    print(f"   Список после удаления: {sll}")
    
    print("\n10. Очистка списка (clear):")
    sll.clear()
    print(f"   Список после очистки: {sll}")
    print(f"   Размер: {len(sll)}, Пуст? {sll.is_empty()}")