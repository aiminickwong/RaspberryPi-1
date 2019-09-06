# libdrm modetest

## source code

https://github.com/grate-driver/libdrm

## compile

* `sudo apt-get install xutils-dev`
* `sudo apt-gen install autogen autoconf libtool`
* `./autogen.sh`
* `./configure`
* `make`

## modetest

* `./modetest -c`
  ```
  [...省略]
  Connectors:
  id      encoder status          name            size (mm)       modes   encoders
  51      0       connected       HDMI-A-1        0x0             5       50
    modes:
          name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot)
    1024x768 60 1024 1048 1184 1344 768 771 777 806 65000 flags: nhsync, nvsync; type: driver
    800x600 60 800 840 968 1056 600 601 605 628 40000 flags: phsync, pvsync; type: driver
    800x600 56 800 824 896 1024 600 601 603 625 36000 flags: phsync, pvsync; type: driver
    848x480 60 848 864 976 1088 480 486 494 517 33750 flags: phsync, pvsync; type: driver
    640x480 60 640 656 752 800 480 490 492 525 25175 flags: nhsync, nvsync; type: driver
    props:
          1 EDID:
                  flags: immutable blob
                  blobs:
  
                  value:
          2 DPMS:
                  flags: enum
                  enums: On=0 Standby=1 Suspend=2 Off=3
                  value: 3
          5 link-status:
                  flags: enum
                  enums: Good=0 Bad=1
                  value: 0
          6 non-desktop:
                  flags: immutable range
                  values: 0 1
                  value: 0
          19 CRTC_ID:
                  flags: object
                  value: 0
  ```
* `./modetest -p`
  ```
  [...省略]
  CRTCs:
  id      fb      pos     size
  49      55      (0,0)   (0x0)
     0 0 0 0 0 0 0 0 0 0 flags: ; type:
    props:
          20 ACTIVE:
                  flags: range
                  values: 0 1
                  value: 0
          21 MODE_ID:
                  flags: blob
                  blobs:
  
                  value:
          18 OUT_FENCE_PTR:
                  flags: range
                  values: 0 18446744073709551615
                  value: 0
  
  Planes:
  id      crtc    fb      CRTC x,y        x,y     gamma size      possible crtcs
  28      49      55      0,0             0,0     0               0x00000001
    formats: XR24 AR24 RG16 RG24 BG24 YU16 YU12 YV12 NV12 NV21
    props:
          7 type:
                  flags: immutable enum
                  enums: Overlay=0 Primary=1 Cursor=2
                  value: 1
          16 FB_ID:
                  flags: object
                  value: 55
          17 IN_FENCE_FD:
                  flags: signed range
                  values: -1 2147483647
                  value: -1
          19 CRTC_ID:
                  flags: object
                  value: 49
          12 CRTC_X:
                  flags: signed range
                  values: -2147483648 2147483647
                  value: 0
          13 CRTC_Y:
                  flags: signed range
                  values: -2147483648 2147483647
                  value: 0
          14 CRTC_W:
                  flags: range
                  values: 0 2147483647
                  value: 1024
          15 CRTC_H:
                  flags: range
                  values: 0 2147483647
                  value: 768
          8 SRC_X:
                  flags: range
                  values: 0 4294967295
                  value: 0
          9 SRC_Y:
                  flags: range
                  values: 0 4294967295
                  value: 0
          10 SRC_W:
                  flags: range
                  values: 0 4294967295
                  value: 67108864
          11 SRC_H:
                  flags: range
                  values: 0 4294967295
                  value: 50331648
          27 IN_FORMATS:
                  flags: immutable blob
                  blobs:
  
                  value:
                          01000000000000000a00000018000000
                          03000000400000005852323441523234
                          52473136524732344247323459553136
                          59553132595631324e5631324e563231
                          ff030000000000000000000000000000
                          00000000000000000700000000000000
                          00000000000000000100000000000007
                          00010000000000000000000000000000
                          0400000000000007
                  in_formats blob decoded:
                           XR24:  LINEAR MOD_BROADCOM_VC4_T_TILED
                           AR24:  LINEAR MOD_BROADCOM_VC4_T_TILED
                           RG16:  LINEAR MOD_BROADCOM_VC4_T_TILED
                           RG24:  LINEAR
                           BG24:  LINEAR
                           YU16:  LINEAR
                           YU12:  LINEAR
                           YV12:  LINEAR
                           NV12:  LINEAR (UNKNOWN MODIFIER)
                           NV21:  LINEAR
          30 alpha:
                  flags: range
                  values: 0 65535
                  value: 65535
          31 rotation:
                  flags: bitmask
                  values: rotate-0=0x1 rotate-180=0x4 reflect-x=0x10 reflect-y=0x20
                  value: 1
          32 COLOR_ENCODING:
                  flags: enum
                  enums: ITU-R BT.601 YCbCr=0 ITU-R BT.709 YCbCr=1 ITU-R BT.2020 YCbCr=2
                  value: 0
          33 COLOR_RANGE:
                  flags: enum
                  enums: YCbCr limited range=0 YCbCr full range=1
                  value: 0
          34 zpos:
                  flags: range
                  values: 0 127
                  value: 0
  [...省略]
  ```
* `./modetest -s 51@42:1024x768 -v`

## Android modetest 

* [libdrm-imx Android modetest](https://github.com/ZengjfOS/RaspberryPi/tree/libdrm-imx_Android_modetest)