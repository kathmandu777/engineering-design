import cv2
import numpy as np
import io
import picamera
from gpiozero import Robot
from time import sleep


def get_contours(gray_img):
    """
    画像から輪郭を抽出する
    """
    contours, _ = cv2.findContours(
        gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def mask_img(img, min_hue, max_hue, saturation_threshold):
    """
    画像をhsvに変換して、hue(色相)とsaturation(彩度)でマスクする
    """
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue = img_hsv[:, :, 0]
    saturation = img_hsv[:, :, 1]
    mask = np.zeros(hue.shape, np.uint8)
    mask[(min_hue < hue) & (hue < max_hue) & (
        saturation > saturation_threshold)] = 255
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


class Color:
    """
    色を表すクラス

    hue: 色相
    name: 色名
    bgr: 色のBGR値
    min_hue: 色相の許容最小値
    max_hue: 色相の許容最大値
    """
    ACCEPTABLE_ERROR = 10

    def __init__(self, hue, name, bgr):
        self.hue = hue
        self.name = name
        self.bgr = bgr

    @property
    def min_hue(self):
        return max(0, self.hue - Color.ACCEPTABLE_ERROR)

    @property
    def max_hue(self):
        return min(179, self.hue + Color.ACCEPTABLE_ERROR)


def main():
    """
    カメラ画像によってモーター制御を行う
    """
    LINE_WIDTH = 3

    # 抽出する色の特徴値
    green = Color(60, "green", (0, 255, 0))
    blue = Color(120, "blue", (255, 0, 0))
    orange = Color(15, "orange", (0, 165, 255))
    colors = [blue, orange, green]
    SATURATION_THRESHOLD = 128

    # ロボットの初期化 (stopも行っておく)
    robot = Robot(left=(17, 18), right=(19, 20))
    robot.stop()

    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.hflip = True
        camera.vflip = True
        while True:
            camera.capture(stream, format='jpeg')
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            stream.seek(0)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)

            # カメラ画像の最大領域色を抽出
            max_area = 0
            max_contour = None
            max_color = None
            for color in colors:
                mask = mask_img(img, color.min_hue, color.max_hue,
                                SATURATION_THRESHOLD)
                contours = get_contours(mask)
                if contours:
                    this_color_max_contour, this_color_max_area = get_max_contour(
                        contours)
                    if this_color_max_area > max_area:
                        max_area = this_color_max_area
                        max_contour = this_color_max_contour
                        max_color = color

            # 色によってモーター制御
            if max_color is not None:
                cv2.drawContours(img, [max_contour], 0,
                                 max_color.bgr, LINE_WIDTH)
                if max_color.name == "green":
                    robot.forward()
                elif max_color.name == "blue":
                    robot.left()
                elif max_color.name == "orange":
                    robot.right()
                sleep(0.2)
            else:
                robot.stop()

            cv2.imshow("img", img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                robot.stop()
                break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
