mkdir /sys/kernel/config/device-tree/overlays/sensehat
ls /sys/kernel/config/device-tree/overlays/sensehat
echo `cat /proc/device-tree/soc/i2c@7e804000/lsm9ds1-magn@1c/status`
cat rpi-sense-overlay.dtbo > /sys/kernel/config/device-tree/overlays/sensehat/dtbo
echo `cat /proc/device-tree/soc/i2c@7e804000/lsm9ds1-magn@1c/status`
rmdir /sys/kernel/config/device-tree/overlays/sensehat
