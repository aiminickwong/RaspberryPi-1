# dtoverlay

## 参考文档

* [dtbocfg - Device Tree Blob Overlay Configuration File System](https://github.com/ikwzm/dtbocfg)
* [Instructions for Dynamically Loading Device Tree Overlays into Linux Kernel](https://www.96boards.org/documentation/consumer/dragonboard/dragonboard410c/guides/dt-overlays.md.html)

## Source Code

https://github.com/raspberrypi/userland/tree/master/host_applications/linux/apps/dtoverlay

## Linux Overlays Dynamically

* 查看内核配置挂在点
  ```
  pi@raspberrypi:~ $ mount | grep config
  configfs on /sys/kernel/config type configfs (rw,relatime)
  ```
  * `mount -t configfs none /sys/kernel/config`
* 查看目录 
  ```
  pi@raspberrypi:~ $ ls /sys/kernel/config
  device-tree  usb_gadget
  ```
* overlays dtparam 
  ```
  pi@raspberrypi:~ $ ls /sys/kernel/config/device-tree/overlays/
  0_dtparam
  pi@raspberrypi:~ $ ls /sys/kernel/config/device-tree/overlays/0_dtparam/
  dtbo  path  status
  ```
* `sudo dtparam -v i2c_arm=on`
  ```
  pi@raspberrypi:~/zengjf/copy $ sudo dtparam -v i2c_arm=on
  run_cmd: which dtoverlay-pre >/dev/null 2>&1 && dtoverlay-pre
  run_cmd: dtc -I fs -O dtb -o '/tmp/.dtoverlays/base.dtb' /proc/device-tree 1>/dev/null 2>&1
  DTOVERLAY[debug]: Found override i2c_arm
  DTOVERLAY[debug]:   override i2c_arm: string target 'status'
  DTOVERLAY[debug]: delete_node(/__symbols__)
  DTOVERLAY[debug]: Wrote 162 bytes to '/tmp/.dtoverlays/0_dtparam.dtbo'
  DTOVERLAY[debug]: Wrote 174 bytes to '/sys/kernel/config/device-tree/overlays/0_dtparam/dtbo'
  run_cmd: which dtoverlay-post >/dev/null 2>&1 && dtoverlay-post
  ```
* dtc -I dtb -O dts -o ~/zengjf/0_dtparam.dts 0_dtparam.dtbo
* dtc -I dtb -O dts -o ~/zengjf/base.dts base.dtb
* rpi dts: https://github.com/raspberrypi/linux/tree/rpi-4.19.y/arch/arm/boot/dts/overlays

## dtparam/dtoverlay

* 两者区别：
  ```Shell
  pi@raspberrypi:/proc/device-tree $ which dtparam
  /usr/bin/dtparam
  pi@raspberrypi:/proc/device-tree $ ls -al /usr/bin/dtparam
  lrwxrwxrwx 1 root root 21 Nov 12 17:26 /usr/bin/dtparam -> /opt/vc/bin/dtoverlay
  pi@raspberrypi:/proc/device-tree $ ls -al /usr/bin/dtoverlay
  lrwxrwxrwx 1 root root 21 Nov 12 17:26 /usr/bin/dtoverlay -> /opt/vc/bin/dtoverlay
  ```
* 帮助文档：
  ```C
  static void usage(void)
  {
      printf("Usage:\n");
      if (strcmp(cmd_name, "dtparam") == 0)
      {
         printf("  %s                Display help on all parameters\n", cmd_name);
         printf("  %s <param>=<val>...\n", cmd_name);
         printf("  %*s                Add an overlay (with parameters)\n", (int)strlen(cmd_name), "");
         printf("  %s -D [<idx>]     Dry-run (prepare overlay, but don't apply -\n",
  	      cmd_name);
         printf("  %*s                save it as dry-run.dtbo)\n", (int)strlen(cmd_name), "");
         printf("  %s -r [<idx>]     Remove an overlay (by index, or the last)\n", cmd_name);
         printf("  %s -R [<idx>]     Remove from an overlay (by index, or all)\n",
  	      cmd_name);
         printf("  %s -l             List active overlays/dtparams\n", cmd_name);
         printf("  %s -a             List all overlays/dtparams (marking the active)\n", cmd_name);
         printf("  %s -h             Show this usage message\n", cmd_name);
         printf("  %s -h <param>...  Display help on the listed parameters\n", cmd_name);
      }
      else
      {
         printf("  %s <overlay> [<param>=<val>...]\n", cmd_name);
         printf("  %*s                Add an overlay (with parameters)\n", (int)strlen(cmd_name), "");
         printf("  %s -D [<idx>]     Dry-run (prepare overlay, but don't apply -\n",
  	      cmd_name);
         printf("  %*s                save it as dry-run.dtbo)\n", (int)strlen(cmd_name), "");
         printf("  %s -r [<overlay>] Remove an overlay (by name, index or the last)\n", cmd_name);
         printf("  %s -R [<overlay>] Remove from an overlay (by name, index or all)\n",
  	      cmd_name);
         printf("  %s -l             List active overlays/params\n", cmd_name);
         printf("  %s -a             List all overlays (marking the active)\n", cmd_name);
         printf("  %s -h             Show this usage message\n", cmd_name);
         printf("  %s -h <overlay>   Display help on an overlay\n", cmd_name);
         printf("  %s -h <overlay> <param>..  Or its parameters\n", cmd_name);
         printf("    where <overlay> is the name of an overlay or 'dtparam' for dtparams\n");
      }
      printf("Options applicable to most variants:\n");
      printf("    -d <dir>    Specify an alternate location for the overlays\n");
      printf("                (defaults to /boot/overlays or /flash/overlays)\n");
      printf("    -v          Verbose operation\n");
      printf("\n");
      printf("Adding or removing overlays and parameters requires root privileges.\n");
  
      exit(1);
  }
  ```

## 获取dts

* 获取当前运行时系统的dtb：`dtc -I fs -O dtb -o base.dtb /proc/device-tree 1>/dev/null 2>&1`；
* 获取设备树：
  * `dtc -I dtb -O dts -o basev0.dts base.dtb`：[basev0.dts](refers/basev0.dts)；
  * `fdtdump base.dtb > basev1.dts`；

## dtparam i2c_arm=on

* `wget https://github.com/raspberrypi/userland/archive/master.zip`
  * `unzip master.zip && cd userland-master`
  * `jar xvf master.zip && cd userland-master`
* `sudo apt-get install cmake`
* `./buildme`
* `sudo apt-get install ctags`
* `ctags -Rn`
* `cat ~/.vimrc`
  ```vimrc
  syntax on
  set number
  
  set expandtab
  set tabstop=4
  set tags=/home/pi/zengjf/dts/userland-master/tags
  ```
* `cd ~/zengjf/dts/userland-master/host_applications/linux/apps/dtoverlay`
* `sudo dtparam -v i2c_arm=on`
  ```
  run_cmd: which dtoverlay-pre >/dev/null 2>&1 && dtoverlay-pre
  run_cmd: dtc -I fs -O dtb -o '/tmp/.dtoverlays/base.dtb' /proc/device-tree 1>/dev/null 2>&1
  DTOVERLAY[debug]: Found override i2c_arm
  DTOVERLAY[debug]:   override i2c_arm: string target 'status'
  DTOVERLAY[debug]: delete_node(/__symbols__)
  DTOVERLAY[debug]: Wrote 162 bytes to '/tmp/.dtoverlays/1_dtparam.dtbo'
  DTOVERLAY[debug]: Wrote 174 bytes to '/sys/kernel/config/device-tree/overlays/1_dtparam/dtbo'
  run_cmd: which dtoverlay-post >/dev/null 2>&1 && dtoverlay-post
  ```
* `i2c_arm`在当前的设备树的状态：
  ```
  __overrides__ {
      [...省略]
      i2c_arm = "", "", "", "!status";
      [...省略]
  };
  ```
* 控制台打印输出调试函数：`void dtoverlay_debug(const char *fmt, ...);`
* `main()`
  * `dtoverlay_add()`
    * `DTOVERLAY[debug]: Found override i2c_arm`
      ```
      /* Returns a pointer to the override data and (through data_len) its length.
         On error, sets *data_len to be the error code. */
      const char *dtoverlay_find_override(DTBLOB_T *dtb, const char *override_name,
                                          int *data_len)
      {
         int overrides_off;
         const char *data;
         int len;
  
         // Find the table of overrides
         overrides_off = fdt_path_offset(dtb->fdt, "/__overrides__");
  
         if (overrides_off < 0)
         {
            dtoverlay_debug("/__overrides__ node not found");
            *data_len = overrides_off;
            return NULL;
         }
  
         // Locate the property
         data = fdt_getprop(dtb->fdt, overrides_off, override_name, &len);
         *data_len = len;
         if (data)
            dtoverlay_debug("Found override %s", override_name);
         else
            dtoverlay_debug("/__overrides__ has no %s property", override_name);
  
         return data;
      }
      ```

## Sense HAT DTS modify

* 参考：
  * [0023_Sense_HAT.md](0023_Sense_HAT.md)
  * [configfs-overlays.txt](https://github.com/Xilinx/linux-xlnx/blob/master/Documentation/devicetree/configfs-overlays.txt)
* [rpi-sense-overlay](https://github.com/ZengjfOS/RaspberryPi/tree/rpi-sense-overlay)
  * `make`
  * `sudo ./run.sh`

## Device Tree Blob Overlay Configuration File System

* 如果你想知道`configfs`中`overlay`是怎么工作的，可以参考: https://github.com/ikwzm/dtbocfg
* `git clone https://github.com/ikwzm/dtbocfg.git`
* `cd dtbocfg`
* `make`
  ```
  pi@raspberrypi:~/zengjf/dtbocfg $ ls
  dtbocfg.c  dtbocfg.ko  dtbocfg.mod.c  dtbocfg.mod.o  dtbocfg.o  dtbocfg.rb  LICENSE  
  Makefile  modules.order  Module.symvers  Readme.ja.md  Readme.md
  ```