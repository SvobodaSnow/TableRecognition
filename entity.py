from enum import Enum


class TypeElement(Enum):
    UNLABELLED = 0
    LINE_H = 1
    LINE_V = 2
    TEXT = 3
    TABLE = 4


class Point:
    def __init__(self, x=-1, y=-1):
        self.x = int(x)
        self.y = int(y)


class Cell:
    def __init__(self, start_cell, end_cell=Point(), content_type=TypeElement.UNLABELLED, content=None):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.content_type = content_type
        self.content = content


class Table:
    def __init__(self, start_table, end_table):
        self.start_table = start_table
        self.end_table = end_table
        self.cells_table = []
