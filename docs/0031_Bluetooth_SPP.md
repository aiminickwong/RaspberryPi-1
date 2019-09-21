# Bluetooth SPP

## 参考文档

* [GUIDE: How to establish Bluetooth serial communication between two Pi 3's](https://www.reddit.com/r/raspberry_pi/comments/6nchaj/guide_how_to_establish_bluetooth_serial/)
* [树莓派 3B+ 原生蓝牙与手机通讯（BlueTooth SPP）方法和步骤](https://zhuanlan.zhihu.com/p/26309165)
* [raspberry-bluetooth-demo](https://github.com/EnableTech/raspberry-bluetooth-demo)

## steps

* `sudo apt-get install bluez pi-bluetooth python-bluez`
* `cat /etc/systemd/system/dbus-org.bluez.service`
  ```
  [Unit]
  Description=Bluetooth service
  Documentation=man:bluetoothd(8)
  ConditionPathIsDirectory=/sys/class/bluetooth
  
  [Service]
  Type=dbus
  BusName=org.bluez
  ExecStart=/usr/lib/bluetooth/bluetoothd -C
  ExecStartPost=/usr/bin/sdptool add SP
  NotifyAccess=main
  #WatchdogSec=10
  #Restart=on-failure
  CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
  LimitNPROC=1
  ProtectHome=true
  ProtectSystem=full
  
  [Install]
  WantedBy=bluetooth.target
  Alias=dbus-org.bluez.service
  ```
* `sudo reboot`
* `hciconfig`
  ```
  hci0:	Type: Primary  Bus: UART
  	BD Address: DC:A6:32:17:47:93  ACL MTU: 1021:8  SCO MTU: 64:1
  	UP RUNNING PSCAN ISCAN 
  	RX bytes:1978 acl:31 sco:0 events:96 errors:0
  	TX bytes:6491 acl:18 sco:0 commands:76 errors:0
  
  ```

## run python service test

* `ls /usr/share/doc/python-bluez/examples/simple/`
  ```
  asynchronous-inquiry.py  l2capclient.py  rfcomm-client.py  sdp-browse.py
  inquiry.py		 l2capserver.py  rfcomm-server.py
  ```
* `python3 /usr/share/doc/python-bluez/examples/simple/rfcomm-server.py`
  ```
  root@raspberrypi: ~# python3 rfcomm-server.py 
  Waiting for connection on RFCOMM channel 1
  Accepted connection from  ('C4:9F:4C:B2:FA:98', 1)
  received [b'wwws']
  received [b'ssss']
  received [b'sddd']
  received [b'ffgg']
  [...省略]
  ```

## systemd

* `/lib/systemd/system/rfcomm.service`
  ```
  [Unit]
  Description=RFCOMM service
  After=bluetooth.service
  Requires=bluetooth.service
  
  [Service]
  ExecStart=/usr/bin/rfcomm watch hci0
  
  [Install]
  WantedBy=multi-user.target
  ```
* `sudo systemctl enable rfcomm` or `sudo systemctl disable rfcomm`
* `minicom -s`
  ```
      +-----------------------------------------------------------------------+
      | A -    Serial Device      : /dev/rfcomm0                              |
      | B - Lockfile Location     : /var/lock                                 |
      | C -   Callin Program      :                                           |
      | D -  Callout Program      :                                           |
      | E -    Bps/Par/Bits       : 115200 8N1                                |
      | F - Hardware Flow Control : No                                        |
      | G - Software Flow Control : No                                        |
      |                                                                       |
      |    Change which setting?                                              |
      +-----------------------------------------------------------------------+
              | Screen and keyboard      |
              | Save setup as dfl        |
              | Save setup as..          |
              | Exit                     |
              | Exit from Minicom        |
              +--------------------------+
  ```
* 测试通信
  ```
  Welcome to minicom 2.7.1
  
  OPTIONS: I18n
  Compiled on Aug 13 2017, 15:25:34.
  Port /dev/rfcomm0, 07:39:14
  
  Press CTRL-A Z for help on special keys
  
  eyiidgkdykry
  
  ```

## python server demo 

```python
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import bluetooth
import threading
#服务器套接字(用来接收新链接)
server_socket=None

#连接套接字服务子线程
def serveSocket(sock,info):
    #开个死循环等待客户端发送信息
    while True:
        #接收1024个字节,然后以UTF-8解码(中文),如果没有可以接收的信息则自动阻塞线程(API)
        receive=sock.recv(1024).decode('utf-8');
        #打印刚刚读到的东西(info=地址)
        print('['+str(info)+']'+receive);
        #为了返回好看点,加个换行
        receive=receive+"\n";
        #回传数据给发送者
        sock.send(receive.encode('utf-8'));

#主线程

#创建一个服务器套接字,用来监听端口
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM);
#允许任何地址的主机连接,未知参数:1(端口号,通道号)
server_socket.bind(("",1))
#监听端口/通道
server_socket.listen(1);

#开死循环 等待客户端连接
#本处应放在另外的子线程中
while True:
    #等待有人来连接,如果没人来,就阻塞线程等待(这本来要搞个会话池,以方便给不同的设备发送数据)
    sock,info=server_socket.accept();
    #打印有人来了的消息
    print(str(info[0])+' Connected!');
    #创建一个线程专门服务新来的连接(这本来应该搞个线程池来管理线程的)
    t=threading.Thread(target=serveSocket,args=(sock,info[0]))
    #设置线程守护,防止程序在线程结束前结束
    t.setDaemon(True)
    #启动线程
    t.start();
```