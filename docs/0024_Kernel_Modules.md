# Kernel Modules

## 参考文档

* [How compile a loadable kernel module without recompiling kernel](https://raspberrypi.stackexchange.com/questions/39845/how-compile-a-loadable-kernel-module-without-recompiling-kernel)

## install kernel headers

* `sudo apt-get install raspberrypi-kernel-headers`
  ```
  root@raspberrypi:~# ls /lib/modules/$(uname -r)/build -al
  lrwxrwxrwx 1 root root 35 Jul  9 15:07 /lib/modules/4.19.57-v7l+/build -> /usr/src/linux-headers-4.19.57-v7l+
  ```

## build kernel module

* `hello.c`
  ```C
  #include <linux/init.h>
  #include <linux/kernel.h>
  #include <linux/module.h>
  
  MODULE_LICENSE("GPL");
  MODULE_DESCRIPTION("Do-nothing test driver");
  MODULE_VERSION("0.1");
  
  static int __init hello_init(void){
     printk(KERN_INFO "Hello, world.\n");
     return 0;
  }
  
  static void __exit hello_exit(void){
     printk(KERN_INFO "Goodbye, world.\n");
  }
  
  module_init(hello_init);
  module_exit(hello_exit);
  ```
* `Makefile`
  ```Makefile
  obj-m += hello.o
  
  all:
          make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
  
  clean:
          make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
  
  modules_install: all
          $(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install
          $(DEPMOD)
  ```
* make log
  ```sh
  pi@raspberrypi:~/zengjf/hello $ make
  make -C /lib/modules/4.19.57-v7l+/build M=/home/pi/zengjf/hello modules
  make[1]: Entering directory '/usr/src/linux-headers-4.19.57-v7l+'
    CC [M]  /home/pi/zengjf/hello/hello.o
    Building modules, stage 2.
    MODPOST 1 modules
    CC      /home/pi/zengjf/hello/hello.mod.o
    LD [M]  /home/pi/zengjf/hello/hello.ko
  make[1]: Leaving directory '/usr/src/linux-headers-4.19.57-v7l+'
  pi@raspberrypi:~/zengjf/hello $ ls
  hello.c  hello.ko  hello.mod.c  hello.mod.o  hello.o  Makefile  modules.order  Module.symvers
  ```
* [hello_module source code branch](https://github.com/ZengjfOS/RaspberryPi/tree/hello_module)
* `dmesg`查看log输出；