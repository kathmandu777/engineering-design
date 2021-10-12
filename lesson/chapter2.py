import cv2
import numpy as np


def init_image(width, height, red, green, blue):
    image = np.zeros((height, width, 3), np.uint8)
    image[:] = [blue, green, red]
    return image


width = 320
height = 240
red = 0
green = 0
blue = 0
img = init_image(width, height, red, green, blue)
cv2.namedWindow("display")
cv2.imshow("display", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
