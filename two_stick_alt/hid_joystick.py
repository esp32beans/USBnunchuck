# SPDX-FileCopyrightText: Copyright (c) 2024 esp32beans@gmail.com
#
# SPDX-License-Identifier: MIT

"""
This code is based on the Adafruit hid_gamepad.py example. See boot.py for
the joystick HID report descriptor.
"""

import time

from adafruit_hid import find_device

class Joystick:
    """ # Joystick with 4 8-bit axes, 1 hat/dpad, 12 buttons """
    def __init__(self, devices):
        """Create a Joystick object that will send USB joystick HID reports.

        Devices can be a list of devices that includes a joystick device or a joystick device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._joystick_device = find_device(devices, usage_page=0x1, usage=0x04)

        # Reuse this bytearray to send joystick reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        self._report = bytearray(6)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(6)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0     # 12 buttons
        self._joy_x = 127           # 0..127..255
        self._joy_y = 127           # 0..127..255
        self._joy_z = 127           # 0..127..255
        self._joy_rz = 127          # 0..127..255
        self._hat = 15              # 0..7,15

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""

        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_joysticks(self, x=None, y=None):
        """Set and send the given joystick values.
        The joysticks will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        Any values left as ``None`` will not be changed.

        All values must be in the range 0 to 255.
        """
        if x is not None:
            self._joy_x = self._validate_joystick8_value(x)
        if y is not None:
            self._joy_y = self._validate_joystick8_value(y)
        self._send()

    def move_joysticks_right(self, x=None, y=None):
        """Set and send the given right joystick values.
        The joystick will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        Any values left as ``None`` will not be changed.

        All values must be in the range 0 to 255.
        """
        if x is not None:
            self._joy_z = self._validate_joystick8_value(x)
        if y is not None:
            self._joy_rz = self._validate_joystick8_value(y)
        self._send()

    def move_hat(self, direct):
        """ direct = 0..7 and 15 """
        if direct is not None:
            self._hat = self._validate_hat_value(direct)
            self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to center."""
        self._buttons_state = 0     # 12 buttons
        self._joy_x = 127           # 0..127..255
        self._joy_y = 127           # 0..127..255
        self._joy_z = 127           # 0..127..255
        self._joy_rz = 127          # 0..127..255
        self._hat = 15              # 0..7,15
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        self._report[0] = self._joy_x & 0xFF
        self._report[1] = self._joy_y & 0xFF
        self._report[2] = self._joy_z & 0xFF
        self._report[3] = self._joy_rz & 0xFF
        self._report[4] = (self._hat & 0x0F) | ((self._buttons_state & 0x0F) << 4)
        self._report[5] = (self._buttons_state >> 4) & 0xFF

        if always or self._last_report != self._report:
            self._joystick_device.send_report(self._report)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 12:
            raise ValueError("Button number must in range 1 to 12")
        return button

    @staticmethod
    def _validate_joystick8_value(value):
        if not 0 <= value <= 255:
            raise ValueError("Joystick value must be in range 0 to 255")
        return value

    @staticmethod
    def _validate_hat_value(value):
        if not ((0 <= value <= 7) or (value == 15)):
            raise ValueError("Hat value must be in range 0 to 7 and 15")
        return value
