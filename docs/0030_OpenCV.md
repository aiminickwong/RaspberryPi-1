# OpenCV

## 参考文档

* [ImportError: libcblas.so.3: cannot open shared object file: No such file or directory](https://stackoverflow.com/questions/53347759/importerror-libcblas-so-3-cannot-open-shared-object-file-no-such-file-or-dire)
* [OpenCV-Python Tutorials](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html)
* [OpenCV-Python中文教程](https://www.kancloud.cn/aollo/aolloopencv)

## python3 Install OpenCV

* `sudo pip3 install opencv-python`
* `sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test`

## python3 import cv2

```
pi@raspberrypi:~ $ python3
Python 3.7.3 (default, Apr  3 2019, 05:39:12)
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>>
```

## usb camera

* `sudo apt-get install fswebcam`
* `fswebcam image.jpg`
* `fswebcam -r 1280x720 image2.jpg`

## Learning source code

[OpenCV_Code](https://github.com/ZengjfOS/RaspberryPi/tree/OpenCV_Code)