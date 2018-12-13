# Dynamic Device Tree

## 参考文档

* [Device tree future](https://elinux.org/Device_tree_future#Material_to_review_before_the_conference)
* [Device Tree Plumbers 2015 Dynamic DT and tools](https://elinux.org/images/f/fa/Plumbers_2015_dt_DT-plumbers-2015.pdf)
* [Device Tree Usage](https://elinux.org/Device_Tree_Usage)
* [u-boot中fdt命令的使用](https://blog.csdn.net/voice_shen/article/details/7441894)
* [5.9.7. Flattened Device Tree support](https://www.denx.de/wiki/DULG/UBootCmdFDT)
* [U-Boot Flattened Device Tree](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841676/U-Boot+Flattened+Device+Tree)
* [Device Tree Overlay Notes](https://www.kernel.org/doc/Documentation/devicetree/overlay-notes.txt)
* [[U-Boot] [PATCH v2 05/10] doc: Document how to apply fdt overlays](https://lists.denx.de/pipermail/u-boot/2017-August/302273.html)

## Understanding the compatible Property

Every node in the tree that represents a device is required to have the compatible property. compatible is the key an operating system uses to decide which device driver to bind to a device. `compatible` is a list of strings. The first string in the list specifies the exact device that the node represents in the form `"<manufacturer>,<model>"`. The following strings represent other devices that the device is compatible with.

理解`compatible`基本上就能理解设备树上外设控制器与外设驱动、外设驱动的match关系了，从而进入对应的驱动probe函数，设备树其他参数基本上就是对外设参数具体的描述，理解起来就简单了，读一下驱动里的获取参数以及解析过程，就知道为什么要填写这些参数了；

## OF(Open Firmware)

[linux/drivers/of/Kconfig](https://github.com/torvalds/linux/blob/master/drivers/of/Kconfig)

```Kconfig
menuconfig OF
    bool "Device Tree and Open Firmware support"
    help
      This option enables the device tree infrastructure.
      It is automatically selected by platforms that need it or can
      be enabled manually for unittests, overlays or
      compile-coverage.
```

## CONFIG_OF_DYNAMIC

[linux/drivers/of/Kconfig](https://github.com/torvalds/linux/blob/master/drivers/of/Kconfig)

```
# Hardly any platforms need this.  It is safe to select, but only do so if you
# need it.
config OF_DYNAMIC
    bool "Support for dynamic device trees" if OF_UNITTEST
    select OF_KOBJ
    help
      On some platforms, the device tree can be manipulated at runtime.
      While this option is selected automatically on such platforms, you
      can enable it manually to improve device tree unit test coverage.
```

## OF_OVERLAY

[linux/drivers/of/Kconfig](https://github.com/torvalds/linux/blob/master/drivers/of/Kconfig)

```
config OF_OVERLAY
    bool "Device Tree overlays"
    select OF_DYNAMIC
    select OF_FLATTREE
    select OF_RESOLVE
    help
      Overlays are a method to dynamically modify part of the kernel's
      device tree with dynamically loaded data.
      While this option is selected automatically when needed, you can
      enable it manually to improve device tree unit test coverage.
```

## U-Boot Device Tree Modify

fdt set - set node properties: `fdt set /amba/usb0 status "disabled"`

## 总结

* 目前在Linux内核中和U-Boot中都有看到可以修改设备的树的部分，U-Boot中可以用`fdt`命令工具参考直接修改，在Kenrel中修改可能要参考`dtoverlay`源代码处理；
  * 在新版本的U-Boot中，貌似可以通过`fdt apply`来直接应用设备树overlays：[Boot-time Device Tree Overlays with U-Boot Jul 24](http://irq5.io/2018/07/24/boot-time-device-tree-overlays-with-u-boot/)
  * 树莓派命令行工具：[`dtoverlay`](https://github.com/raspberrypi/userland/tree/master/host_applications/linux/apps/dtoverlay)
    * `run_cmd("dtc -I fs -O dtb -o '%s' /proc/device-tree 1>/dev/null 2>&1", overlay_file)`: [Debugging - random hints](https://elinux.org/Device_Tree_Reference)，这里可以通过dtc命令直接获取到当前运行时的dtb；
      ```
      pi@raspberrypi:/proc/device-tree $ ls
      #address-cells  compatible          memory         phy            system
      aliases         fixedregulator_3v3  memreserve     serial-number  thermal-zones
      axi             fixedregulator_5v0  model          #size-cells
      chosen          interrupt-parent    name           soc
      clocks          leds                __overrides__  __symbols__
      ```
    * 再逆向出数据并修改数据；
    * 再保存成原来的dtb；