import numpy as np
from icecream import ic

data1 = [6, 7.5, 8, 0.1, 1]
ary1 = np.array(data1)

ic(ary1)

ic(ary1 * 10)
ic(ary1 + ary1)
ic(ary1 - ary1)
ic(ary1 * ary1)
ic(ary1 / ary1)

ary1[2] = 7
ic(ary1)

ary_slice = ary1[2:4]
ic(ary_slice)

ary_slice[0] = 4
ic(ary_slice)
ic(ary1)

ary1[3:5] = 9
ic(ary1)
ic(ary_slice)

n = 10
x = [-1 + 2 * i / n for i in range(n)]
y = x
z = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        z[i][j] = 0.5 * (x[i] * x[i] + y[j] * y[j])
ic(x)
ic(y)
ic(z)

points = np.arange(-1, 1, 0.01)
xs, ys = np.meshgrid(points, points)
ic(xs)
ic(ys)
zs = 0.5 * (xs * xs + ys * ys)
ic(zs)

import cv2
cv2.namedWindow("display_zs")
cv2.imshow("display_zs", zs)
cv2.waitKey(0)
cv2.destroyAllWindows()
