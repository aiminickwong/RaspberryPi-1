# README

## note

```
mek_8q:/ # modetest
CANNOT LINK EXECUTABLE "modetest": library "libdrm_android.so" not found
mek_8q:/ # cp /vendor/lib64/libdrm_android.so /system/lib64/
mek_8q:/ # modetest
[...省略]
Encoders:
id      crtc    type    possible crtcs  possible clones
81      45      LVDS    0x00000002      0xffffffff
83      71      LVDS    0x00000008      0xffffffff

Connectors:
id      encoder status          name            size (mm)       modes   encoders
82      81      connected       LVDS-1          158x211         1       81
  modes:
        name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot)
  1920x1080 63 1920 2040 2041 2042 1080 1124 1125 1126 145600 flags: ; type: preferred, driver
  props:
        1 EDID:
                flags: immutable blob
                blobs:

                value:
        2 DPMS:
                flags: enum
                enums: On=0 Standby=1 Suspend=2 Off=3
                value: 0
        5 link-status:
                flags: enum
                enums: Good=0 Bad=1
                value: 0
        7 non-desktop:
                flags: immutable range
                values: 0 1
                value: 0

[...省略]
```
