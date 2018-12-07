# systemd-sysv-generator

systemd已经没有了启动等级的问题，采用target的方式，那么传统的init.d里面的脚本怎么使用就成了问题，所以有了`systemd-sysv-generator`，会进行转换，那些脚本需要添加响应的描述头便于信息提取转换。

## 参考文档

* [systemd-sysv-generator — Unit generator for SysV init scripts](https://www.freedesktop.org/software/systemd/man/systemd-sysv-generator.html)
* [20.2. Init Script Actions](http://refspecs.linuxbase.org/LSB_3.1.1/LSB-Core-generic/LSB-Core-generic/iniscrptact.html)
* [How does systemd use /etc/init.d scripts?](https://unix.stackexchange.com/questions/233468/how-does-systemd-use-etc-init-d-scripts)
* [What is the default path that systemd uses to locate locate System V scripts?](https://unix.stackexchange.com/questions/394187/what-is-the-default-path-that-systemd-uses-to-locate-locate-system-v-scripts/394191#394191)
* [debian services not running](https://unix.stackexchange.com/questions/203987/debian-services-not-running/204075#204075)
* [SysVinit 引导脚本](https://zh.opensuse.org/openSUSE:Packaging_init_scripts)

## 程序

```
pi@raspberrypi:/ $ sudo find * -iname systemd-sysv-generator
lib/systemd/system-generators/systemd-sysv-generator
```

This program is listed in the `/lib/systemd/system-generators/` directory and is thus run automatically by systemd early in the bootstrap process at every boot, and again every time that systemd is instructed to re-load its configuration later on.

## 生成目录

```
pi@raspberrypi:/run/systemd $ ls
ask-password   fsck.progress  generator.late  initctl  machines  notify   quotacheck  sessions  system     users
cgroups-agent  generator      inaccessible    journal  netif     private  seats       shutdown  transient
pi@raspberrypi:/run/systemd/generator.late $ ls
dphys-swapfile.service  graphical.target.wants  multi-user.target.wants  raspi-config.service
```