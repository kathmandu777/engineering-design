import numpy as np
import cv2


class SelectImgArea:
    def __init__(self, img):
        self.origin_img = img
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.is_drawing = False
        cv2.namedWindow('window')

    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.is_drawing = True
        if event == cv2.EVENT_LBUTTONUP:
            self.is_drawing = False
        if self.is_drawing and event == cv2.EVENT_MOUSEMOVE:
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
    select_img = SelectImgArea(img)
    select_img.run()


if __name__ == '__main__':
    main()
