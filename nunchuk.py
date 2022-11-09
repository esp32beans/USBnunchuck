# SPDX-FileCopyrightText: Copyright (c) 2022 esp32beans@gmail.com
#
# SPDX-License-Identifier: MIT

""" Convert Wii Nunchuk to USB joystick with 2 axes and 2 buttons
See boot.py for the creation of the USB HID joystick object.
See hid_joystick.py for the Joystick class.
"""

import board
import adafruit_nunchuk
import usb_hid

from hid_joystick import Joystick

js = Joystick(usb_hid.devices)

# For QT Py ESP32-S3 no PSRAM when using the STEMMA connector.
# This should work for other boards with STEMMA connectors.
nc = adafruit_nunchuk.Nunchuk(board.STEMMA_I2C())

while True:
    x, y = nc.joystick
    y = 255 - y
    js.move_joysticks(x, y)

    if nc.buttons.Z:
        js.press_buttons(1)
    else:
        js.release_buttons(1)
    if nc.buttons.C:
        js.press_buttons(2)
    else:
        js.release_buttons(2)
