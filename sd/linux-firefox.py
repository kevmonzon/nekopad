# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                       # REQUIRED dict, must be named 'app'
    'name' : 'Linux Firefox', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('< Back', [Keycode.CONTROL, '[']),
        ('Fwd >', [Keycode.CONTROL, ']']),
        ('Up', [Keycode.SHIFT, ' ']),      # Scroll up
        # 2nd row ----------
        ('< Tab', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        ('Tab >', [Keycode.CONTROL, Keycode.TAB]),
        ('Down', ' '),                     # Scroll down
        # 3rd row ----------
        ('Reload', [Keycode.CONTROL, 'r']),
        ('Home', [Keycode.CONTROL, 'h']),
        ('Private', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        # 4th row ----------
        ('Ada', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        ('Dev Mode', [Keycode.F12]),     # dev mode
        ('Digi', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
        # Encoder button ---
        ('', [Keycode.CONTROL, 'w']) # Close window/tab
    ]
}
