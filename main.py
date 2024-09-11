import math
from statistics import mean

from PIL import Image
import numpy as np

from entity import *

img = Image.open('TEST.png')
imageToMatrices = np.asarray(img)
isHorizontal = True
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
    if direction == Direction.DIRECT:
        delta = 1
    elif direction == Direction.REVERSE:
        delta = -1
    else:
        return None

    x = start_node.x
    y = start_node.y
    y_d = start_node.y + displacement

    t = None

    while True:
        x += delta
        if is_black(imageToMatrices[y, x]):
            if is_black(imageToMatrices[y_d, x]):
                t = analyze(Point(x, y_d))
                if t is not TypeElement.UNLABELLED and t is not TypeElement.TEXT:
                    return Point(x, y)
        else:
            return None


def get_vertical_node(start_node, displacement, direction=Direction.DIRECT):
    if direction == Direction.DIRECT:
        delta = 1
    elif direction == Direction.REVERSE:
        delta = -1
    else:
        return None

    x = start_node.x
    y = start_node.y
    x_d = start_node.x + displacement

    t = None

    while True:
        y += delta
        if is_black(imageToMatrices[y, x]):
            if is_black(imageToMatrices[y, x_d]):
                t = analyze(Point(x_d, y))
                if t is not TypeElement.UNLABELLED and t is not TypeElement.TEXT:
                    return Point(x, y)
        else:
            return None


def get_table(start_point):
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

    search_cell_point = left_top_point
    new_table = Table(start_table=left_top_point)

    while True:
        new_cell = Cell(start_cell=search_cell_point)
        right_top_point_cell = get_horizontal_node(search_cell_point, step)

        break

    return new_table


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
        print(get_table(p_b))
