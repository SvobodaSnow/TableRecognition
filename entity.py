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
        return ("Левая верхняя точка:\t\t" + str(self.left_top_cell) + "\n" +
                "Правая верхняя точка:\t\t" + str(self.right_top_cell) + "\n" +
                "Левая нижняя точка:\t\t\t" + str(self.left_bottom_cell) + "\n" +
                "Правая нижняя точка:\t\t" + str(self.right_bottom_cell) + "\n" +
                "Тип содержимого: " + str(self.content_type) + "\n" +
                "Содержимое: " + str(self.content))


class TableSerialize:
    def __init__(self, start=Point(), end=Point(), cells_table=None, row=1, column=1):
        if cells_table is None:
            cells_table = {}
        self.start = start
        self.end = end
        self.cells_table = cells_table
        self.row = row
        self.column = column

    def __str__(self):
        return ("Начальная точка: " + str(self.start) + "\n" +
                "Конечная точка: " + str(self.end) + "\n" +
                "Ячейки: \n" + self.cells_table_to_string() + "\n" +
                "Строк: " + str(self.row) + "\n" +
                "Колонок: " + str(self.column)
                )


    def cells_table_to_string(self):
        s = ""
        i = 0
        for row in self.cells_table:
            i += 1
            j = 0
            for cell in row:
                j += 1
                s += str(i) + "|" + str(j) + "\n" + str(cell) + "\n"
        return s[:-1]


class Line:
    def __init__(self, start=Point, end=Point()):
        self.start = start
        self.end = end


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
