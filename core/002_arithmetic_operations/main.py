#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

img1 = cv2.imread('capture.jpg')
img2 = cv2.imread('opencv-logo-white.png')

print(img1.shape)
print(img2.shape)

img2 = cv2.resize(img2, (320, 240), interpolation=cv2.INTER_CUBIC)
print(img1.shape)
print(img2.shape)

dst = cv2.addWeighted(img1,0.7,img2,0.3,0)

cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
