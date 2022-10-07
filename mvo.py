import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time

img1 = cv.imread('t.jpg')
img2 = cv.imread('t+1.jpg')

gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

corners1 = cv.goodFeaturesToTrack(gray1, 25, 0.01, 10)

corners1 = np.int0(corners1)

p0 = []
for x in corners1:
    for y in x:
        p0.append([[np.float32(y[0]), np.float32(y[1])]])
corners1 = np.array(p0)

corners2, st, err = cv.calcOpticalFlowPyrLK(gray1, gray2, corners1, None)

good_new = []
good_old = []
for i in range(0, len(corners2)):
    if st[i] == 1 and corners2[i][0][0] > 0 and corners2[i][0][1] > 0:
        good_new.append(corners2[i])
        good_old.append(corners1[i])

E, mask = cv.findEssentialMat(np.array(good_old), np.array(good_new), 1.0, (0., 0.), 0)

final_new = []
final_old = []
for i in range(0, len(mask)):
    if mask[i] == 1:
        final_new.append(good_new[i])
        final_old.append(good_old[i])

#

retval, R, t, mask = cv.recoverPose(E, np.array(final_old), np.array(final_new), focal=1.0, pp=(0., 0.))
# R_f = R
# t_f = t

# scale = 15
# t_f = t_f + scale*(np.matmul(R_f, t))
# R_f = np.matmul(R, R_f)

# x = int(t_f[0]) + 300
# y = int(t_f[2]) + 100
# print(x, y)
#


color = np.random.randint(0, 255, (1000, 3))
mask = np.zeros_like(img1)
for i, (new, old) in enumerate(zip(final_new, final_old)):
    a, b = new.ravel()
    c, d = old.ravel()
    cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)

    cv.circle(img2, (int(a), int(b)), 5, color[i].tolist(), -1)
        
img = cv.add(img2, mask)


cv.imshow('frame', img)
cv.waitKey()