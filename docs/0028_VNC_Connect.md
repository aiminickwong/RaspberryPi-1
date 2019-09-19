# VNC Connect

## 参考文档

* [VNC (Virtual Network Computing)](https://www.raspberrypi.org/documentation/remote-access/vnc/)

## 基本操作

* sudo apt-get update
* sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer
* sudo raspi-config
  * Navigate to `Interfacing Options`.
  * `VNC` -> `Yes`.
* 下载[VNC viewer](https://www.realvnc.com/en/connect/download/viewer/)
  * 设置登录账号、密码即可连接；
    * 账号：pi；
    * 密码：raspberry；