import usb_hid, usb_midi
usb_midi.disable()

# Joystick with 4 8-bit axes, 1 hat/dpad, 12 buttons
JOYSTICK_REPORT_DESCRIPTOR = bytes((
0x05,0x01,0x09,0x04,0xA1,0x01,0xA1,0x02,0x75,0x08,0x95,0x04,0x15,0x00,0x26,
0xFF,0x00,0x35,0x00,0x46,0xFF,0x00,0x09,0x30,0x09,0x31,0x09,0x32,0x09,0x35,
0x81,0x02,0x75,0x04,0x95,0x01,0x25,0x07,0x46,0x3B,0x01,0x65,0x14,0x09,0x39,
0x81,0x42,0x65,0x00,0x75,0x01,0x95,0x0C,0x25,0x01,0x45,0x01,0x05,0x09,0x19,
0x01,0x29,0x0C,0x81,0x02,0x06,0x00,0xFF,0x75,0x01,0x95,0x10,0x25,0x01,0x45,
0x01,0x09,0x01,0x81,0x02,0xC0,0xA1,0x02,0x75,0x08,0x95,0x07,0x46,0xFF,0x00,
0x26,0xFF,0x00,0x09,0x02,0x91,0x02,0xC0,0xC0))

joystick = usb_hid.Device(
    report_descriptor=JOYSTICK_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x04,                # Joystick
    report_ids=(0,),           # Descriptor uses report ID 0.
    in_report_lengths=(6,),    # This joystick sends 6 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable((joystick,))
