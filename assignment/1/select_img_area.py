import numpy as np
import cv2


class SelectImgArea:
    def __init__(self, img):
        self.origin_img = img
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.is_draw = False
        cv2.namedWindow('window')

    def callback(self, event, x, y, flags, param):
        """
        左クリックされている間は原点(左上)からマウスのポインターがある地点の範囲の画像を描画（範囲外は黒ぬり）
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.is_draw = True
        if event == cv2.EVENT_LBUTTONUP:
            self.is_draw = False
        if self.is_draw and event == cv2.EVENT_MOUSEMOVE:
            img = np.zeros((self.height, self.width, 3), np.uint8)
            img[0:y, 0:x] = self.origin_img[0:y, 0:x]
            self.img = img

    def run(self):
        cv2.setMouseCallback('window', self.callback)
        while True:
            cv2.imshow('window', self.img)
            if cv2.waitKey(10) & 0xFF == ord(' '):
                break
        cv2.destroyAllWindows()


def main():
    img = cv2.imread('./Lenna.jpg')
    select_img_area = SelectImgArea(img)
    select_img_area.run()


if __name__ == '__main__':
    main()
