# SPDX-FileCopyrightText: Copyright (c) 2022 esp32beans@gmail.com
#
# SPDX-License-Identifier: MIT

""" Convert Wii Nunchuk to USB joystick with 2 axes and 2 buttons
See boot.py for the creation of the USB HID joystick object.
See hid_joystick.py for the Joystick class.
"""

import board
import busio
import adafruit_nunchuk
import usb_hid

from hid_joystick import Joystick

js = Joystick(usb_hid.devices)

# This should work for all boards with STEMMA connectors.
i2c = board.STEMMA_I2C()

if board.board_id in ('adafruit_qt2040_trinkey', 'adafruit_qtpy_rp2040',
        'adafruit_feather_rp2040'):
    i2c.try_lock()
    i2c.scan()
    i2c.unlock()

nc = adafruit_nunchuk.Nunchuk(i2c)

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
