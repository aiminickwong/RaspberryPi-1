# Boot Dir Support SSH Auto Run

## raspberrypi-net-mods.service

* `ls -al /etc/systemd/system/multi-user.target.wants/raspberrypi-net-mods.service`
  ```
  lrwxrwxrwx 1 root root 48 Jul 10 01:10 /etc/systemd/system/multi-user.target.wants/raspberrypi-net-mods.service -> /lib/systemd/system/raspberrypi-net-mods.service
  ```
* `/lib/systemd/system/raspberrypi-net-mods.service`
  ```
  [Unit]
  Description=Copy user wpa_supplicant.conf
  ConditionPathExists=/boot/wpa_supplicant.conf
  Before=dhcpcd.service
  After=systemd-rfkill.service
  
  [Service]
  Type=oneshot
  RemainAfterExit=yes
  ExecStart=/bin/mv /boot/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
  ExecStartPost=/bin/chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
  ExecStartPost=/usr/sbin/rfkill unblock wifi
  
  [Install]
  WantedBy=multi-user.target
  ```

## sshwitch.service

* `ls -al /etc/systemd/system/multi-user.target.wants/sshswitch.service`
  ```
  lrwxrwxrwx 1 root root 37 Jul 10 01:08 /etc/systemd/system/multi-user.target.wants/sshswitch.service -> /lib/systemd/system/sshswitch.service
  ```
* `/lib/systemd/system/sshswitch.service`
  ```
  [Unit]
  Description=Turn on SSH if /boot/ssh is present
  ConditionPathExistsGlob=/boot/ssh{,.txt}
  After=regenerate_ssh_host_keys.service
  
  [Service]
  Type=oneshot
  ExecStart=/bin/sh -c "update-rc.d ssh enable && invoke-rc.d ssh start && rm -f /boot/ssh ; rm -f /boot/ssh.txt"
  
  [Install]
  WantedBy=multi-user.target
  ```
* `whereis update-rc.d`
  ```
  update-rc: /usr/sbin/update-rc.d
  ```