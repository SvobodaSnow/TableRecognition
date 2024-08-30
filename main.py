import math
from statistics import mean

from PIL import Image
import numpy as np

img = Image.open('TEST.png')
imageToMatrice = np.asarray(img)
isHorizontal = True
k = 1
r = 1


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


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
            if is_black(imageToMatrice[i, j]):
                return Point(j, i)
    return


def analyze(start_point):

    print('\t\t\t\t\t', imageToMatrice[(start_point.y - 1), start_point.x])
    print(imageToMatrice[start_point.y, start_point.x - 1], "\t", imageToMatrice[start_point.y, start_point.x], "\t", imageToMatrice[start_point.y, start_point.x + 1])
    print('\t\t\t\t\t', imageToMatrice[(start_point.y + 1), start_point.x])
    return


if __name__ == '__main__':
    r = int((((imageToMatrice.shape[1] * imageToMatrice.shape[0]) * 0.001) ** 0.5) // 2)

    k = math.floor((imageToMatrice.shape[1] / imageToMatrice.shape[0])
                   if (isHorizontal := imageToMatrice.shape[1] > imageToMatrice.shape[0])
                   else (imageToMatrice[0] / imageToMatrice[1]))

    if isHorizontal:
        for i in range(imageToMatrice.shape[0] - 2 * r):
            if p_b := search_black_point(Point(x=i * k, y=i)):
                print(imageToMatrice[p_b.y, p_b.x])
                analyze(p_b)
                break
    else:
        for i in range(imageToMatrice.shape[1] - 2 * r):
            search_black_point(Point(x=i, y=i*k))
