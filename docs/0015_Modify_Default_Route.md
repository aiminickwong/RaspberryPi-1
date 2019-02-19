# Modify default Route

使用了usb otg转网口功能，发现原来能用的网络不能用了，找一下原因；

## Default route

```shell
root@raspberrypi:/home/pi# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         192.168.137.1   0.0.0.0         UG    202    0        0 usb0
default         192.168.23.1    0.0.0.0         UG    303    0        0 wlan0
192.168.23.0    0.0.0.0         255.255.255.0   U     303    0        0 wlan0
192.168.137.0   0.0.0.0         255.255.255.0   U     202    0        0 usb0
root@raspberrypi:/home/pi#
```

## 删除路由重新添加路由

```shell
root@raspberrypi:/home/pi# route del default gw 192.168.23.1
root@raspberrypi:/home/pi# route add default gw 192.168.23.1
root@raspberrypi:/home/pi# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         192.168.23.1    0.0.0.0         UG    0      0        0 wlan0
default         192.168.137.1   0.0.0.0         UG    202    0        0 usb0
192.168.23.0    0.0.0.0         255.255.255.0   U     303    0        0 wlan0
192.168.137.0   0.0.0.0         255.255.255.0   U     202    0        0 usb0
root@raspberrypi:/home/pi# ping www.baidu.com
PING www.baidu.com (14.215.177.39) 56(84) bytes of data.
64 bytes from 14.215.177.39 (14.215.177.39): icmp_seq=1 ttl=55 time=36.1 ms
64 bytes from 14.215.177.39 (14.215.177.39): icmp_seq=2 ttl=55 time=14.1 ms
^C
--- www.baidu.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 14.147/25.163/36.180/11.017 ms
root@raspberrypi:/home/pi#
```

## linux下设置永久路由的方法

在`/etc/rc.local`里添加。