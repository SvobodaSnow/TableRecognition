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
    def __init__(
            self,
            left_top_cell=Point(),
            right_top_cell=Point(),
            left_bottom_cell=Point(),
            right_bottom_cell=Point(),
            content_type=TypeElement.UNLABELLED,
            content=None
    ):
        self.left_top_cell = left_top_cell
        self.right_top_cell = right_top_cell
        self.left_bottom_cell = left_bottom_cell
        self.right_bottom_cell = right_bottom_cell
        self.content_type = content_type
        self.content = content

    def __str__(self):
        return ("Начальная точка: " + str(self.start_cell) + "\nКонечная точка: " + str(self.end_cell) + "\nТип "
                                    "содержимого: " + str(self.content_type) + "\nСодержимое: " + str(self.content))


class Table:
    def __init__(self, start_table=Point(), end_table=Point()):
        self.start_table = start_table
        self.end_table = end_table
        self.cells_table = []

    def __str__(self):
        return "Начальная точка: " + str(self.start_table) + "\nКонечная точка: " + str(self.end_table)


class Line:
    def __init__(self, start_line=Point, end_line=Point()):
        self.start_line = start_line
        self.end_line = end_line
