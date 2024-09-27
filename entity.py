from enum import Enum


class TypeElement(Enum):
    UNLABELLED = 0
    LINE_H = 1
    LINE_V = 2
    TEXT = 3
    TABLE = 4
    CELL = 5


class Direction(Enum):
    DIRECT = 1
    REVERSE = -1


class Point:
    def __init__(self, x=-1, y=-1):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return 'x: ' + str(self.x) + '\t\t' + 'y: ' + str(self.y)


    def new_point_add(self, x=0, y=0):
        return Point(self.x + x, self.y + y)


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
        return ("Левая верхняя точка: " + str(self.left_top_cell) + "\n" +
                "Правая верхняя точка: " + str(self.right_top_cell) + "\n" +
                "Левая нижняя точка: " + str(self.left_bottom_cell) + "\n" +
                "Правая нижняя точка: " + str(self.right_bottom_cell) + "\n" +
                "Тип содержимого: " + str(self.content_type) + "\n" +
                "Содержимое: " + str(self.content))


class TableSerialize:
    def __init__(self, start_table=Point(), end_table=Point(), cells_table=None, row=1, column=1):
        if cells_table is None:
            cells_table = {}
        self.start_table = start_table
        self.end_table = end_table
        self.cells_table = cells_table
        self.row = row
        self.column = column

    def __str__(self):
        return ("Начальная точка: " + str(self.start_table) + "\n" +
                "Конечная точка: " + str(self.end_table) + "\n" +
                "Ячейки: \n" + self.cells_table_to_string() + "\n" +
                "Строк: " + str(self.row) + "\n" +
                "Колонок: " + str(self.column)
                )


    def cells_table_to_string(self):
        s = ""
        for e in self.cells_table.keys():
            s += e + "\n" + str(self.cells_table[e]) + "\n"
        return s[:-1]


class Line:
    def __init__(self, start_line=Point, end_line=Point()):
        self.start_line = start_line
        self.end_line = end_line


class IDElement:
    def __init__(self, position: Point, type_element: TypeElement):
        self.position = position
        self.type_element = type_element

    def __str__(self):
        return "Позиция: " + str(self.position) + "\nТип элемента: " + str(self.type_element)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (self.type_element == other.type_element and
            abs(self.position.x - other.position.x) <= 5 and
            abs(self.position.y - other.position.y) <= 5):
            return True
        else:
            return False

    def __hash__(self):
        return 1
