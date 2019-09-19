#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

img = cv2.imread('in.png', cv2.IMREAD_UNCHANGED)

cv2.imshow('image',img)
cv2.waitKey(0)

cv2.imwrite('out.png',img)
