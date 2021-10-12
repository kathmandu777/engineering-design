import numpy as np
import cv2


class ToggleImg:
    def __init__(self, img1, img2):
        self.img_1 = img1
        self.img_2 = img2
        self.img = img1
        cv2.namedWindow('window')

    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.img = self.img_2 if np.array_equal(
                self.img, self.img_1) else self.img_1

    def run(self):
        cv2.setMouseCallback('window', self.callback)
        while True:
            cv2.imshow('window', self.img)
            if cv2.waitKey(10) & 0xFF == ord(' '):
                break
        cv2.destroyAllWindows()


def main():
    img1 = cv2.imread('./Lenna.jpg')
    img2 = cv2.imread('./Mandrill.jpg')
    toggle_img = ToggleImg(img1, img2)
    toggle_img.run()


if __name__ == '__main__':
    main()
