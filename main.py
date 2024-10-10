import math
from statistics import mean

import numpy as np
from spire.doc import *
from spire.doc.common import *

from TableManipulation import add_row_table
from entity import *
from OCR import *

# TABLE_TEST_MERGE.png
# TEST_LINE.png
# TEST_1.png
name_img = "TEST_1.png"
img = Image.open(name_img)
imageToMatrices = np.asarray(img)
isHorizontal = True
objects = {}

k = 1
r = 1


def is_black(point_p):
    mean_p = mean((point_p[0], point_p[1], point_p[2]))
    if (point_p[0] < 40 and point_p[1] < 40 and point_p[2] < 40 and
            abs(point_p[0] - mean_p) < 5 and abs(point_p[1] - mean_p) < 5 and abs(point_p[2] - mean_p) < 5):
        return True
    else:
        return False


def search_black_point(start_point):
    for i in range(start_point.y, start_point.y + (2 * r + 1)):
        for j in range(start_point.x, start_point.x + (2 * r + 1)):
            if is_black(imageToMatrices[i, j]):
                return Point(j, i)
    return


def analyze(start_point):
    r_h = round(max(imageToMatrices.shape[1] * 0.01, 40))
    r_v = round(max(imageToMatrices.shape[0] * 0.01, 40))
    count_black = 0
    for i in range(r_h):
        if not is_black(imageToMatrices[start_point.y, start_point.x + i]):
            break
    else:
        return TypeElement.LINE_H
    for i in range(r_h):
        if not is_black(imageToMatrices[start_point.y, start_point.x - i]):
            break
    else:
        return TypeElement.LINE_H
    for i in range(r_v):
        if not is_black(imageToMatrices[start_point.y + i, start_point.x]):
            break
    else:
        return TypeElement.LINE_V
    for i in range(r_v):
        if not is_black(imageToMatrices[start_point.y - i, start_point.x]):
            break
    else:
        return TypeElement.LINE_V
    for i in range(r_v):
        for j in range(r_h):
            if is_black(imageToMatrices[start_point.y + i, start_point.x + j]):
                count_black += 1
    else:
        if (count_black / (r_v * r_h)) > 0.2:
            return TypeElement.TEXT
    return TypeElement.UNLABELLED


def get_horizontal_node(start_node, displacement, direction=Direction.DIRECT):
    delta = direction.value

    x = start_node.x + displacement
    y = start_node.y
    y_d_t = y - displacement
    y_d_d = y + displacement

    while True:
        x += delta
        if is_black(imageToMatrices[y, x]):
            f_top = is_black(imageToMatrices[y_d_t, x])
            f_down = is_black(imageToMatrices[y_d_d, x])
            if f_top or f_down:
                if f_down:
                    t = analyze(Point(x, y_d_d))
                else:
                    t = analyze(Point(x, y_d_t))
                if t is not TypeElement.UNLABELLED and t is not TypeElement.TEXT:
                    return Point(x, y), TypeElement.CELL
        else:
            return Point(x, y), TypeElement.LINE_H


def get_vertical_node(start_node, displacement, direction=Direction.DIRECT):
    delta = direction.value

    x = start_node.x
    y = start_node.y + displacement
    x_d = x + displacement

    while True:
        y += delta
        if is_black(imageToMatrices[y, x]):
            if is_black(imageToMatrices[y, x_d]):
                t = analyze(Point(x_d, y))
                if t is not TypeElement.UNLABELLED and t is not TypeElement.TEXT:
                    return Point(x, y), TypeElement.CELL
        else:
            return Point(x, y), TypeElement.LINE_V


