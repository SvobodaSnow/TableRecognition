import math

from PIL import Image
import numpy as np

img = Image.open('TEST.png')
imageToMatrice = np.asarray(img)
isHorizontal = True
k = 1
r = 1


def get_area():
    for i in range(0, 2 * r + 1):
        for j in range(0, 2 * r + 1):
            print(i, j, '\t\t', imageToMatrice[i, j])
    return


if __name__ == '__main__':
    r = int((((imageToMatrice.shape[1] * imageToMatrice.shape[0]) * 0.001) ** 0.5) // 2)

    k = math.floor((imageToMatrice.shape[1] / imageToMatrice.shape[0])
                   if (isHorizontal := imageToMatrice.shape[1] > imageToMatrice.shape[0])
                   else (imageToMatrice[0] / imageToMatrice[1]))

    get_area()

    if isHorizontal:
        for i in range(r, imageToMatrice.shape[0]):
            a = 1
    else:
        for i in range(r, imageToMatrice.shape[1]):
            a = 1
