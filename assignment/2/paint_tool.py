
from unicodedata import category
import numpy as np
import cv2
from enum import IntEnum, auto


class PalletteElementCategory(IntEnum):
    COLOR = auto()
    THICK = auto()
    THIN = auto()


class PalletteElement:
    """
    パレットの要素

    Attributes
    ----------
    color : tuple
        色(BGR)
    position : tuple(tuple(int, int))
        位置((start_x, start_y), (end_x, end_y))
    category : PalletteElementCategory
        カテゴリ
    """

    def __init__(self, color, position, category):
        self.color = color
        self.position = position
        self.category = category


class PaintTool:
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    YELLOW = (0, 255, 255)
    ORANGE = (0, 128, 255)
    PURPLE = (255, 0, 255)
    CYAN = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHTGRAY = (64, 64, 64)

    def __init__(self):
        self.line_color = self.BLACK
        self.line_width = 1
        self.is_drawing = False
        self.width = 512
        self.height = 512
        self.canvas = self.init_img(self.width, self.height, self.WHITE)
        self.img = self.canvas.copy()
        self.pallette_list = self.init_pallette_list()
        self.pallette = self.init_pallette()

        # 前回のカーソル値
        self.pre_x = 0
        self.pre_y = 0
        cv2.namedWindow('paint_tool')

    def init_img(self, width, height, color):
        """
        与えられた引数に基づいて画像を初期化

        Parameters
        ----------
        width : int
            画像の幅
        height : int
            画像の高さ
        color : tuple
            画像の色(BGR)
            cv2を使用しているためBGRであることに注意! RGBではない
        """
        img = np.zeros((height, width, 3), np.uint8)
        img[:] = color
        return img

    def init_pallette_list(self):
        """
        パレットリストを初期化する
        """
        choices = [
            (self.RED, PalletteElementCategory.COLOR),
            (self.GREEN, PalletteElementCategory.COLOR),
            (self.BLUE, PalletteElementCategory.COLOR),
            (self.YELLOW, PalletteElementCategory.COLOR),
            (self.ORANGE, PalletteElementCategory.COLOR),
            (self.BLACK, PalletteElementCategory.COLOR),
            (self.LIGHTGRAY, PalletteElementCategory.THICK),
            (self.LIGHTGRAY, PalletteElementCategory.THIN),
        ]
        pallette_list = []
        for i, color_category in enumerate(choices):
            pallette_list.append(PalletteElement(
                color_category[0],
                ((0, self.width // 8 * i),
                 (self.width // 8, self.width // 8 * (i + 1))),
                color_category[1]
            )
            )
        return pallette_list

    def init_pallette(self):
        pallette = self.init_img(self.width // 8, self.height, self.WHITE)
        for pallette_element in self.pallette_list:
            if pallette_element.category == PalletteElementCategory.COLOR:
                cv2.rectangle(pallette, pallette_element.position[0],
                              pallette_element.position[1], pallette_element.color, -1)
            elif pallette_element.category == PalletteElementCategory.THICK:
                cv2.circle(pallette, (pallette_element.position[0][0] + pallette_element.position[1][0] // 2,
                           pallette_element.position[0][1] + (
                    pallette_element.position[1][1] - pallette_element.position[0][1]) // 2), self.width // 18, pallette_element.color, -1)
            elif pallette_element.category == PalletteElementCategory.THIN:
                cv2.circle(pallette, (pallette_element.position[0][0] + pallette_element.position[1][0] // 2,
                           pallette_element.position[0][1] + (
                    pallette_element.position[1][1] - pallette_element.position[0][1]) // 2), self.width // 24, pallette_element.color, thickness=-1)
        return pallette

    def callback(self, event, x, y, flags, param):
        """
        左クリックをしている間、canvasにlineを引く。
        右クリックでcanvasをクリアする。
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.is_drawing = True
            for pallette_element in self.pallette_list:
                if pallette_element.category == PalletteElementCategory.COLOR:
                    if x in range(pallette_element.position[0][0], pallette_element.position[1][0]) and y in range(
                            pallette_element.position[0][1], pallette_element.position[1][1]):
                        self.line_color = pallette_element.color
                        break
                elif pallette_element.category == PalletteElementCategory.THICK:
                    if x in range(pallette_element.position[0][0], pallette_element.position[1][0]) and y in range(
                            pallette_element.position[0][1], pallette_element.position[1][1]):
                        self.line_width += 1
                        break
                elif pallette_element.category == PalletteElementCategory.THIN:
                    if x in range(pallette_element.position[0][0], pallette_element.position[1][0]) and y in range(
                            pallette_element.position[0][1], pallette_element.position[1][1]):
                        self.line_width -= 1
                        break
            self.pre_x = x
            self.pre_y = y
        elif event == cv2.EVENT_LBUTTONUP:
            self.is_drawing = False
        elif event == cv2.EVENT_MOUSEMOVE and self.is_drawing:
            cv2.line(self.canvas, (self.pre_x, self.pre_y),
                     (x, y), self.line_color, self.line_width)
            self.pre_x = x
            self.pre_y = y
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.canvas = self.init_img(self.width, self.height, self.WHITE)

        self.img = self.canvas.copy()
        # img にpalletteを重ねる
        self.img[:, 0:self.width // 8] = self.pallette

    def run(self):
        cv2.setMouseCallback('paint_tool', self.callback)
        while True:
            cv2.imshow('paint_tool', self.img)
            if cv2.waitKey(10) == ord('q'):
                break
        cv2.destroyAllWindows()


def main():
    paint_tool = PaintTool()
    paint_tool.run()


if __name__ == '__main__':
    main()