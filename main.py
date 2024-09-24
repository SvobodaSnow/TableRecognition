import math
from statistics import mean

import numpy as np
from PIL import Image
from spire.doc import *
from spire.doc.common import *

from entity import *
from OCR import *

img = Image.open('TEST_1.png')
imageToMatrices = np.asarray(img)
isHorizontal = True

doc = Document()
section = doc.AddSection()

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
    r_h = round(max(imageToMatrices.shape[1] * 0.01, 10))
    r_v = round(max(imageToMatrices.shape[0] * 0.01, 10))
    count_black = 0
    for i in range(r_h):
        if not is_black(imageToMatrices[start_point.y, start_point.x + i]):
            break
    else:
        return TypeElement.LINE_H
    for i in range(r_v):
        if not is_black(imageToMatrices[start_point.y + i, start_point.x]):
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

    x = start_node.x
    y = start_node.y
    y_d = y + displacement

    while True:
        x += delta
        if is_black(imageToMatrices[y, x]):
            if is_black(imageToMatrices[y_d, x]):
                t = analyze(Point(x, y_d))
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


def get_element(start_point):
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

    new_element = {}
    i, j = 1, 1

    while True:

        answer = get_horizontal_node(left_top_point, step)

        if answer[1] == TypeElement.CELL:
            new_element[str(i) + "|" + str(j)] = Cell(left_top_cell=left_top_point, right_top_cell=answer[0])
        elif answer[1] == TypeElement.LINE_H:
            new_element[str(i) + "|" + str(j)] = Line(start_line=left_top_point, end_line=answer[0])
            return new_element

        answer = get_vertical_node(left_top_point, step)

        if answer[1] == TypeElement.CELL:
            new_element[str(i) + "|" + str(j)].left_bottom_cell = answer[0]
            new_element[str(i) + "|" + str(j)].right_bottom_cell = Point(
                x=new_element[str(i) + "|" + str(j)].right_top_cell.x,
                y=new_element[str(i) + "|" + str(j)].left_bottom_cell.y
            )
        elif answer[1] == TypeElement.LINE_V:
            new_element[str(i) + "|" + str(j)] = Line(start_line=left_top_point, end_line=answer[0])
            return new_element

        print(new_element[str(i) + "|" + str(j)])

        if is_black(imageToMatrices[new_element[str(i) + "|" + str(j)].right_top_cell.y, new_element[str(i) + "|" + str(j)].right_top_cell.x + (step // 2)]):
            left_top_point = new_element[str(i) + "|" + str(j)].right_top_cell
            j += 1
        else:
            break

    return new_element


def filling_elements(element: {}):
    for t in element:
        cell = element[t]
        cell.content = string_from_image(
            img.crop(
                (cell.left_top_cell.x * 1.01,
                 cell.left_top_cell.y * 1.01,
                 cell.right_bottom_cell.x * 1.01,
                 cell.right_bottom_cell.y * 1.01)
            )
        )
        print(cell)
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
        filling_elements(el := get_element(p_b))