def get_element_old(start_point):
    step = 0
    step_x = 0
    step_y = 0

    left_top_point = Point()

    while True:
        if is_black(imageToMatrices[start_point.y - step_y, start_point.x - step_x]):
            step_x += 1
        else:
            step_y += 1
            if not is_black(imageToMatrices[start_point.y - step_y, start_point.x - step_x + 1]):
                left_top_point.y = start_point.y - step_y + 1
                left_top_point.x = start_point.x - step_x + 1
                break

    while True:
        step += 1
        if not is_black(imageToMatrices[left_top_point.y + step, left_top_point.x + step]):
            step = step * 2
            break

    new_table = TableSerialize(
        start=left_top_point
    )

    new_element = [[]]
    i, j = 1, 1

    while True:
        print(i, j)
        answer = get_horizontal_node(left_top_point, step)

        if answer[1] == TypeElement.CELL:
            if i == 1:
                new_element[i - 1].append(Cell(left_top_cell=left_top_point, right_top_cell=answer[0]))
            else:
                new_element[i - 1][j - 1] = Cell(left_top_cell=left_top_point, right_top_cell=answer[0])
        elif answer[1] == TypeElement.LINE_H:
            new_element[i - 1].append(Line(start=left_top_point, end=answer[0]))
            return new_element

        answer = get_vertical_node(left_top_point, step)
        if answer[1] == TypeElement.CELL:

            new_element[i - 1][j - 1].left_bottom_cell = answer[0]

            end_point = Point(
                x=new_element[i - 1][j - 1].right_top_cell.x,
                y=new_element[i - 1][j - 1].left_bottom_cell.y
            )

            new_element[i - 1][j - 1].right_bottom_cell = end_point
        elif answer[1] == TypeElement.LINE_V:
            new_element[0].append(Line(start=left_top_point, end=answer[0]))
            return new_element

        if is_black(imageToMatrices[new_element[i - 1][j - 1].right_top_cell.y, new_element[i - 1][j - 1].right_top_cell.x + (step // 2)]):
            left_top_point = new_element[i - 1][j - 1].right_top_cell
            j += 1
        else:
            j = 1
            left_top_point = new_element[i - 1][j - 1].left_bottom_cell
            if is_black(imageToMatrices[left_top_point.y + (step // 2), left_top_point.x]):
                i += 1
                add_row_table(new_element)
            else:
                break


    for row in new_element:
        for cell in row:
            print(cell)
    print(len(new_element), len(new_element[0]))

    new_table.cells_table = new_element
    new_table.end = end_point
    new_table.column = len(new_element[0])
    new_table.row = len(new_element)

    return new_table


def get_left_top_point(start_point):
    step_x = 0
    step_y = 0

    left_top_point = Point()

    while True:
        if is_black(imageToMatrices[start_point.y - step_y, start_point.x - step_x]):
            step_x += 1
        else:
            step_y += 1
            if not is_black(imageToMatrices[start_point.y - step_y, start_point.x - step_x + 1]):
                left_top_point.y = start_point.y - step_y + 1
                left_top_point.x = start_point.x - step_x + 1
                break
    return left_top_point


def get_displacement(start_point):
    step = 0
    while True:
        step += 1
        if not is_black(imageToMatrices[start_point.y + step, start_point.x + step]):
            step = step * 2
            break
    return step


def get_element(start_point):
    # Получение параметров проверки и первой точки
    left_top_point = get_left_top_point(start_point)
    displacement = get_displacement(left_top_point)

    # Получение горизонтальной точки
    horizontal_point_answer = get_horizontal_node(left_top_point, displacement)

    # Проверка на тип линии
    if horizontal_point_answer[1] == TypeElement.LINE_H:
        return Line(left_top_point, horizontal_point_answer[0]), TypeElement.LINE_H

    # Создание новой таблицы
    new_cells_table = [[]]

    # Заполнение первой ячейки
    vertical_point_answer = get_vertical_node(left_top_point, displacement)

    new_cells_table[0].append(
        Cell(
            left_top_cell=left_top_point,
            right_top_cell=horizontal_point_answer[0],
            left_bottom_cell=vertical_point_answer[0],
            right_bottom_cell=Point(x=horizontal_point_answer[0].x, y=vertical_point_answer[0].y)
        )
    )

    # Создание класса таблицы
    table = TableSerialize(start=left_top_point)

    # Индексы ячеек
    i, j = 0, 1

    # Переопределение левой точки, как точки отсчета новой ячейки
    left_top_point = horizontal_point_answer[0]

    # Поиск новых ячеек
    while True:
        # Получение правой верхней точки таблицы
        horizontal_point_answer = get_horizontal_node(left_top_point, displacement)

        # Получение левой нижней точки таблицы
        vertical_point_answer = get_vertical_node(left_top_point, displacement)

        right_bottom_point = Point(x=horizontal_point_answer[0].x, y=vertical_point_answer[0].y)

        # Добавление новой ячейки
        # Проверка, первая ли строка заполняется или нет
        if i == 0:
            # Добавление новой ячейки в конец первой строки
            new_cells_table[i].append(
                Cell(
                    left_top_cell=left_top_point,
                    right_top_cell=horizontal_point_answer[0],
                    left_bottom_cell=vertical_point_answer[0],
                    right_bottom_cell=right_bottom_point
                )
            )
        else:
            # Добавление новой ячейки в остальных строках
            new_cells_table[i][j] = Cell(
                left_top_cell=left_top_point,
                right_top_cell=horizontal_point_answer[0],
                left_bottom_cell=vertical_point_answer[0],
                right_bottom_cell=right_bottom_point
            )

        # Проверка на продолжение таблицы
        if is_black(
            imageToMatrices[horizontal_point_answer[0].y, horizontal_point_answer[0].x + displacement]
        ):
            # Переход на следующую ячейку
            j += 1
            left_top_point = horizontal_point_answer[0]
        else:
            # Проверка на существование следующей строки
            if is_black(
                imageToMatrices[right_bottom_point.y + displacement, right_bottom_point.x]
            ):
                j = 0
                cell = new_cells_table[i][j]
                left_top_point = cell.left_bottom_cell
                i += 1
                add_row_table(new_cells_table)
            else:
                break

    table.cells_table = new_cells_table
    table.row = len(new_cells_table)
    table.column = len(new_cells_table[0])
    table.end = right_bottom_point

    print(table)

    return table, TypeElement.TABLE


def filling_elements(element: [[]]):
    for row in element:
        for cell in row:
            if cell is not None:
                cell.content = string_from_image(
                    img.crop(
                        (cell.left_top_cell.x * 1.01,
                         cell.left_top_cell.y * 1.01,
                         cell.right_bottom_cell.x * 1.01,
                         cell.right_bottom_cell.y * 1.01)
                    )
                )
    return


def create_word():
    name_document = name_img[:name_img.rfind(".")] + ".docx"

    doc = Document()
    section = doc.AddSection()

    for o in objects:
        table = Table(doc, True)
        table.PreferredWidth = PreferredWidth(WidthType.Percentage, int(100))

        table.TableFormat.Borders.BorderType = BorderStyle.Single
        table.TableFormat.Borders.Color = Color.get_Black()

        if o.type_element == TypeElement.TABLE:
            element = objects[o]
            table.AddRow(False, element.column)

            for _ in range(element.row - 1):
                table.AddRow()

            for i in range(len(element.cells_table)):
                for j in range(len(element.cells_table[i])):
                    cell = element.cells_table[i][j]
                    if cell is not None:
                        table.Rows[i].Cells[j].AddParagraph().AppendText(element.cells_table[i][j].content).CharacterFormat.LocaleIdASCII = 1049

            section.Tables.Add(table)

    doc.SaveToFile(name_document)
    doc.Close()
    return


if __name__ == '__main__':
    r = int((((imageToMatrices.shape[1] * imageToMatrices.shape[0]) * 0.001) ** 0.5) // 2)
    type_o = TypeElement.UNLABELLED
    start_p = Point(0, 0)

    k = math.floor((imageToMatrices.shape[1] / imageToMatrices.shape[0])
                   if (isHorizontal := imageToMatrices.shape[1] > imageToMatrices.shape[0])
                   else (imageToMatrices[0] / imageToMatrices[1]))

    if isHorizontal:
        for i in range(imageToMatrices.shape[0] - 2 * r):
            if p_b := search_black_point(start_p := Point(x=i * k, y=i)):
                type_o = analyze(p_b)
                break
    else:
        for i in range(imageToMatrices.shape[1] - 2 * r):
            if p_b := search_black_point(start_p := Point(x=i * k, y=i)):
                type_o = analyze(p_b)
                break

    if type_o is TypeElement.LINE_V or type_o is TypeElement.LINE_H:
        el, type = get_element(p_b)
        if type == TypeElement.TABLE:
            filling_elements(el.cells_table)
        objects[IDElement(el.start, type)] = el

    create_word()
