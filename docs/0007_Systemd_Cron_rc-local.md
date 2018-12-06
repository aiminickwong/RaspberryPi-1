# Systemd Cron rc.local

## 参考文档

* [systemd](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)
* [Scheduling tasks with Cron](https://www.raspberrypi.org/documentation/linux/usage/cron.md)
* [rc.local](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md)

## systemd基本操作

* `/etc/systemd/system/myscript.service`
  ```
  [Unit]
  Description=My service
  After=network.target
  
  [Service]
  ExecStart=/usr/bin/python3 -u main.py
  WorkingDirectory=/home/pi/myscript
  StandardOutput=inherit
  StandardError=inherit
  Restart=always
  User=pi
  
  [Install]
  WantedBy=multi-user.target
  ```
* `sudo systemctl start myscript.service`
* `sudo systemctl stop myscript.service`