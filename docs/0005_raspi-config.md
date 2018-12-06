# raspi-config

## 参考文档

* [raspi-config](https://github.com/raspberrypi/documentation/blob/master/configuration/raspi-config.md)
* [raspi-config Source Code](https://github.com/RPi-Distro/raspi-config)
* [树莓派 -- i2c学习](https://blog.csdn.net/feiwatson/article/details/81048616)

## UART Config Code Hacking

```Shell
#!/bin/sh
# Part of raspi-config https://github.com/RPi-Distro/raspi-config
#
# See LICENSE file for copyright and license details

INTERACTIVE=True
ASK_TO_REBOOT=0
BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf
CONFIG=/boot/config.txt

is_pi () {
  ARCH=$(dpkg --print-architecture)
  if [ "$ARCH" = "armhf" ] ; then
    return 0
  else
    return 1
  fi
}

if is_pi ; then
  CMDLINE=/boot/cmdline.txt
else
  CMDLINE=/proc/cmdline
fi

[...省略]

set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"                 # lua脚本输出到$3.bak文件
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do                             # 轮询每一行
  if line:match("^#?%s*"..key.."=.*$") then             # 链接两个字符串
    line=key.."="..value                                # 匹配到了重新合成
    made_change=true
  end
  print(line)                                           # 生成当前行
end
if not made_change then                                 # 如果之前的key不存在，那么就加在文件末尾
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"                                        # 文件替换
}

[...省略]

get_serial() {                                          # 获取命令参数console值
  if grep -q -E "console=(serial0|ttyAMA0|ttyS0)" $CMDLINE ; then
    echo 0
  else
    echo 1
  fi
}

get_serial_hw() {                                       # 获取BIOS对uart的配置
  if grep -q -E "^enable_uart=1" $CONFIG ; then
    echo 0
  elif grep -q -E "^enable_uart=0" $CONFIG ; then
    echo 1
  elif [ -e /dev/serial0 ] ; then
    echo 0
  else
    echo 1
  fi
}

do_serial() {
  DEFAULTS=--defaultno
  DEFAULTH=--defaultno
  CURRENTS=0
  CURRENTH=0
  if [ $(get_serial) -eq 0 ]; then              # 获取文件系统串口名称，0表示找到了
      DEFAULTS=
      CURRENTS=1
  fi
  if [ $(get_serial_hw) -eq 0 ]; then           # 获取BIOS配置，0表示找到了
      DEFAULTH=
      CURRENTH=1
  fi
  if [ "$INTERACTIVE" = True ]; then            # 通过登陆，这里相当于将内核信息打印到这个串口上去
    # Exit status is 0 if whiptail is exited by pressing the Yes or OK button, and 1 if the No or Cancel button is pressed. 
    whiptail --yesno "Would you like a login shell to be accessible over serial?" $DEFAULTS 20 60 2
    RET=$?
  else
    RET=$1
  fi
  if [ $RET -eq $CURRENTS ]; then               # 如果选择了YES，需要重启
    ASK_TO_REBOOT=1
  fi
  if [ $RET -eq 0 ]; then                       # login shell，修改内核命令行参数
    if grep -q "console=ttyAMA0" $CMDLINE ; then
      if [ -e /proc/device-tree/aliases/serial0 ]; then
        sed -i $CMDLINE -e "s/console=ttyAMA0/console=serial0/"
      fi
    elif ! grep -q "console=ttyAMA0" $CMDLINE && ! grep -q "console=serial0" $CMDLINE ; then
      if [ -e /proc/device-tree/aliases/serial0 ]; then
        sed -i $CMDLINE -e "s/root=/console=serial0,115200 root=/"
      else
        sed -i $CMDLINE -e "s/root=/console=ttyAMA0,115200 root=/"
      fi
    fi
    set_config_var enable_uart 1 $CONFIG        # enable_uart置1，并写入配置
    SSTATUS=enabled
    HSTATUS=enabled
  elif [ $RET -eq 1 ] || [ $RET -eq 2 ]; then   # 作为普通串口使用
    sed -i $CMDLINE -e "s/console=ttyAMA0,[0-9]\+ //"       # 移除
    sed -i $CMDLINE -e "s/console=serial0,[0-9]\+ //"       # 移除
    SSTATUS=disabled
    if [ "$INTERACTIVE" = True ]; then
      whiptail --yesno "Would you like the serial port hardware to be enabled?" $DEFAULTH 20 60 2
      RET=$?
    else
      RET=$((2-$RET))
    fi
    if [ $RET -eq $CURRENTH ]; then
     ASK_TO_REBOOT=1
    fi
    if [ $RET -eq 0 ]; then                         # 选择了YES，开启串口
      set_config_var enable_uart 1 $CONFIG
      HSTATUS=enabled
    elif [ $RET -eq 1 ]; then                       # 选择了NO，关闭串口引脚复用
      set_config_var enable_uart 0 $CONFIG
      HSTATUS=disabled
    else
      return $RET
    fi
  else
    return $RET
  fi
  if [ "$INTERACTIVE" = True ]; then                # 提示最终的选择状态
      whiptail --msgbox "The serial login shell is $SSTATUS\nThe serial interface is $HSTATUS" 20 60 1
  fi
}

[...省略]

do_interface_menu() {
  FUN=$(whiptail --title "Raspberry Pi Software Configuration Tool (raspi-config)" --menu "Interfacing Options" $WT_HEIGHT $WT_WIDTH $WT_MENU_HEIGHT --cancel-button Back --ok-button Select \
    "P1 Camera" "Enable/Disable connection to the Raspberry Pi Camera" \
    "P2 SSH" "Enable/Disable remote command line access to your Pi using SSH" \
    "P3 VNC" "Enable/Disable graphical remote access to your Pi using RealVNC" \
    "P4 SPI" "Enable/Disable automatic loading of SPI kernel module" \
    "P5 I2C" "Enable/Disable automatic loading of I2C kernel module" \
    "P6 Serial" "Enable/Disable shell and kernel messages on the serial connection" \
    "P7 1-Wire" "Enable/Disable one-wire interface" \
    "P8 Remote GPIO" "Enable/Disable remote access to GPIO pins" \
    3>&1 1>&2 2>&3)
  RET=$?
  if [ $RET -eq 1 ]; then
    return 0
  elif [ $RET -eq 0 ]; then
    case "$FUN" in
      P1\ *) do_camera ;;
      P2\ *) do_ssh ;;
      P3\ *) do_vnc ;;
      P4\ *) do_spi ;;
      P5\ *) do_i2c ;;
      P6\ *) do_serial ;;                       # 串口
      P7\ *) do_onewire ;;
      P8\ *) do_rgpio ;;
      *) whiptail --msgbox "Programmer error: unrecognized option" 20 60 1 ;;
    esac || whiptail --msgbox "There was an error running option $FUN" 20 60 1
  fi
}

[...省略]

#
# Interactive use loop
#
if [ "$INTERACTIVE" = True ]; then
  [ -e $CONFIG ] || touch $CONFIG
  calc_wt_size
  while true; do
    [...省略]
    elif [ $RET -eq 0 ]; then
      if is_pi ; then
        case "$FUN" in
          [...省略]
          5\ *) do_interface_menu ;;                # 接口选择
          [...省略]
        esac || whiptail --msgbox "There was an error running option $FUN" 20 60 1
      else
      [...省略]
  done
fi
```

## I2C Config Code Hacking

* raspi-config源代码:
  ```Shell
  get_i2c() {
    if grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?(=(on|true|yes|1))?(,.*)?$" $CONFIG; then
      echo 0
    else
      echo 1
    fi
  }
  
  do_i2c() {
    DEFAULT=--defaultno
    if [ $(get_i2c) -eq 0 ]; then                         # 检查i2c配置
      DEFAULT=
    fi
    if [ "$INTERACTIVE" = True ]; then
      whiptail --yesno "Would you like the ARM I2C interface to be enabled?" $DEFAULT 20 60 2
      RET=$?
    else
      RET=$1
    fi
    if [ $RET -eq 0 ]; then                               # 打开i2c
      SETTING=on
      STATUS=enabled
    elif [ $RET -eq 1 ]; then                             # 关闭i2c
      SETTING=off
      STATUS=disabled
    else
      return $RET
    fi
  
    set_config_var dtparam=i2c_arm $SETTING $CONFIG &&    # 设置当前选择
    # BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf
    if ! [ -e $BLACKLIST ]; then
      touch $BLACKLIST
    fi
    # 树莓派上的i2c master控制器驱动: i2c-bcm2708，这里将其注释掉，
    # 也就从黑名单中剔除，反过来就是允许加载i2c-bcm2708
    sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*i2c[-_]bcm2708\)/#\1/"
    # 加载i2c工具驱动
    sed /etc/modules -i -e "s/^#[[:space:]]*\(i2c[-_]dev\)/\1/"               # i2c-dev
    # 如果不存在，就直接添加
    if ! grep -q "^i2c[-_]dev" /etc/modules; then
      printf "i2c-dev\n" >> /etc/modules
    fi
    dtparam i2c_arm=$SETTING                              # 使用到设备树叠加层原理使能i2c的配置，这个很关键
    modprobe i2c-dev                                      # 加载驱动
  
    if [ "$INTERACTIVE" = True ]; then
      whiptail --msgbox "The ARM I2C interface is $STATUS" 20 60 1
    fi
  }
  ```
* 使能i2c:
  ```Shell
  pi@raspberrypi:/sys/class/i2c-adapter $ ls
  i2c-1
  pi@raspberrypi:/sys/class/i2c-adapter $ cd i2c-1
  pi@raspberrypi:/sys/class/i2c-adapter/i2c-1 $ ls
  delete_device  i2c-dev  new_device  power      uevent
  device         name     of_node     subsystem
  ```
* 通过适配器直接添加外设：
  ```Shell
  pi@raspberrypi:/sys/class/i2c-adapter/i2c-1 $ echo ds3231 0x68 | sudo tee new_device ds3231 0x68
  ```
