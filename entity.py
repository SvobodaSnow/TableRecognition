from enum import Enum


class TypeElement(Enum):
    UNLABELLED = 0
    LINE_H = 1
    LINE_V = 2
    TEXT = 3
    TABLE = 4


class Direction(Enum):
    DIRECT = 0
    REVERSE = 1


class Point:
    def __init__(self, x=-1, y=-1):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return 'x: ' + str(self.x) + '\t\t' + 'y: ' + str(self.y)


class Cell:
    def __init__(self, start_cell=Point(), end_cell=Point(), content_type=TypeElement.UNLABELLED, content=None):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.content_type = content_type
        self.content = content

    def __str__(self):
        pass


class Table:
    def __init__(self, start_table=Point(), end_table=Point()):
        self.start_table = start_table
        self.end_table = end_table
        self.cells_table = []

    def __str__(self):
        pass
