# GPIO Interrupt

## 参考文档

* [gpioIrq](https://github.com/OnionIoT/gpioIrq)
* [python-sysfs-gpio](https://github.com/derekstavis/python-sysfs-gpio)
* [BeagleBone Black: How to Get Interrupts Through Linux GPIO](https://www.linux.com/tutorials/beaglebone-black-how-get-interrupts-through-linux-gpio/)

## 测试GPIO

用GPIO21也就是排针的P40引脚，不用做其他的配置，上来就能直接export使用

```
root@raspberrypi:# cd /sys/class/gpio
root@raspberrypi:/sys/class/gpio# echo 21 > export
root@raspberrypi:/sys/class/gpio# ls
export  gpio21  gpiochip0  unexport
root@raspberrypi:/sys/class/gpio# cd gpio21/
root@raspberrypi:/sys/class/gpio/gpio21# ls
active_low  device  direction  edge  power  subsystem  uevent  value
root@raspberrypi:/sys/class/gpio/gpio21# cat value
0
root@raspberrypi:/sys/class/gpio/gpio21# cat direction
in
root@raspberrypi:/sys/class/gpio/gpio21# cat value
0
root@raspberrypi:/sys/class/gpio/gpio21# cat value
1
```

## 测试IRQ

* git clone https://github.com/OnionIoT/gpioIrq
* make
* 测试中断
  ```
  root@raspberrypi:/home/pi/zengjf/gpioIrq# ./gpioIrq 21
  
  poll() GPIO 21 interrupt occurred
          read value: '0'
  .
  poll() GPIO 21 interrupt occurred
          read value: '1'
  
  poll() GPIO 21 interrupt occurred
          read value: '0'
  .
  ```

## Android.mk

* https://github.com/ZengjfOS/RaspberryPi/blob/gpioIrq/Android.mk
  ```
  LOCAL_PATH := $(call my-dir)
  
  include $(CLEAR_VARS)
  
  LOCAL_CFLAGS += -Wno-unused-variable -Wno-unused-parameter -Wno-format
  LOCAL_MODULE    := gpioIrq 
  LOCAL_SRC_FILES := gpioIrq.c
  
  include $(BUILD_EXECUTABLE)
  ```