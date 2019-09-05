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

## lsm9ds1 i2c device

* https://github.com/FrankBau/raspi-repo-manifest/wiki/device-tree#device-tree-overlays-sense-hat
  ```
  // rpi-sense HAT
  /dts-v1/;
  /plugin/;
  
  / {
  	compatible = "brcm,bcm2708", "brcm,bcm2709";
  
  	fragment@0 {
  		target = <&i2c1>;
  		__overlay__ {
  			#address-cells = <1>;
  			#size-cells = <0>;
  			status = "okay";
  
  			rpi-sense@46 {
  				compatible = "rpi,rpi-sense";
  				reg = <0x46>;
  				keys-int-gpios = <&gpio 23 1>;
  				status = "okay";
  			};
  
  			lsm9ds1-magn@1c {
  				compatible = "st,lsm9ds1-magn";
  				reg = <0x1c>;
  				status = "okay";
  			};
  
  			lsm9ds1-accel6a {
  				compatible = "st,lsm9ds1-accel";
  				reg = <0x6a>;
  				status = "okay";
  			};
  
  			lps25h-press@5c {
  				compatible = "st,lps25h-press";
  				reg = <0x5c>;
  				status = "okay";
  			};
  
  			hts221-humid@5f {
  				compatible = "st,hts221-humid";
  				reg = <0x5f>;
  				status = "okay";
  			};
  		};
  	};
  };
  ```
* 检查设备
  ```
  root@raspberrypi:/sys/bus/i2c/devices# ls
  1-001c  1-0046  1-005c  1-005f  1-006a  i2c-1
  root@raspberrypi:/sys/bus/i2c/devices# cat 1-001c/name
  lsm9ds1-magn
  root@raspberrypi:/sys/bus/i2c/devices# cat 1-0046/name
  rpi-sense
  root@raspberrypi:/sys/bus/i2c/devices# cat 1-005c/name
  lps25h-press
  root@raspberrypi:/sys/bus/i2c/devices# cat 1-005f/name
  hts221-humid
  root@raspberrypi:/sys/bus/i2c/devices# cat 1-006a/name
  lsm9ds1-accel
  ```
* `/proc/device-tree/soc/i2c@7e804000/lsm9ds1-magn@1c`
* `cat /proc/device-tree/soc/i2c@7e804000/lsm9ds1-magn@1c/compatible`
  * "st,lsm9ds1-magn"
* diff from ST [linux driver](https://www.st.com/en/mems-and-sensors/lsm9ds1.html#)
  ```diff
  diff --git a/st_magn/st_mag3d_i2c.c b/st_magn/st_mag3d_i2c.c
  index e8c7d0a..4741f3b 100644
  --- a/st_magn/st_mag3d_i2c.c
  +++ b/st_magn/st_mag3d_i2c.c
  @@ -66,7 +66,7 @@ static const struct of_device_id st_mag3d_id_table[] = {
                  .compatible = "st,lis3mdl_magn",
          },
          {
  -               .compatible = "st,lsm9ds1_magn",
  +               .compatible = "st,lsm9ds1-magn",
          },
          {},
   };
  ```
* [lsm9ds1 driver](https://github.com/ZengjfOS/RaspberryPi/tree/lsm9ds1_driver)
  * [Build Kernel Modules](0024_Kernel_Modules.md)
  * `make`
  * `sudo ./modules.sh insmod`
* 确认设备节点：`/dev/iio:device0`
* sysfs没有trigger
  ```
  pi@raspberrypi:~ $ ls /sys/bus/iio/devices/
  iio:device0
  pi@raspberrypi:~ $ ls /sys/bus/iio/devices/iio\:device0
  current_timestamp_clock  in_magn_x_raw    in_magn_y_raw    in_magn_z_raw    name     power               sampling_frequency_available  uevent
  dev                      in_magn_x_scale  in_magn_y_scale  in_magn_z_scale  of_node  sampling_frequency  subsystem
  ```
* [iio-tools](https://github.com/ZengjfOS/iio-tools)
  * `./iio_generic_buffer -N 0 -g`
    ```
    iio device number being used is 0
    trigger-less mode selected
    Problem reading scan element information
    diag /sys/bus/iio/devices/iio:device0
    ```
  * 没有生成`/sys/bus/iio/devices/iio:device0/scan_elements`导致的，经分析代码发现，由于没有使用中断导致没有注册buffer导致的；

## Sense HAT API

* https://pythonhosted.org/sense-hat/api/
* https://github.com/astro-pi/python-sense-hat/blob/master/examples/README.md

