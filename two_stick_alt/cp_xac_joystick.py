# SPDX-FileCopyrightText: Copyright (c) 2024 esp32beans@gmail.com
#
# SPDX-License-Identifier: MIT

""" Convert Wii Nunchuk to USB joystick with 2 axes, 2 buttons and dpad.
See boot.py for the creation of the USB HID joystick object.
See hid_joystick.py for the Joystick class.
"""

import math
import board
import busio
import digitalio
import adafruit_nunchuk
import usb_hid
from hid_joystick import Joystick
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut

USE_HAT = False

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
js.reset_all()

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

def degree2direction(deg):
    """
    deg direction in degrees (0..359)
    return direction 0..7 where 0=N,1=NE,2=E,3=SE,4=S,5=SW,6=W,7=NW
    """
    return (int((deg + 22.5) / 45.0) + 2) & 0x07

def xy2direction(x, y):
    """ Convert (x,y) co-ords to direction """
    radians = math.atan2(y, x)
    degrees = radians * 180.0 / 3.1415926
    if degrees < 0.0:
        degrees += 360.0
    direction = degree2direction(degrees)
    # print(x, y, degrees, direction)
    return direction

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

        # accel = 0..512..1023
        accel = nc.acceleration
        if USE_HAT:
            x_motion = accel[0] - 512
            y_motion = 512 - accel[1]
            if abs(x_motion) > 16 or abs(y_motion) > 16:
                js.move_hat(xy2direction(x_motion, y_motion))
            else:
                js.move_hat(15)
        else:
            x_motion = accel[0]
            y_motion = accel[1]
            if abs(x_motion - 512) > 32 or abs(y_motion - 512) > 32:
                x_map = x_motion >> 2
                y_map = (1023 - y_motion) >> 2
                js.move_joysticks_right(x_map, y_map)
            else:
                js.move_joysticks_right(127, 127)

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
