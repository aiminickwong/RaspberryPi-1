# SoC Device Tree

## proc file

* `cat /proc/device-tree/compatible`
  ```
  raspberrypi,4-model-bbrcm,bcm2838
  ```
* `cat /proc/device-tree/model`
  ```
  Raspberry Pi 4 Model B Rev 1.1r
  ```

## compile dts

* `KERNEL=kernel7l`
* `make bcm2711_defconfig`
* `make -j4 dtbs`
* `sudo cp arch/arm/boot/dts/bcm2711-rpi-4-b.dtb /boot/bcm2711-rpi-4-b.dtb`

## default dts

* `cat arch/arm64/boot/dts/broadcom/bcm2711-rpi-4-b.dts`
  ```
  #define RPI364
  
  #include "../../../../arm/boot/dts/bcm2711-rpi-4-b.dts"
  ```
* cat `arch/arm/boot/dts/bcm2711-rpi-4-b.dts`
  ```
  /dts-v1/;
  
  #include "bcm2711.dtsi"
  #include "bcm2711-rpi.dtsi"
  #include "bcm283x-rpi-csi1-2lane.dtsi"
  
  / {
      compatible = "raspberrypi,4-model-b", "brcm,bcm2838";
      model = "Raspberry Pi 4 Model B";
  
      memory {
          device_type = "memory";
          reg = <0x0 0x0 0x0>;
      };
  
      chosen {
          bootargs = "coherent_pool=1M 8250.nr_uarts=1 cma=64M zengjf ";
      };
  
      aliases {
          serial0 = &uart1;
          serial1 = &uart0;
          mmc0 = &emmc2;
          mmc1 = &mmcnr;
          mmc2 = &sdhost;
          i2c3 = &i2c3;
          i2c4 = &i2c4;
          i2c5 = &i2c5;
          i2c6 = &i2c6;
          /delete-property/ ethernet;
          /delete-property/ intc;
          ethernet0 = &genet;
      };
  };

  [...省略]
  ```
* 添加`zengjf`节点进行调试确认
  ```
  /dts-v1/;
  
  #include "bcm2711.dtsi"
  #include "bcm2711-rpi.dtsi"
  #include "bcm283x-rpi-csi1-2lane.dtsi"
  
  / {
      compatible = "raspberrypi,4-model-b", "brcm,bcm2838";
      model = "Raspberry Pi zengjf 4 Model B ";
  
      memory {
          device_type = "memory";
          reg = <0x0 0x0 0x0>;
      };
  
      zengjf{                           /* 添加节点 */
          name = "zengjf";
      };
  
      chosen {
          bootargs = "coherent_pool=1M 8250.nr_uarts=1 cma=64M";
      };
  
      aliases {
          serial0 = &uart1;
          serial1 = &uart0;
          mmc0 = &emmc2;
          mmc1 = &mmcnr;
          mmc2 = &sdhost;
          i2c3 = &i2c3;
          i2c4 = &i2c4;
          i2c5 = &i2c5;
          i2c6 = &i2c6;
          /delete-property/ ethernet;
          /delete-property/ intc;
          ethernet0 = &genet;
      };
  };
  ```
* `ls /proc/device-tree`
  ```
  '#address-cells'   fixedregulator_3v3   name            __symbols__
   aliases           fixedregulator_5v0   __overrides__   system
   arm-pmu           hat                  phy             thermal-zones
   axi               interrupt-parent     scb             timer
   chosen            leds                 sd_io_1v8_reg   v3dbus
   clocks            memory               serial-number   zengjf   <--------添加的节点
   compatible        memreserve          '#size-cells'
   cpus              model                soc
  ```
* `cat /proc/cmdline`
  ```
  coherent_pool=1M 8250.nr_uarts=0 cma=64M zengjf  bcm2708_fb.fbwidth=1280 bcm2708_fb.fbheight=720 bcm2708_fb.fbswap=1 smsc95xx.macaddr=DC:A6:32:17:47:91 vc_mem.mem_base=0x3ec00000 vc_mem.mem_size=0x40000000  dwc_otg.lpm_enable=1 console=ttyS0,115200 console=tty1 root=PARTUUID=48597d87-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles modules-load=dwc2,g_ether
  ```

