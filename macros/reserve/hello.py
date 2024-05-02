# MACROPAD Hotkeys: Test Hotkey Scenarios

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from consumer import Toolbar

app = {
    'name' : 'Test',
    'order': 4,
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ( 'Hello  ', [[Keycode.SHIFT, Keycode.H], [Keycode.E, Keycode.L, Keycode.L], Keycode.O]),
        ( 'World  ', [[Keycode.SHIFT, Keycode.W], 2.0, Keycode.O, 1.0, [Keycode.R, Keycode.L], 3.0, Keycode.D]),
        ( 'o      ', Keycode.O),
        # 2nd row ----------
        ( '       ', []),
        ( '       ', []),
        ( '       ', []),
        # 3rd row ----------
        ( '       ', []),
        ( '       ', []),
        ( '       ', []),
        # 4th row ----------
        ( '       ', []),
        ( '       ', []),
        ( 'HD', [
            [Keycode.LEFT_SHIFT, Keycode.H],
            5.0,
            [Keycode.LEFT_SHIFT, Keycode.E],
            5.0,
            [Keycode.LEFT_SHIFT, Keycode.L],
            5.0,
            [Keycode.LEFT_SHIFT, Keycode.L],
            5.0,
            [Keycode.LEFT_SHIFT, Keycode.O],
            5.0,
            ]),
    ]
}