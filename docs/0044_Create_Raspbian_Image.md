# Create Raspbian Image

## 参考

* [pi-gen](https://github.com/RPi-Distro/pi-gen)

## config

```
export IMG_NAME=zengjf
```

## 运行build-docker.sh

* error
  ```
  I: Validating vim-common 2:8.1.0875-5
  I: Retrieving vim-tiny 2:8.1.0875-5
  I: Validating vim-tiny 2:8.1.0875-5
  I: Retrieving xxd 2:8.1.0875-5
  I: Validating xxd 2:8.1.0875-5
  I: Retrieving zlib1g 1:1.2.11.dfsg-1
  I: Validating zlib1g 1:1.2.11.dfsg-1
  rmdir: failed to remove '/pi-gen/work/2019-10-14-zengjf/stage0/rootfs/debootstrap': Directory not empty
  ```
* `/pi-gen/work/2019-10-14-zengjf/stage0/rootfs/debootstrap/debootstrap.log` 
  ```
  [...省略]
  2019-10-15 03:00:56 URL:http://mirrors.nju.edu.cn/raspbian/raspbian/pool/main/t/tasksel/tasksel-data_3.53_all.deb [17928/17928] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/tasksel-data_3.53_all.deb" [1]
  2019-10-15 03:01:02 URL:http://mirrors.nju.edu.cn/raspbian/raspbian/pool/main/t/traceroute/traceroute_2.1.0-2_armhf.deb [51310/51310] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/traceroute_1%3a2.1.0-2_armhf.deb" [1]
  2019-10-15 03:01:04 URL:http://mirrors.ustc.edu.cn/raspbian/raspbian/pool/main/t/tzdata/tzdata_2019c-0+deb10u1_all.deb [261272/261272] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/tzdata_2019c-0+deb10u1_all.deb" [1]
  2019-10-15 03:01:08 URL:http://mirrors.ustc.edu.cn/raspbian/raspbian/pool/main/s/systemd/udev_241-7~deb10u1+rpi1_armhf.deb [1246616/1246616] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/udev_241-7~deb10u1+rpi1_armhf.deb" [1]
  2019-10-15 03:01:36 URL:http://mirrors.nju.edu.cn/raspbian/raspbian/pool/main/u/util-linux/util-linux_2.33.1-0.1_armhf.deb [962124/962124] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/util-linux_2.33.1-0.1_armhf.deb" [1]
  2019-10-15 03:01:38 URL:http://mirrors.nju.edu.cn/raspbian/raspbian/pool/main/v/vim/vim-common_8.1.0875-5_all.deb [194748/194748] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/vim-common_2%3a8.1.0875-5_all.deb" [1]
  2019-10-15 03:01:45 URL:http://mirrors.nju.edu.cn/raspbian/raspbian/pool/main/v/vim/vim-tiny_8.1.0875-5_armhf.deb [502672/502672] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/vim-tiny_2%3a8.1.0875-5_armhf.deb" [1]
  2019-10-15 03:01:50 URL:http://mirrors.nju.edu.cn/raspbian/raspbian/pool/main/v/vim/xxd_8.1.0875-5_armhf.deb [139052/139052] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/xxd_2%3a8.1.0875-5_armhf.deb" [1]
  2019-10-15 03:01:52 URL:http://mirrors.nju.edu.cn/raspbian/raspbian/pool/main/z/zlib/zlib1g_1.2.11.dfsg-1_armhf.deb [87340/87340] -> "/home/pi/zengjf/pi-gen/work/2019-10-15-zengjf/stage0/rootfs//var/cache/apt/archives/partial/zlib1g_1%3a1.2.11.dfsg-1_armhf.deb" [1]
  cp: cannot stat 'debootstrap': No such file or directory
  ```
