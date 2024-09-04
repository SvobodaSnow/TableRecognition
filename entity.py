from enum import Enum


class TypeElement(Enum):
    UNLABELLED = 0
    LINE_H = 1
    LINE_V = 2
    TEXT = 3
    TABLE = 4


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


class Cell:
    def __init__(self, start_cell, end_cell, content_type=TypeElement.UNLABELLED):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.content_type = content_type
