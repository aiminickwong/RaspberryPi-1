# Linux Kernel Compile

## 参考文档

* [Kernel building](https://www.raspberrypi.org/documentation/linux/kernel/building.md)

## Source code

https://github.com/raspberrypi/linux

## steps

* `sudo apt-get install git bc bison flex libssl-dev`
* download kernel source code and `cd` to kernel root path
* `KERNEL=kernel7l`
* `make bcm2711_defconfig`
* `make -j4 zImage modules dtbs`
  * config dir: `arch/arm64/configs/bcm2711_defconfig`
  * overlay dir: `arch/arm/boot/dts/overlays`
  * dts dir: `arch/arm64/boot/dts/broadcom/bcm2711-rpi-4-b.dts`
  * function map：`System.map`
* `sudo make modules_install`
  ```
  INSTALL arch/arm/crypto/aes-arm-bs.ko
  INSTALL arch/arm/crypto/aes-arm.ko
  INSTALL arch/arm/crypto/sha1-arm-neon.ko
  INSTALL arch/arm/crypto/sha1-arm.ko
  [...省略]
  INSTALL sound/usb/6fire/snd-usb-6fire.ko
  INSTALL sound/usb/caiaq/snd-usb-caiaq.ko
  INSTALL sound/usb/hiface/snd-usb-hiface.ko
  INSTALL sound/usb/misc/snd-ua101.ko
  INSTALL sound/usb/snd-usb-audio.ko
  INSTALL sound/usb/snd-usbmidi-lib.ko
  DEPMOD  4.19.71-v7l
  ```
* `ls /lib/modules/`
  ```
  4.19.57+  4.19.57-v7+  4.19.57-v7l+  4.19.71-v7l  4.9.0-6-rpi
  ```
* `sudo cp arch/arm/boot/dts/*.dtb /boot/`
* `sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/`
* `sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/`
* `sudo cp arch/arm/boot/zImage /boot/$KERNEL.img`
* `sudo sync`
* `sudo reboot`
* `uname -a`
  ```
  Linux raspberrypi 4.19.71-v7l #1 SMP Mon Sep 9 12:24:09 BST 2019 armv7l GNU/Linux
  ```

## menuconfig

`make ARCH=arm64 CROSS_COMPILE=arm-linux-gnueabihf- menuconfig`

## Check version

* Current system version
  ```Console
  pi@raspberrypi:~/zengjf $ uname -a
  Linux raspberrypi 4.19.57-v7l+ #1244 SMP Thu Jul 4 18:48:07 BST 2019 armv7l GNU/Linux
  ```
* `head Makefile`
  ```Makefile
  # SPDX-License-Identifier: GPL-2.0
  VERSION = 4
  PATCHLEVEL = 19
  SUBLEVEL = 71
  EXTRAVERSION =
  NAME = "People's Front"
  
  # *DOCUMENTATION*
  # To see a list of typical targets execute "make help"
  # More info can be located in ./README
  ```
* 如上可知，由于重新编译的内核和系统本身的内核版本有差异，所以不能仅仅替换内核，这样会导致内核驱动模块加载失败，需要将内核相关文件全部进行替换：
  ```Shell
  make -j4 zImage modules dtbs
  sudo make modules_install
  sudo cp arch/arm/boot/dts/*.dtb /boot/
  sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
  sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/
  sudo cp arch/arm/boot/zImage /boot/$KERNEL.img
  ```