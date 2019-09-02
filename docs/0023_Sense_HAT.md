# Sense HAT

## 参考文档

* [rpi-sense firmware souce code](https://github.com/raspberrypi/rpi-sense)
* [rpi-sense schematic](https://www.raspberrypi.org/documentation/hardware/sense-hat/images/Sense-HAT-V1_0.pdf)
* [AVR MCU Reference Manual](https://www.microchip.com/wwwproducts/en/ATTINY88)
  * http://ww1.microchip.com/downloads/en/DeviceDoc/doc8008.pdf
* [Getting started with the Sense HAT](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat)

## RPI 4插入Sense HAT无法使用

* 参考文档：[Buster won't boot headless with the Sense Hat attached](https://www.raspberrypi.org/forums/viewtopic.php?t=243949)
* 修改：`/boot/config.txt`
  * removed the "#" in front of the line "hdmi_force_hotplug=1" and now the Raspberry Pi is booting attached with the SenseHAT.

## rpi-sense firmware 

* 使用`raspi-config`打开I2C、SPI接口；
* `sudo apt-get update`
* `sudo apt-get install sense-hat`
  * 示例程序：`/usr/src/sense-hat/examples`
* `sudo apt-get install gcc-avr avr-libc avrdude`
* `sudo reboot`
* `cd ~`
* `git clone https://github.com/raspberrypi/rpi-sense`
* `make`
* `make flash`