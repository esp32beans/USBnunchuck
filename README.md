# Convert Wii Nunchunk to USB Joystick without soldering

![Photo of nunchuck connected to adapter and QT Py ESP32-S3](./images/USBnunchuck.jpg)
![Photo of Xbox Adaptive Controller with nunchuck connected to QT Py 2040 and 4 arcade buttons](./images/xac_nunchuck_4buttons.jpg)

## Hardware

This project uses the same hardware as https://github.com/esp32beans/USBnunchuck_mouse.

* Adafruit QT Py ESP32-S3 with STEMMA QT, no PSRAM
* Adafruit QT Py RP2040
* Adafruit Trinkey QT2040 - RP2040 USB Key with Stemma QT
* Adafruit Feather RP2040
* Adafruit STEMMA QT/Qwiic JST SH 4-pin cable
* Adafruit Wii Nunchuck Breakout Adapter - Qwiic/STEMMA QT
* Adafruit Wii controller (Nunchuck/Wiichuck)
* USB cable with Type C connector for the ESP32-S3 and the appropriate connector for your computer.

Plug the boards together as shown below. No soldering is needed.

Only one of the QT Py, Trinkey, and Feather boards is needed. The Trinkey is
the cheapest. The RP2040 boards do not have WiFi or Bluetooth so are cheaper
and use much less power.

The ESP32-S3 includes WiFi and Bluetooth Low Energy which are not currently
used but might be in the future. The ESP32-S3 requires powering the XAC using a
wall adapter because the ESP32 uses much more current than the other boards.
The arcade buttons currently do not work on this board.

```
ESP32-S3 --STEMMA-- Nunchuck adapter -- Nunchuck controller
QT Py RP2040 --STEMMA-- Nunchuck adapter -- Nunchuck controller
Trinkey QT2040 --STEMMA-- Nunchuck adapter -- Nunchuck controller
Feather RP2040 --STEMMA-- Nunchuck adapter -- Nunchuck controller
```

Add four 30mm arcade buttons so the joystick has a total of six buttons. Still no
soldering. The arcade button board is sold without the buttons and cables.

* Adafruit LED Arcade Button 1x4 - STEMMA QT I2C Breakout - STEMMA QT / Qwiic
* Adafruit STEMMA QT/Qwiic JST SH 4-pin cable
* 4 X Arcade Button with LED - 30mm
* Arcade Button Quick-Connect Wire Pairs - 0.11" (10 pack)

## Tutorials

Recommended only if you want to change the Python code. Or if you are new to
CircuitPython. The first four guides include instructions on how to install
CircuitPython on the respective boards.

* [Adafruit QT Py ESP32-S3](https://learn.adafruit.com/adafruit-qt-py-esp32-s3)
* [Adafruit QT Py RP2040](https://learn.adafruit.com/adafruit-trinkey-qt2040)
* [Adafruit Trinkey QT2040](https://learn.adafruit.com/adafruit-qt-py-2040)
* [Adafruit Feather RP2040](https://learn.adafruit.com/adafruit-feather-rp2040-pico)
* [Customizing USB Devices in CircuitPython](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices)
* [Adafruit Wii Nunchuck Breakout Adapter](https://learn.adafruit.com/adafruit-wii-nunchuck-breakout-adapter)

This guide is for the arcade button board.

* [Adafruit LED Arcade Button 1x4 STEMMA QT](https://learn.adafruit.com/adafruit-led-arcade-button-qt)

## CircuitPython files

code.py is a renamed copy of nunchuk.py.

CircuitPython files and directories

```
CIRCUITPY/
├── boot_out.txt
├── boot.py
├── code.py
├── hid_joystick.py
└── lib
    ├── adafruit_bus_device
    │   ├── i2c_device.mpy
    │   ├── __init__.py
    │   └── spi_device.mpy
    ├── adafruit_hid
    │   ├── consumer_control_code.mpy
    │   ├── consumer_control.mpy
    │   ├── __init__.mpy
    │   ├── keyboard_layout_base.mpy
    │   ├── keyboard_layout_us.mpy
    │   ├── keyboard.mpy
    │   ├── keycode.mpy
    │   └── mouse.mpy
    ├── adafruit_nunchuk.mpy
    └── adafruit_seesaw
        ├── analoginput.mpy
        ├── attiny8x7.mpy
        ├── attinyx16.mpy
        ├── crickit.mpy
        ├── digitalio.mpy
        ├── __init__.py
        ├── keypad.mpy
        ├── neopixel.mpy
        ├── pwmout.mpy
        ├── robohat.mpy
        ├── rotaryio.mpy
        ├── samd09.mpy
        ├── seesaw.mpy
        └── tftshield18.mpy
```

## Two Stick example

```
├── two_stick
│   ├── boot.py
│   ├── cp_xac_joystick.py
│   ├── hid_joystick.py
│   ├── LICENSE
│   ├── README.md
```

The two_stick example controls both Xbox Adaptive Controller joysticks
using one nunchuk.

The two_stick example uses the same CP libs and hardware but presents the
USB joystick with X axis, Y axis, an 8 way directional pad (dpad), and
two buttons.

The Windows joystick control panel shows the nunchuk thumb stick controls the
USB joystick X and Y axes as before. Tilting the nunchuk controls the USB
joystick dpad. This means means one nunchuk can control the X, Y, dpad, and two
buttons.

When plugged into an Xbox Adaptive Controller (XAC), the dpad can be mapped to
either the XAC left or right joystick. The result is one nunchuk can control
both the XAC left and right joysticks. This requires the XAC run the firmware
released in June 2024 or newer. The latest XAC firmware can be installed using
the Xbox Accessory app on an Xbox console or a Windows PC.

The following explains how to map the XAC dpad buttons to the XAC right
joystick.

https://github.com/touchgadget/xac_onehand_controller

## Two Stick Alt example

```
├── two_stick_alt
│   ├── boot.py
│   ├── cp_xac_joystick.py
│   ├── hid_joystick.py
│   ├── LICENSE
│   ├── README.md
```

The two_stick_alt example controls both Xbox Adaptive Controller joysticks
using one nunchuk. This version does not use the XAC direction pad so does not
require mapping the XAC dpad to an XAC joystick.

The two_stick_alt example uses the same CP libs and hardware but presents
the USB joystick with X axis, Y axis, X2 axis, Y2 axis, and two buttons.

The Windows joystick control panel shows the nunchuk thumb stick controls
the USB joystick X and Y axes as before. Tilting the nunchuk controls the
other/second USB joystick. This means means one nunchuk can control two
joysticks and 2 buttons without using the Xbox Accessory app.

The nunchuk accelerometer used to detect tilting is not as precise as the
thumb joystick so use the Xbox Accesory app to calibrate both joysticks.
The Xbox Accessory app can also change the joystick sensitivity so it can
be fine tuned to your style of play.

## Testing as of Aug 24, 2024

Works on XBox Adaptive Controller.

Tested using CircuitPython 9.1.2. Files in lib/ directory from
adafruit-circuitpython-bundle-9.x-mpy-20240822.zip