## i2c1 dts

* i2c1控制器注册
  * `bcm2711-rpi-4-b.dts`
    * `bcm2711.dtsi`
      * `bcm2838.dtsi`
        * `bcm283x.dtsi`
          ```
          i2c1: i2c@7e804000 {
              compatible = "brcm,bcm2835-i2c";
              reg = <0x7e804000 0x1000>;
              interrupts = <2 21>;
              clocks = <&clocks BCM2835_CLOCK_VPU>;
              #address-cells = <1>;
              #size-cells = <0>;
              status = "disabled";
          };
          ```
* 添加默认设备，默认是没有添加设备的
  * `bcm2711-rpi-4-b.dts`
    * `bcm2711-rpi.dtsi`
      * `bcm2708-rpi.dtsi`
        ```
        &i2c1 {
            status = "disabled";
        
            eeprom@50 {
                compatible = "24c02";
                reg = <0x50>;
                status = "okay";
            };
        };
        ```
* 编译拷贝覆盖boot分区dts：`sudo cp arch/arm/boot/dts/bcm2711-rpi-4-b.dtb /boot/bcm2711-rpi-4-b.dtb`
* 运行时查看设备树情况
  ```Console
  root@raspberrypi:/proc/device-tree/soc/i2c@7e804000# pwd
  /proc/device-tree/soc/i2c@7e804000
  root@raspberrypi:/proc/device-tree/soc/i2c@7e804000# ls
  '#address-cells'   eeprom@50         lsm9ds1-accel6a   pinctrl-0      '#size-cells'
   clock-frequency   hts221-humid@5f   lsm9ds1-magn@1c   pinctrl-names   status
   clocks            interrupts        name              reg
   compatible        lps25h-press@5c   phandle           rpi-sense@46
  ```

## __overrides__

* "bcm2708-rpi.dtsi"
  * "bcm2711-rpi.dtsi"
    * "bcm2708-rpi.dtsi"
      ```
      __overrides__ {
          cache_line_size;

          uart0 = <&uart0>,"status";
          uart1 = <&uart1>,"status";
          i2s = <&i2s>,"status";
          spi = <&spi0>,"status";
          i2c0 = <&i2c0>,"status";
          i2c1 = <&i2c1>,"status";
          i2c2_iknowwhatimdoing = <&i2c2>,"status";
          i2c0_baudrate = <&i2c0>,"clock-frequency:0";
          i2c1_baudrate = <&i2c1>,"clock-frequency:0";
          i2c2_baudrate = <&i2c2>,"clock-frequency:0";

          audio = <&audio>,"status";
          watchdog = <&watchdog>,"status";
          random = <&random>,"status";
          sd_overclock = <&sdhost>,"brcm,overclock-50:0";
          sd_force_pio = <&sdhost>,"brcm,force-pio?";
          sd_pio_limit = <&sdhost>,"brcm,pio-limit:0";
          sd_debug     = <&sdhost>,"brcm,debug";
          sdio_overclock = <&mmc>,"brcm,overclock-50:0",
                   <&mmcnr>,"brcm,overclock-50:0";
          axiperf      = <&axiperf>,"status";
      };
      ```
* [What does raspi-config do when you enable i2c?](https://raspberrypi.stackexchange.com/questions/28935/what-does-raspi-config-do-when-you-enable-i2c): `/boot/config.txt`
  ```
  # Uncomment some or all of these to enable the optional hardware interfaces
  dtparam=i2c_arm=on
  #dtparam=i2s=on
  dtparam=spi=on
  ```
* `cat /proc/device-tree/soc/i2c@7e804000/status`
  ```
  okay
  ```
* https://github.com/raspberrypi/userland
  * host_applications/linux/apps/dtoverlay
    * `dtoverlay`是覆盖整体dts；
    * `dtparam`主要是处理`__overrides__`中的部分；
  * Linux Kenrel Driver: `OF_CONFIGFS`
    * [0013_dtoverlay.md](0013_dtoverlay.md)