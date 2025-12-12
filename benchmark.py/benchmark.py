"""
Сравнение производительности различных структур данных.
"""

import time
from collections import deque
from src.lab10.structures import Stack, Queue
from src.lab10.linked_list import SinglyLinkedList


def benchmark_push_pop(n: int = 10000) -> None:
    """Сравнение операций push/pop для Stack и list."""
    print(f"\n=== Бенчмарк: push/pop для {n} элементов ===")
    
    # Тестирование Stack
    start = time.perf_counter()
    stack = Stack()
    for i in range(n):
        stack.push(i)
    for _ in range(n):
        stack.pop()
    stack_time = time.perf_counter() - start
    
    # Тестирование обычного списка
    start = time.perf_counter()
    lst = []
    for i in range(n):
        lst.append(i)
    for _ in range(n):
        lst.pop()
    list_time = time.perf_counter() - start
    
    print(f"Stack: {stack_time:.6f} секунд")
    print(f"list:  {list_time:.6f} секунд")
    print(f"Разница: {stack_time/list_time:.2f}x")


def benchmark_enqueue_dequeue(n: int = 10000) -> None:
    """Сравнение операций enqueue/dequeue для Queue, deque и list."""
    print(f"\n=== Бенчмарк: enqueue/dequeue для {n} элементов ===")
    
    # Тестирование Queue
    start = time.perf_counter()
    queue = Queue()
    for i in range(n):
        queue.enqueue(i)
    for _ in range(n):
        queue.dequeue()
    queue_time = time.perf_counter() - start
    
    # Тестирование deque
    start = time.perf_counter()
    dq = deque()
    for i in range(n):
        dq.append(i)
    for _ in range(n):
        dq.popleft()
    deque_time = time.perf_counter() - start
    
    # Тестирование обычного списка (неэффективно!)
    start = time.perf_counter()
    lst = []
    for i in range(n):
        lst.append(i)
    for _ in range(n):
        lst.pop(0)  # O(n) операция!
    list_time = time.perf_counter() - start
    
    print(f"Queue: {queue_time:.6f} секунд")
    print(f"deque: {deque_time:.6f} секунд")
    print(f"list:  {list_time:.6f} секунд (pop(0))")
    print(f"\nПримечание: list.pop(0) имеет сложность O(n), поэтому медленнее!")


def benchmark_linked_list_operations(n: int = 5000) -> None:
    """Сравнение операций для связного списка и обычного списка."""
    print(f"\n=== Бенчмарк: операции со списками для {n} элементов ===")
    
    # Тестирование вставки в начало
    print("\n1. Вставка в начало (prepend/insert(0, value)):")
    
    start = time.perf_counter()
    sll = SinglyLinkedList()
    for i in range(n):
        sll.prepend(i)
    sll_time = time.perf_counter() - start
    
    start = time.perf_counter()
    lst = []
    for i in range(n):
        lst.insert(0, i)  # O(n) операция!
    list_time = time.perf_counter() - start
    
    print(f"   SinglyLinkedList.prepend: {sll_time:.6f} секунд (O(1))")
    print(f"   list.insert(0, value):    {list_time:.6f} секунд (O(n))")
    print(f"   Разница: {list_time/sll_time:.2f}x")
    
    # Тестирование вставки в конец
    print("\n2. Вставка в конец (append):")
    
    start = time.perf_counter()
    sll.clear()
    for i in range(n):
        sll.append(i)
    sll_time = time.perf_counter() - start
    
    start = time.perf_counter()
    lst = []
    for i in range(n):
        lst.append(i)
    list_time = time.perf_counter() - start
    
    print(f"   SinglyLinkedList.append: {sll_time:.6f} секунд (O(1) с tail)")
    print(f"   list.append:             {list_time:.6f} секунд (O(1) в среднем)")
    
    # Тестирование доступа по индексу
    print("\n3. Доступ по индексу (get):")
    
    start = time.perf_counter()
    for i in range(min(n, 1000)):  # Меньше итераций, т.к. O(n) операция
        _ = sll.get(i)
    sll_time = time.perf_counter() - start
    
    start = time.perf_counter()
    for i in range(min(n, 1000)):
        _ = lst[i]
    list_time = time.perf_counter() - start
    
    print(f"   SinglyLinkedList.get: {sll_time:.6f} секунд (O(n))")
    print(f"   list[i]:              {list_time:.6f} секунд (O(1))")
    print(f"   Разница: {sll_time/list_time:.2f}x")


def benchmark_memory_usage() -> None:
    """Сравнение использования памяти."""
    print("\n=== Анализ использования памяти ===")
    print("\n1. Stack vs list:")
    print("   - Stack использует list внутри, поэтому память одинаковая")
    print("   - Плюс Stack: абстракция и защита от неправильного использования")
    
    print("\n2. Queue vs deque:")
    print("   - Queue использует deque внутри, поэтому память одинаковая")
    print("   - Плюс Queue: FIFO семантика, четкий API")
    
    print("\n3. SinglyLinkedList vs list:")
    print("   - SinglyLinkedList: больше памяти на узел (value + next pointer)")
    print("   - list: меньше памяти, т.к. хранит только значения в массиве")
    print("   - Обычно: список Python эффективнее по памяти в 2-3 раза")


def main():
    """Основная функция бенчмаркинга."""
    print("=" * 60)
    print("БЕНЧМАРКИНГ СТРУКТУР ДАННЫХ")
    print("=" * 60)
    
    # Размеры для тестов
    small_n = 1000
    medium_n = 10000
    large_n = 50000
    
    # Запуск бенчмарков
    benchmark_push_pop(small_n)
    benchmark_enqueue_dequeue(small_n)
    benchmark_linked_list_operations(small_n)
    benchmark_memory_usage()
    
    print("\n" + "=" * 60)
    print("ОСНОВНЫЕ ВЫВОДЫ:")
    print("=" * 60)
    print("""
1. Stack (на базе list):
   - Эффективность равна обычному списку
   - Плюс: чистая LIFO семантика, защита от ошибок

2. Queue (на базе deque):
   - deque уже оптимизирован для операций с двух сторон
   - НИКОГДА не используйте list.pop(0) для очереди!

3. SinglyLinkedList:
   - Быстрая вставка/удаление в начале (O(1))
   - Медленный доступ по индексу (O(n))
   - Больше памяти, чем у list
   - Полезен когда нужно часто вставлять/удалять в начале
   """)
    
    print("\nРЕКОМЕНДАЦИИ ПО ВЫБОРУ СТРУКТУРЫ:")
    print("""
1. Для LIFO (стек): используйте list или collections.deque
2. Для FIFO (очередь): ВСЕГДА используйте collections.deque
3. Для связного списка: используйте только если:
   - Часто вставляете/удаляете в начале
   - Не нужен доступ по индексу
   - Не критична память
4. В 95% случаев: обычный list или deque достаточно
    """)


if __name__ == "__main__":
    main()