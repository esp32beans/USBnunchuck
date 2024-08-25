# SPDX-FileCopyrightText: Copyright (c) 2022, 2024 esp32beans@gmail.com
#
# SPDX-License-Identifier: MIT

""" Convert Wii Nunchuk to USB joystick with 2 axes and 2 buttons
See boot.py for the creation of the USB HID joystick object.
See hid_joystick.py for the Joystick class.
"""

import board
import busio
import digitalio
import adafruit_nunchuk
import usb_hid
from hid_joystick import Joystick
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut

while True:
    try:
        js = Joystick(usb_hid.devices)
    except OSError:
        print("USB joystick failed")
    else:
        break

# This should work for all boards with STEMMA connectors.
board.STEMMA_I2C().unlock()
i2c = board.STEMMA_I2C()

nc = adafruit_nunchuk.Nunchuk(i2c)

try:
    arcade_qt = Seesaw(i2c, addr=0x3A)
except ValueError:
    arcade_buttons = False
else:
    arcade_buttons = True
    # Button pins in order (1, 2, 3, 4)
    button_pins = (18, 19, 20, 2)
    buttons = []
    for button_pin in button_pins:
        button = DigitalIO(arcade_qt, button_pin)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        buttons.append(button)

    # LED pins in order (1, 2, 3, 4)
    led_pins = (12, 13, 0, 1)
    leds = []
    for led_pin in led_pins:
        led = PWMOut(arcade_qt, led_pin)
        leds.append(led)

while True:
    try:
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

        if arcade_buttons:
            for led_number, button in enumerate(buttons):
                if not button.value:
                    js.press_buttons(led_number + 3)
                    leds[led_number].duty_cycle = 65534
                else:
                    js.release_buttons(led_number + 3)
                    leds[led_number].duty_cycle = 0
    except OSError:
        print("USB failed")
