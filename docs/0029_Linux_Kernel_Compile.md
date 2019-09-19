# Linux Kernel Compile

## 参考文档

* [Kernel building](https://www.raspberrypi.org/documentation/linux/kernel/building.md)

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
