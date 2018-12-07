# Systemd Advance

## 参考文档

* [树莓派启动的相关问题](http://elmagnifico.me/2015/11/12/RaspberryStartup-6/)
* [走进Linux之systemd启动过程](https://www.cnblogs.com/swordxia/p/4521428.html)
* [systemd 中文手册](http://www.jinbuguo.com/systemd/systemd.html)
* [Systemd 入门教程：命令篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html)
* [Systemd 入门教程：实战篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)
* [Systemd FAQ (简体中文)](https://wiki.archlinux.org/index.php/Systemd_FAQ_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))

## init真相

```
pi@raspberrypi:/etc/rcS.d $ stat /sbin/init
  File: /sbin/init -> /lib/systemd/systemd
  Size: 20              Blocks: 0          IO Block: 4096   symbolic link
Device: b302h/45826d    Inode: 6755        Links: 1
Access: (0777/lrwxrwxrwx)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2018-11-13 14:08:59.595343944 +0000
Modify: 2018-10-28 17:02:10.000000000 +0000
Change: 2018-11-13 14:08:59.595343944 +0000
 Birth: -
```

## Systemd 配置

当作为系统实例运行时， systemd 将会按照 system.conf 配置文件 以及 system.conf.d 配置目录中的指令工作； 当作为用户实例运行时，systemd 将会按照 user.conf 配置文件 以及 user.conf.d 配置目录中的指令工作。

## sysvinit启动级别和systemd target的对应表

看懂这部分可以很好得理解为什么无图形界面是从`multi-user.target`启动，有图形界面从`graphical.target`启动。

sysvinit | systemd target | 备注
:---:|:---:|:---:
0           | poweroff.target   | 关闭系统
1,s,single  | rescue.target     | 单用户模式
2,4         | multi-user.target | 用户定义/域特定运行级别。默认等同于 3
3           | multi-user.target | 多用户，非图形化界面
5           | graphical.target  | 多用户，图形化界面
6           | reboot.target     | 重启
emergency   | emergency.target  | 紧急shell

```
pi@raspberrypi:/lib/systemd/system $ ls -al runlevel*
lrwxrwxrwx 1 root root   15 Oct 28 17:02 runlevel0.target -> poweroff.target
lrwxrwxrwx 1 root root   13 Oct 28 17:02 runlevel1.target -> rescue.target
lrwxrwxrwx 1 root root   17 Oct 28 17:02 runlevel2.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Oct 28 17:02 runlevel3.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Oct 28 17:02 runlevel4.target -> multi-user.target
lrwxrwxrwx 1 root root   16 Oct 28 17:02 runlevel5.target -> graphical.target
lrwxrwxrwx 1 root root   13 Oct 28 17:02 runlevel6.target -> reboot.target
```

## 基本概念

* service：用于封装一个后台服务进程；
* target：用于将多个单元在逻辑上组合在一起；
* 命令行处理命令：`systemctl`
* `systemctl enable xxx.service`：为对应得service在target目录(/etc/systemd/system/<target dir>)创建软链接；
* `systemctl disable xxx.service`：删除软链接；

## Systemd 工作目录

* 存放系统target目录: `/lib/systemd/system`
  ```
  pi@raspberrypi:/ $ pkg-config systemd --variable=systemdsystemunitdir
  /lib/systemd/system
  pi@raspberrypi:/ $ ls /lib/systemd/system
  alsa-restore.service                    getty.target.wants                 paths.target                       runlevel4.target                       systemd-journal-flush.service
  alsa-state.service                      gldriver-test.service              paxctld.service                    runlevel4.target.wants                 systemd-kexec.service
  alsa-utils.service                      graphical.target                   pigpiod.service                    runlevel5.target                       systemd-localed.service
  apply_noobs_os_config.service           graphical.target.wants             plymouth-halt.service              runlevel5.target.wants                 systemd-logind.service
  apt-daily.service                       halt.service                       plymouth-kexec.service             runlevel6.target                       systemd-machine-id-commit.service
  apt-daily.timer                         halt.target                        plymouth-log.service               run-rpc_pipefs.mount                   systemd-modules-load.service
  apt-daily-upgrade.service               halt.target.wants                  plymouth-poweroff.service          sendsigs.service                       systemd-networkd.service
  apt-daily-upgrade.timer                 hciuart.service                    plymouth-quit.service              serial-getty@.service                  systemd-networkd.socket
  auth-rpcgss-module.service              hibernate.target                   plymouth-quit-wait.service         shutdown.target                        systemd-networkd-wait-online.service
  autovt@.service                         hostname.service                   plymouth-read-write.service        sigpwr.target                          systemd-poweroff.service
  avahi-daemon.service                    hwclock.service                    plymouth-reboot.service            single.service                         systemd-quotacheck.service
  avahi-daemon.socket                     hybrid-sleep.target                plymouth.service                   sleep.target                           systemd-random-seed.service
  basic.target                            ifup@.service                      plymouth-start.service             slices.target                          systemd-reboot.service
  basic.target.wants                      initrd-cleanup.service             plymouth-switch-root.service       smartcard.target                       systemd-remount-fs.service
  bluealsa.service                        initrd-fs.target                   polkit.service                     sockets.target                         systemd-resolved.service
  bluetooth.service                       initrd-parse-etc.service           portmap.service                    sockets.target.wants                   systemd-resolved.service.d
  bluetooth.target                        initrd-root-device.target          poweroff.target                    sound.target                           systemd-rfkill.service
  bootlogd.service                        initrd-root-fs.target              poweroff.target.wants              ssh.service                            systemd-rfkill.socket
  bootlogs.service                        initrd-switch-root.service         printer.target                     ssh@.service                           systemd-suspend.service
  bootmisc.service                        initrd-switch-root.target          proc-fs-nfsd.mount                 ssh.socket                             systemd-sysctl.service
  bthelper@.service                       initrd-switch-root.target.wants    procps.service                     sshswitch.service                      systemd-timedated.service
  busnames.target                         initrd.target                      proc-sys-fs-binfmt_misc.automount  stop-bootlogd.service                  systemd-timesyncd.service
  busnames.target.wants                   initrd-udevadm-cleanup-db.service  proc-sys-fs-binfmt_misc.mount      stop-bootlogd-single.service           systemd-timesyncd.service.d
  checkfs.service                         kexec.target                       quotaon.service                    sudo.service                           systemd-tmpfiles-clean.service
  checkroot-bootclean.service             kexec.target.wants                 raspberrypi-net-mods.service       suspend.target                         systemd-tmpfiles-clean.timer
  checkroot.service                       keyboard-setup.service             rc-local.service                   swap.target                            systemd-tmpfiles-setup-dev.service
  console-getty.service                   killprocs.service                  rc.local.service                   sys-fs-fuse-connections.mount          systemd-tmpfiles-setup.service
  console-setup.service                   kmod.service                       rc-local.service.d                 sysinit.target                         systemd-udevd-control.socket
  container-getty@.service                kmod-static-nodes.service          rc.service                         sysinit.target.wants                   systemd-udevd-kernel.socket
  cron.service                            lightdm.service                    rcS.service                        sys-kernel-config.mount                systemd-udevd.service
  cryptdisks-early.service                local-fs-pre.target                reboot.service                     sys-kernel-debug.mount                 systemd-udev-settle.service
  cryptdisks.service                      local-fs.target                    reboot.target                      syslog.socket                          systemd-udev-trigger.service
  cryptsetup-pre.target                   local-fs.target.wants              reboot.target.wants                systemd-ask-password-console.path      systemd-update-utmp-runlevel.service
  cryptsetup.target                       machine.slice                      regenerate_ssh_host_keys.service   systemd-ask-password-console.service   systemd-update-utmp.service
  ctrl-alt-del.target                     module-init-tools.service          remote-fs-pre.target               systemd-ask-password-plymouth.path     systemd-user-sessions.service
  dbus-org.freedesktop.hostname1.service  motd.service                       remote-fs.target                   systemd-ask-password-plymouth.service  system.slice
  dbus-org.freedesktop.locale1.service    mountall-bootclean.service         rescue.service                     systemd-ask-password-wall.path         system-update.target
  dbus-org.freedesktop.login1.service     mountall.service                   rescue.target                      systemd-ask-password-wall.service      system-update.target.wants
  dbus-org.freedesktop.network1.service   mountdevsubfs.service              rescue.target.wants                systemd-backlight@.service             timers.target
  dbus-org.freedesktop.resolve1.service   mountkernfs.service                rmnologin.service                  systemd-binfmt.service                 timers.target.wants
  dbus-org.freedesktop.timedate1.service  mountnfs-bootclean.service         rpcbind.service                    systemd-exit.service                   time-sync.target
  dbus.service                            mountnfs.service                   rpcbind.socket                     systemd-fsckd.service                  triggerhappy.service
  dbus.socket                             multi-user.target                  rpcbind.target                     systemd-fsckd.socket                   triggerhappy.socket
  debug-shell.service                     multi-user.target.wants            rpc-gssd.service                   systemd-fsck-root.service              udev.service
  default.target                          networking.service                 rpc-statd-notify.service           systemd-fsck@.service                  udisks2.service
  dev-hugepages.mount                     network-online.target              rpc-statd.service                  systemd-halt.service                   umountfs.service
  dev-mqueue.mount                        network-pre.target                 rpc-svcgssd.service                systemd-hibernate-resume@.service      umountnfs.service
  dhcpcd.service                          network.target                     rpi-display-backlight.service      systemd-hibernate.service              umountroot.service
  emergency.service                       nfs-client.target                  rsync.service                      systemd-hostnamed.service              umount.target
  emergency.target                        nfs-common.service                 rsyslog.service                    systemd-hwdb-update.service            urandom.service
  exit.target                             nfs-config.service                 runlevel0.target                   systemd-hybrid-sleep.service           usb_modeswitch@.service
  fake-hwclock.service                    nfs-idmapd.service                 runlevel1.target                   systemd-initctl.service                user@.service
  final.target                            nfs-utils.service                  runlevel1.target.wants             systemd-initctl.socket                 user.slice
  fuse.service                            nss-lookup.target                  runlevel2.target                   systemd-journald-audit.socket          wifi-country.service
  getty@.service                          nss-user-lookup.target             runlevel2.target.wants             systemd-journald-dev-log.socket        wpa_supplicant.service
  getty-static.service                    packagekit-offline-update.service  runlevel3.target                   systemd-journald.service               wpa_supplicant@.service
  getty.target                            packagekit.service                 runlevel3.target.wants             systemd-journald.socket                x11-common.service
  ```
* 存放用户target目录: `/usr/lib/systemd/user`
  ```
  pi@raspberrypi:/ $ pkg-config systemd --variable=systemduserunitdir
  /usr/lib/systemd/user
  pi@raspberrypi:/ $ ls /usr/lib/systemd/user
  basic.target      exit.target               gpg-agent-ssh.socket                gvfs-goa-volume-monitor.service      printer.target        ssh-agent.service
  bluetooth.target  glib-pacrunner.service    graphical-session-pre.target        gvfs-gphoto2-volume-monitor.service  shutdown.target       systemd-exit.service
  busnames.target   gpg-agent-browser.socket  graphical-session-pre.target.wants  gvfs-metadata.service                smartcard.target      timers.target
  dbus.service      gpg-agent-extra.socket    graphical-session.target            gvfs-mtp-volume-monitor.service      sockets.target
  dbus.socket       gpg-agent.service         gvfs-afc-volume-monitor.service     gvfs-udisks2-volume-monitor.service  sockets.target.wants
  default.target    gpg-agent.socket          gvfs-daemon.service                 paths.target                         sound.target
  pi@raspberrypi:/ $
  ```

## Systemd Squence

在系统启动时，systemd 默认启动 default.target 单元， 该单元中应该包含所有你想在开机时默认启动的单元。 但实际上，它通常只是一个指向 graphical.target (图形界面) 或 multi-user.target (命令行界面，常用于嵌入式或服务器环境， 一般是 graphical.target 的一个子集)的符号连接。

目前跟得是非图形界面得树莓派系统版本；

* `/etc/systemd/system/default.target`
  ```
  pi@raspberrypi:/etc/systemd/system $ systemctl get-default    # 获取默认target名称
  multi-user.target
  pi@raspberrypi:/etc/systemd/system $ ls -al default.target
  lrwxrwxrwx 1 root root 37 Dec  6 00:22 default.target -> /lib/systemd/system/multi-user.target
  ```
* `/lib/systemd/system/multi-user.target`
  ```
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  [Unit]
  Description=Multi-User System
  Documentation=man:systemd.special(7)
  # Requires字段则表示"强依赖"关系，即如果该服务启动失败或异常退出，那么sshd.service也必须退出。
  # Wants字段：表示sshd.service与sshd-keygen.service之间存在"弱依赖"关系，即如果"sshd-keygen.service"启动失败或停止运行，不影响sshd.service继续执行。
  # required 是强依赖；want 则是弱依赖
  Requires=basic.target
  # Conflicts字段：冲突字段。如果rescue.service或rescue.target正在运行，multi-user.target就不能运行，反之亦然。这里指定的 Unit 不能与当前 Unit 同时运行
  Conflicts=rescue.service rescue.target
  # 当前target需要在这些target之后启动，也就是会转到先去处理那些target，出了After，还有Before是同样得意思
  After=basic.target rescue.service rescue.target
  # AllowIsolate：允许使用systemctl isolate命令切换到default.target
  AllowIsolate=yes
  ```
* `/lib/systemd/system/basic.target`
  ```
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  [Unit]
  Description=Basic System
  Documentation=man:systemd.special(7)
  Requires=sysinit.target
  Wants=sockets.target timers.target paths.target slices.target
  After=sysinit.target sockets.target paths.target slices.target tmp.mount
  
  # We support /var, /tmp, /var/tmp, being on NFS, but we don't pull in
  # remote-fs.target by default, hence pull them in explicitly here. Note that we
  # require /var and /var/tmp, but only add a Wants= type dependency on /tmp, as
  # we support that unit being masked, and this should not be considered an error.
  RequiresMountsFor=/var /var/tmp
  Wants=tmp.mount
  ```
* `/lib/systemd/system/sysinit.target`
  ```
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  [Unit]
  Description=System Initialization
  Documentation=man:systemd.special(7)
  Conflicts=emergency.service emergency.target
  Wants=local-fs.target swap.target
  After=local-fs.target swap.target emergency.service emergency.target
  ```
* `lib/systemd/system/local-fs.target`
  ```
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  [Unit]
  Description=Local File Systems
  Documentation=man:systemd.special(7)
  DefaultDependencies=no
  Conflicts=shutdown.target
  After=local-fs-pre.target
  OnFailure=emergency.target
  OnFailureJobMode=replace-irreversibly
  ```
* `lib/systemd/system/local-fs-pre.target`
  ```
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  [Unit]
  Description=Local File Systems (Pre)
  Documentation=man:systemd.special(7)
  RefuseManualStart=yes
  ```

## sshd.service分析

* ssh service
  ```
  pi@raspberrypi:/etc/systemd/system $ ls -al sshd.service multi-user.target.wants/ssh.service
  lrwxrwxrwx 1 root root 31 Dec  5 08:27 multi-user.target.wants/ssh.service -> /lib/systemd/system/ssh.service
  lrwxrwxrwx 1 root root 31 Dec  5 10:55 sshd.service -> /lib/systemd/system/ssh.service
  ```
* `/lib/systemd/system/ssh.service`
  ```
  [Unit]
  Description=OpenBSD Secure Shell server
  After=network.target auditd.service
  ConditionPathExists=!/etc/ssh/sshd_not_to_be_run
  
  [Service]
  # EnvironmentFile字段：指定当前服务的环境参数文件。该文件内部的key=value键值对，可以用$key的形式，在当前配置文件中获取。
  # 所有的启动设置之前，都可以加上一个连词号（-），表示"抑制错误"，即发生错误的时候，不影响其他命令的执行。
  EnvironmentFile=-/etc/default/ssh
  # ExecStartPre字段：启动服务之前执行的命令
  ExecStartPre=/usr/sbin/sshd -t
  # ExecStart字段：定义启动进程时执行的命令。
  ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
  # ExecReload字段：重启服务时执行的命令
  ExecReload=/usr/sbin/sshd -t
  ExecReload=/bin/kill -HUP $MAINPID
  # KillMode字段：定义 Systemd 如何停止 sshd 服务。将KillMode设为process，表示只停止主进程，不停止任何sshd 子进程，即子进程打开的 SSH session 仍然保持连接。
  KillMode=process
  # Restart字段：定义了 sshd 退出后，Systemd 的重启方式。Restart设为on-failure，表示任何意外的失败，就将重启sshd。如果 sshd 正常停止（比如执行systemctl stop命令），它就不会重启。
  Restart=on-failure
  RestartPreventExitStatus=255
  Type=notify
  
  [Install]
  # WantedBy字段：表示该服务所在的 Target。
  WantedBy=multi-user.target
  Alias=sshd.service
  ```

## 内核引导项

* 参考文档：[内核引导选项](http://www.jinbuguo.com/systemd/systemd.html#%E5%86%85%E6%A0%B8%E5%BC%95%E5%AF%BC%E9%80%89%E9%A1%B9)
* systemd.unit=, rd.systemd.unit=：设置默认启动的单元。 默认值是 default.target 。 可用于临时修改启动目标(例如 rescue.target 或 emergency.target )。这就相当于是PC进入安全模式得功能；

## rc.local

* 查找线索
  ```Shell
  pi@raspberrypi:/ $ grep rc.local /etc/* -r                              # 检查谁调用rc.local线索
  grep: /etc/dhcpcd.secret: Permission denied
  grep: /etc/gshadow: Permission denied
  grep: /etc/polkit-1/localauthority: Permission denied
  /etc/rc.local:# rc.local
  grep: /etc/security/opasswd: Permission denied
  grep: /etc/shadow: Permission denied
  grep: /etc/ssh/ssh_host_ed25519_key: Permission denied
  grep: /etc/ssh/ssh_host_dsa_key: Permission denied
  grep: /etc/ssh/ssh_host_ecdsa_key: Permission denied
  grep: /etc/ssh/ssh_host_rsa_key: Permission denied
  grep: /etc/ssl/private: Permission denied
  grep: /etc/sudoers: Permission denied
  grep: /etc/sudoers.d/010_pi-nopasswd: Permission denied
  grep: /etc/sudoers.d/README: Permission denied
  /etc/systemd/system/autologin@.service:After=rc-local.service
  /etc/vim/vimrc:if filereadable("/etc/vim/vimrc.local")
  /etc/vim/vimrc:  source /etc/vim/vimrc.local
  pi@raspberrypi:/ $ sudo find / -iname rc-local.service                  # 查找一下服务
  /run/systemd/generator/multi-user.target.wants/rc-local.service
  /lib/systemd/system/rc-local.service
  /sys/fs/cgroup/devices/system.slice/rc-local.service
  /sys/fs/cgroup/systemd/system.slice/rc-local.service
  pi@raspberrypi:/ $ ls -al /lib/systemd/system/rc-local.service
  -rw-r--r-- 1 root root 628 Oct 28 17:02 /lib/systemd/system/rc-local.service
  ```
* `/lib/systemd/system/rc-local.service`
  ```Shell
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  # This unit gets pulled automatically into multi-user.target by
  # systemd-rc-local-generator if /etc/rc.local is executable.
  [Unit]
  Description=/etc/rc.local Compatibility
  ConditionFileIsExecutable=/etc/rc.local
  After=network.target
  
  [Service]
  Type=forking
  ExecStart=/etc/rc.local start                                           # 就是这里了
  TimeoutSec=0
  RemainAfterExit=yes
  GuessMainPID=no
  ```
* `/etc/systemd/system/autologin@.service`
  ```Shell
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  [Unit]
  Description=Getty on %I
  Documentation=man:agetty(8) man:systemd-getty-generator(8)
  Documentation=http://0pointer.de/blog/projects/serial-console.html
  After=systemd-user-sessions.service plymouth-quit-wait.service
  After=rc-local.service
  
  # If additional gettys are spawned during boot then we should make
  # sure that this is synchronized before getty.target, even though
  # getty.target didn't actually pull it in.
  Before=getty.target
  IgnoreOnIsolate=yes
  
  # On systems without virtual consoles, don't start any getty. Note
  # that serial gettys are covered by serial-getty@.service, not this
  # unit.
  ConditionPathExists=/dev/tty0
  
  [Service]
  # the VT is cleared by TTYVTDisallocate
  ExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM                 # 启动服务
  Type=idle
  Restart=always
  RestartSec=0
  UtmpIdentifier=%I
  TTYPath=/dev/%I
  TTYReset=yes
  TTYVHangup=yes
  TTYVTDisallocate=yes
  KillMode=process
  IgnoreSIGPIPE=no
  SendSIGHUP=yes
  
  # Unset locale for the console getty since the console has problems
  # displaying some internationalized messages.
  Environment=LANG= LANGUAGE= LC_CTYPE= LC_NUMERIC= LC_TIME= LC_COLLATE= LC_MONETARY= LC_MESSAGES= LC_PAPER= LC_NAME= LC_ADDRESS= LC_TELEPHONE= LC_MEASUREMENT= LC_IDENTIFICATION=
  
  [Install]
  WantedBy=getty.target
  DefaultInstance=tty1
  ```
* `ps aux`得出来得结果不是`/etc/systemd/system/autologin@.service`运行的，参数不对
  ```
  [...省略]
  root       322  0.0  0.4   4180  1808 tty1     Ss+  05:07   0:00 /sbin/agetty --noclear tty1 linux
  [...省略]
  ```
* `/lib/systemd/system/getty@.service`
  ```
  pi@raspberrypi:/etc/systemd/system/getty.target.wants $ ls -al
  total 8
  drwxr-xr-x  2 root root 4096 Dec  6 00:22 .
  drwxr-xr-x 15 root root 4096 Dec  6 00:22 ..
  lrwxrwxrwx  1 root root   34 Dec  6 00:22 getty@tty1.service -> /lib/systemd/system/getty@.service
  ```
* `/lib/systemd/system/getty@.service`
  ```
  #  This file is part of systemd.
  #
  #  systemd is free software; you can redistribute it and/or modify it
  #  under the terms of the GNU Lesser General Public License as published by
  #  the Free Software Foundation; either version 2.1 of the License, or
  #  (at your option) any later version.
  
  [Unit]
  Description=Getty on %I
  Documentation=man:agetty(8) man:systemd-getty-generator(8)
  Documentation=http://0pointer.de/blog/projects/serial-console.html
  After=systemd-user-sessions.service plymouth-quit-wait.service
  After=rc-local.service
  
  # If additional gettys are spawned during boot then we should make
  # sure that this is synchronized before getty.target, even though
  # getty.target didn't actually pull it in.
  Before=getty.target
  IgnoreOnIsolate=yes
  
  # IgnoreOnIsolate causes issues with sulogin, if someone isolates
  # rescue.target or starts rescue.service from multi-user.target or
  # graphical.target.
  Conflicts=rescue.service
  Before=rescue.service
  
  # On systems without virtual consoles, don't start any getty. Note
  # that serial gettys are covered by serial-getty@.service, not this
  # unit.
  ConditionPathExists=/dev/tty0
  
  [Service]
  # the VT is cleared by TTYVTDisallocate
  ExecStart=-/sbin/agetty --noclear %I $TERM
  Type=idle
  Restart=always
  RestartSec=0
  UtmpIdentifier=%I
  TTYPath=/dev/%I
  TTYReset=yes
  TTYVHangup=yes
  TTYVTDisallocate=yes
  KillMode=process
  IgnoreSIGPIPE=no
  SendSIGHUP=yes
  
  # Unset locale for the console getty since the console has problems
  # displaying some internationalized messages.
  Environment=LANG= LANGUAGE= LC_CTYPE= LC_NUMERIC= LC_TIME= LC_COLLATE= LC_MONETARY= LC_MESSAGES= LC_PAPER= LC_NAME= LC_ADDRESS= LC_TELEPHONE= LC_MEASUREMENT= LC_IDENTIFICATION=
  
  [Install]
  WantedBy=getty.target
  DefaultInstance=tty1
  ```
* 由上可知`getty@tty1.service`经过调用`getty@.service`，在`getty@.service`的%I = tty1；

## multi-user.target 究竟启用了哪些服务

```
pi@raspberrypi:~ $ systemctl show -p "Wants" multi-user.target > data
pi@raspberrypi:~ $ cat data
Wants=remote-fs.target cron.service systemd-ask-password-wall.path systemd-user-sessions.service systemd-logind.service rsync.service rc-local.service sshswitch.service dhcpcd.service gldriver-test.service triggerhappy.service avahi-daemon.service ssh.service raspberrypi-net-mods.service plymouth-quit.service nfs-client.target console-setup.service wifi-country.service dphys-swapfile.service systemd-update-utmp-runlevel.service plymouth-quit-wait.service dbus.service networking.service raspi-config.service hciuart.service rsyslog.service getty.target
pi@raspberrypi:~ $

```