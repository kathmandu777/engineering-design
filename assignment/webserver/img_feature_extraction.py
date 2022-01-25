import cv2
import numpy as np


def get_contours(gray_img):
    """
    画像から輪郭を抽出する
    """
    contours, _ = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def mask_img(img, min_hue, max_hue, saturation_threshold):
    """
    画像をhsvに変換して、hue(色相)とsaturation(彩度)でマスクする
    """
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue = img_hsv[:, :, 0]
    saturation = img_hsv[:, :, 1]
    mask = np.zeros(hue.shape, np.uint8)
    mask[(min_hue < hue) & (hue < max_hue) & (saturation > saturation_threshold)] = 255
    return mask


def get_max_contour(contours):
    """
    与えられた輪郭の中で最大領域である輪郭とその面積を返す
    """
    max_contour = contours[0]
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_contour = contour
            max_area = area
    return max_contour, max_area


def get_line_points_from_contour(contour, img):
    """
    与えられた輪郭にフィットする直線の二点を返す
    """
    ZERO_THRESHOLD = 10 ** -5

    vx, vy, x, y = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
    _, width = img.shape[:2]
    # vxが限りなく0に近く計算をした際に発散することを防ぐearly return
    if vx < ZERO_THRESHOLD:
        return ((0, 0), (width - 1, 0))
    left_y = int((-x * vy / vx) + y)
    right_y = int(((width - x) * vy / vx) + y)
    return ((0, left_y), (width - 1, right_y))
