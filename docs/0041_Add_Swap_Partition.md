# Add Swap Partition

## 参考源代码

* [Linux 下 swap 分区及作用详解](https://blog.csdn.net/a860mhz/article/details/51124153)
* [Linux调整swap大小和swap性能优化](https://www.cnblogs.com/saneri/p/10319412.html)

## steps

```Console
pi@raspberrypi:~/zengjf $ mkdir swap
pi@raspberrypi:~/zengjf $ cd swap/
pi@raspberrypi:~/zengjf/swap $ dd if=/dev/zero of=swapfree bs=32k count=1024
1024+0 records in
1024+0 records out
33554432 bytes (34 MB, 32 MiB) copied, 0.202008 s, 166 MB/s
pi@raspberrypi:~/zengjf/swap $ ls
swapfree
pi@raspberrypi:~/zengjf/swap $ /sbin/mkswap swapfree
mkswap: swapfree: insecure permissions 0644, 0600 suggested.
Setting up swapspace version 1, size = 32 MiB (33550336 bytes)
no label, UUID=b93502fa-ca0e-42e4-bdc2-e0fbf5b6e3a8
pi@raspberrypi:~/zengjf/swap $ sudo /sbin/swapon swapfree
swapon: /home/pi/zengjf/swap/swapfree: insecure permissions 0644, 0600 suggested.
swapon: /home/pi/zengjf/swap/swapfree: insecure file owner 1000, 0 (root) suggested.
pi@raspberrypi:~/zengjf/swap $ free
free          freeze_graph
pi@raspberrypi:~/zengjf/swap $ free -m
              total        used        free      shared  buff/cache   available
Mem:           3854         195        3219          11         440        3526
Swap:           131           0         131
pi@raspberrypi:~/zengjf/swap $ /sbin/swapon -s
Filename                                Type            Size    Used    Priority
/var/swap                               file            102396  0       -2
/home/pi/zengjf/swap/swapfree           file            32764   0       -3
pi@raspberrypi:~/zengjf/swap $  cat /proc/sys/vm/swappiness
60
```