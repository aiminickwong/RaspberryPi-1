# Modify default Route


## 参考文档

* [RPi 3B 无线连接配置](https://www.cnblogs.com/zengjfgit/p/8854449.html)
* [How to setup multiple WiFi networks?](https://raspberrypi.stackexchange.com/questions/11631/how-to-setup-multiple-wifi-networks)

## 操作方法

* `/etc/wpa_supplicant/wpa_supplicant.conf`
  ```
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  update_config=1
  country=GB
  
  network={
          ssid="your ssid"
          psk="your password"
          key_mgmt=WPA-PSK
  }
  
  network={
          ssid="your ssid"
          psk="your password"
          key_mgmt=WPA-PSK
  }
  ```