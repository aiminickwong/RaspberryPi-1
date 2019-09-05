#!/bin/bash

if [ ! $# -eq 1 ]; then
        echo "USAGE:"
        echo "    modules.sh insmod"
        exit
fi

echo "cmd: $1"


if [ "$1" == "insmod" ]; then
        sudo insmod install/iio.ko
        sudo insmod install/industrialio-configfs.ko
        sudo insmod install/industrialio-sw-device.ko
        sudo insmod install/industrialio-sw-trigger.ko
        sudo insmod install/industrialio-triggered-event.ko
        
        sudo insmod install/kfifo_buf.ko
        sudo insmod install/industrialio-buffer-cb.ko
        sudo insmod install/industrialio-hw-consumer.ko
        sudo insmod install/industrialio-triggered-buffer.ko
        
        sudo insmod install/st_mag3d.ko
elif [ "$1" == "rmmod" ]; then
        sudo rmmod st_mag3d.ko

        sudo rmmod industrialio-triggered-buffer.ko
        sudo rmmod industrialio-hw-consumer.ko
        sudo rmmod industrialio-buffer-cb.ko
        sudo rmmod kfifo_buf.ko

        sudo rmmod industrialio-triggered-event.ko
        sudo rmmod industrialio-sw-trigger.ko
        sudo rmmod industrialio-sw-device.ko
        sudo rmmod industrialio-configfs.ko

        sudo rmmod iio.ko
fi
