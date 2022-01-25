import os
import numpy as np
import cv2
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from img_feature_extraction import *

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

LINE_WIDTH = 3
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
BLACK = (0, 0, 0)

# 抽出する色の特徴値
GREEN_MIN_HUE = 30
GREEN_MAX_HUE = 90
SATURATION_THRESHOLD = 128


@app.route("/send", methods=["POST"])
def send():  # ファイル読み込み
    img_file = request.files["img_file"]
    filename = secure_filename(img_file.filename)

    p_fname = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    img_file.save(p_fname)
    raw_img = cv2.imread(p_fname)
    raw_img_url = os.path.join(app.config["UPLOAD_FOLDER"], "raw_" + filename)
    if os.path.exists(raw_img_url):
        os.remove(raw_img_url)
    os.rename(p_fname, raw_img_url)

    after_img = raw_img.copy()
    mask = mask_img(after_img, GREEN_MIN_HUE, GREEN_MAX_HUE, SATURATION_THRESHOLD)
    contours = get_contours(mask)
    if contours:
        max_contour, _ = get_max_contour(contours)
        cv2.drawContours(after_img, [max_contour], 0, RED, LINE_WIDTH)
        line_points = get_line_points_from_contour(max_contour, after_img)
        cv2.line(after_img, line_points[0], line_points[1], BLACK, LINE_WIDTH)
    after_img_url = os.path.join(app.config["UPLOAD_FOLDER"], "after_" + filename)
    cv2.imwrite(after_img_url, after_img)
    time = int(os.stat(after_img_url).st_mtime)  # 保存時刻を記録
    return render_template(
        "index.html",
        title="After Processing the Image",
        raw_img_url=raw_img_url,
        after_img_url=after_img_url + "?" + str(time),
    )


# 画像処理したものを強制更新してブラウザに表示
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/")
def index():
    return render_template("index.html", title="Test by Flask and OpenCV")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
