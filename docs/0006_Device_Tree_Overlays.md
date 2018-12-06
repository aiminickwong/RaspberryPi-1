# Device Tree Overlays

之前接触的设备树是固定的，每个引脚都是在设备树中固定配置好，编译完成以后不能在进行修改，当我们引出的引脚是固定的，想要对引脚复用的时候，这个缺陷就变得很明显了，譬如我们引出的引脚带有I2C或者GPIO两个可选功能，需要在运用到的时候在进行修改，这就要用到设备树的Overlays功能了。

## 参考文档

* [LWN 616859: 设备树动态叠加技术](http://tinylab.org/lwn-616859-device-tree-overlays/)
* [Device Trees, Overlays and Parameters](https://github.com/pickfire/rpi_doc/blob/master/configuration/device-tree.md)
* [设备树叠加层](https://source.android.google.cn/devices/architecture/dto/?hl=zh-cn)
* [树莓派 -- i2c学习 续（1） DeviceTree Overlay实例化rtc](https://blog.csdn.net/feiwatson/article/details/81072640)
* [Device Tree Overlay Notes](https://www.kernel.org/doc/Documentation/devicetree/overlay-notes.txt)

## 树莓派当前支持的dtbo

[Supported overlays and parameters](https://github.com/pickfire/rpi_doc/blob/master/configuration/device-tree.md#35-supported-overlays-and-parameters)

```Shell
pi@raspberrypi:/boot/overlays $ ls
adau1977-adc.dtbo                       dpi24.dtbo                     hy28b.dtbo                      mcp3202.dtbo             qca7000.dtbo                    spi1-1cs.dtbo
adau7002-simple.dtbo                    dwc2.dtbo                      i2c0-bcm2708.dtbo               media-center.dtbo        README                          spi1-2cs.dtbo
ads1015.dtbo                            dwc-otg.dtbo                   i2c1-bcm2708.dtbo               midi-uart0.dtbo          rotary-encoder.dtbo             spi1-3cs.dtbo
ads1115.dtbo                            enc28j60.dtbo                  i2c-bcm2708.dtbo                midi-uart1.dtbo          rpi-backlight.dtbo              spi2-1cs.dtbo
ads7846.dtbo                            enc28j60-spi2.dtbo             i2c-gpio.dtbo                   mmc.dtbo                 rpi-cirrus-wm5102.dtbo          spi2-2cs.dtbo
adv7282m.dtbo                           exc3000.dtbo                   i2c-mux.dtbo                    mpu6050.dtbo             rpi-dac.dtbo                    spi2-3cs.dtbo
adv728x-m.dtbo                          fe-pi-audio.dtbo               i2c-pwm-pca9685a.dtbo           mz61581.dtbo             rpi-display.dtbo                spi-gpio35-39.dtbo
akkordion-iqdacplus.dtbo                goodix.dtbo                    i2c-rtc.dtbo                    ov5647.dtbo              rpi-ft5406.dtbo                 spi-rtc.dtbo
allo-boss-dac-pcm512x-audio.dtbo        googlevoicehat-soundcard.dtbo  i2c-rtc-gpio.dtbo               papirus.dtbo             rpi-poe.dtbo                    superaudioboard.dtbo
allo-digione.dtbo                       gpio-fan.dtbo                  i2c-sensor.dtbo                 pi3-act-led.dtbo         rpi-proto.dtbo                  sx150x.dtbo
allo-katana-dac-audio.dtbo              gpio-ir.dtbo                   i2s-gpio28-31.dtbo              pi3-disable-bt.dtbo      rpi-sense.dtbo                  tc358743-audio.dtbo
allo-piano-dac-pcm512x-audio.dtbo       gpio-ir-tx.dtbo                iqaudio-dac.dtbo                pi3-disable-wifi.dtbo    rpi-tv.dtbo                     tc358743.dtbo
allo-piano-dac-plus-pcm512x-audio.dtbo  gpio-key.dtbo                  iqaudio-dacplus.dtbo            pi3-miniuart-bt.dtbo     rra-digidac1-wm8741-audio.dtbo  tinylcd35.dtbo
applepi-dac.dtbo                        gpio-no-bank0-irq.dtbo         iqaudio-digi-wm8804-audio.dtbo  pibell.dtbo              sc16is750-i2c.dtbo              uart0.dtbo
at86rf233.dtbo                          gpio-no-irq.dtbo               jedec-spi-nor.dtbo              piscreen2r.dtbo          sc16is752-i2c.dtbo              uart1.dtbo
audioinjector-addons.dtbo               gpio-poweroff.dtbo             justboom-dac.dtbo               piscreen.dtbo            sc16is752-spi1.dtbo             upstream-aux-interrupt.dtbo
audioinjector-ultra.dtbo                gpio-shutdown.dtbo             justboom-digi.dtbo              pisound.dtbo             sdhost.dtbo                     upstream.dtbo
audioinjector-wm8731-audio.dtbo         hd44780-lcd.dtbo               lirc-rpi.dtbo                   pitft22.dtbo             sdio-1bit.dtbo                  vc4-fkms-v3d.dtbo
audremap.dtbo                           hifiberry-amp.dtbo             ltc294x.dtbo                    pitft28-capacitive.dtbo  sdio.dtbo                       vc4-kms-kippah-7inch.dtbo
balena-fin.dtbo                         hifiberry-dac.dtbo             mbed-dac.dtbo                   pitft28-resistive.dtbo   sdtweak.dtbo                    vc4-kms-v3d.dtbo
bmp085_i2c-sensor.dtbo                  hifiberry-dacplus.dtbo         mcp23017.dtbo                   pitft35-resistive.dtbo   smi-dev.dtbo                    vga666.dtbo
dht11.dtbo                              hifiberry-digi.dtbo            mcp23s17.dtbo                   pps-gpio.dtbo            smi.dtbo                        w1-gpio.dtbo
dionaudio-loco.dtbo                     hifiberry-digi-pro.dtbo        mcp2515-can0.dtbo               pwm-2chan.dtbo           smi-nand.dtbo                   w1-gpio-pullup.dtbo
dionaudio-loco-v2.dtbo                  hy28a.dtbo                     mcp2515-can1.dtbo               pwm.dtbo                 spi0-cs.dtbo                    wittypi.dtbo
dpi18.dtbo                              hy28b-2017.dtbo                mcp3008.dtbo                    pwm-ir-tx.dtbo           spi0-hw-cs.dtbo
```

## 理解Overlay的使用方法

* 编写overlay dts: `rasp-rtc.dts`
  ```dts
  /dts-v1/;
  /plugin/;

  / {
       compatible = "brcm,bcm2835", "brcm,bcm2708", "brcm,bcm2709";

       fragment@0 {
          target = <&i2c1>;
          __overlay__ {
            #address-cells = <1>;
            #size-cells = <0>;
            rtc@68 {
                    compatible = "maxim,ds3231";
                    reg = <0x68>;
                    #address-cells = <2>;
                    #size-cells = <1>;
            };      
          };
       };
    };
  ```
* 编译: `dtc -I dts -O dtb -o /boot/overlays/rasp-rtc.dtbo rasp-rtc.dts`；
* 将编译出来的`rasp-rtc.dtbo`放到`/boot/overlays`；
* 更新 `/boot/config.txt`:
  ```
  dtparam=i2c_arm=on                # i2c interface
  dtoverlay=rasp-rtc                # Overlay
  ```