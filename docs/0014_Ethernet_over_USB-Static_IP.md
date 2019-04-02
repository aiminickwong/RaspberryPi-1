# Ethernet over USB - Static IP

貌似不设定静态IP，这个USB OTG的IP总是会变化，有时候还会跨网段变化，所以还是设定死了比较好。

## 参考文档

* [Raspberry Pi Zero - Ethernet over USB - Static IP](https://www.raspberrypi.org/forums/viewtopic.php?t=188528)

## 操作方法

`/etc/dhcpcd.conf`：
```
[...省略]
interface usb0
static ip_address=192.168.137.2/24
static routers=192.168.137.1
static domain_name_servers=8.8.8.8
```

上面的routers字段，如果不想使用这个路由，没必要设定；