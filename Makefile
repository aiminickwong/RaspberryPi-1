all:
	dtc -I dts -O dtb -o rpi-sense-overlay.dtbo rpi-sense-overlay.dts

clean:
	rm rpi-sense-overlay.dtbo
