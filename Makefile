EXTRA_CFLAGS:= -DCONFIG_IIO_BUFFER

obj-m += iio.o
iio-objs := industrialio-core.o \
        industrialio-event.o \
        inkern.o \
        industrialio-buffer.o \
        industrialio-trigger.o

obj-m += industrialio-configfs.o
obj-m += industrialio-sw-device.o 
obj-m += industrialio-sw-trigger.o 
obj-m += industrialio-triggered-event.o 

obj-y += buffer/
obj-y += st_magn/

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

modules_install: all
	mkdir -p install
	cp buffer/industrialio-buffer-cb.ko           install
	cp buffer/industrialio-buffer-dma.ko          install
	cp buffer/industrialio-buffer-dmaengine.ko    install
	cp buffer/industrialio-hw-consumer.ko         install
	cp buffer/industrialio-triggered-buffer.ko    install
	cp buffer/kfifo_buf.ko                        install
	cp iio.ko                                     install
	cp industrialio-configfs.ko                   install
	cp industrialio-sw-device.ko                  install
	cp industrialio-sw-trigger.ko                 install
	cp industrialio-triggered-event.ko            install
	cp st_magn/st_mag3d.ko                        install

