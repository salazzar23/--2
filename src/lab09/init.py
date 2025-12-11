"""
Пакет lab09 - работа с базой данных студентов на основе CSV.
Содержит класс Group для CRUD-операций.
"""

from .group import Group, create_sample_data

__all__ = ['Group', 'create_sample_data']
__version__ = '1.0.0'