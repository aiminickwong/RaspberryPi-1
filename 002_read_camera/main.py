#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time
import sys


cap = cv2.VideoCapture(0)

print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if (sys.version_info > (3, 0)):

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)      #sirka videa 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)     #vyska videa

else:
    pass
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, frame = cap.read()

cv2.imwrite("capture.jpg", frame)               # write picture 

cap.release()
