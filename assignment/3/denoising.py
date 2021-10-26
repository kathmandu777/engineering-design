import cv2
import numpy as np
import io
import picamera


def add_salt_pepper_noise(img, prob=0.01):
    """
    与えられた画像に一定の確率(prob)でノイズをかける。
    入力画像と同じサイズのランダム配列を生成し、その要素が確立以下であればノイズを加える。

    Parameters
    ----------
    img : ndarray
        入力画像
    prob : float
        ノイズをかける確率
    """
    row, col, _ = img.shape
    random_array = np.random.rand(row, col)
    img[random_array < prob] = (255, 255, 255)
    return img


def main():
    """
    カメラから画像を入力してオリジナル画像、ノイズをかけた画像、median filterでノイズ除去した画像を表示する
    """
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
            noised_img = add_salt_pepper_noise(img)
            denoised_img = cv2.medianBlur(noised_img, 3)
            merged_img = np.hstack((img, noised_img, denoised_img))
            cv2.imshow("merged_img", merged_img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cv2.imwrite("merged_img.jpg", merged_img)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
