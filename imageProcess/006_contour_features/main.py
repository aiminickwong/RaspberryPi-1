#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

img = cv2.imread('capture.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
binary,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)
print(M)

rows,cols = img.shape[:2]
[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
img2 = cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)

cv2.imshow("0",binary)
cv2.imshow("1",img)
cv2.imshow("2",img2)
cv2.waitKey(0)

