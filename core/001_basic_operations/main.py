#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

img = cv2.imread('capture.jpg', cv2.IMREAD_UNCHANGED)

px = img[100,100]
print(px)

blue = img[100,100,0]
print(blue)

print(img.shape)
print(img.size)
print(img.dtype)
