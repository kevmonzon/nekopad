# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Universal Numpad

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                # REQUIRED dict, must be named 'app'
    'name' : 'Numpad', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('7', ['7']),
        ('8', ['8']),
        ('9', ['9']),
        # 2nd row ----------
        ('4', ['4']),
        ('5', ['5']),
        ('6', ['6']),
        # 3rd row ----------
        ('1', ['1']),
        ('2', ['2']),
        ('3', ['3']),
        # 4th row ----------
        ('*', ['*']),
        ('0', ['0']),
        ('#', ['#']),
        # Encoder button ---
        ('', [Keycode.BACKSPACE])
    ]
}
