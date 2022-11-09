# Convert Wii Nunchunk to USB Joystick without soldering

![Photo of nunchuck connected to adapter and QT Py ESP32-S3](./images/USBnunchuck.jpg)

## Hardware

This project uses the same hardware as https://github.com/esp32beans/USBnunchuck_mouse.

* Adafruit QT Py ESP32-S3 with STEMMA QT, no PSRAM
* Adafruit STEMMA QT/Qwiic JST SH 4-pin cable
* Adafruit Wii Nunchuck Breakout Adapter - Qwiic/STEMMA QT
* Adafruit Wii controller (Nunchuck/Wiichuck)
* USB cable with Type C connector for the ESP32-S3 and the appropriate connector for your computer.

Plug the boards together as shown below. No soldering is needed.

```
ESP32-S3 --STEMMA-- Nunchuck adapter -- Nunchuck controller
```

## Tutorials

Recommended only if you want to change the Python code.

* [Adafruit QT Py ESP32-S3](https://learn.adafruit.com/adafruit-qt-py-esp32-s3)
* [Customizing USB Devices in CircuitPython](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices)
* [Adafruit Wii Nunchuck Breakout Adapter](https://learn.adafruit.com/adafruit-wii-nunchuck-breakout-adapter)

## CircuitPython files on the ESP32-S3

code.py is a renamed copy of nunchuk.py.

CircuitPython files and directories

```
└── CIRCUITPY
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
        └── adafruit_nunchuk.mpy
```
