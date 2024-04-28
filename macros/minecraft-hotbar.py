# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Minecraft hotbar (inventory)

# Note: Must enable "full keyboad gameplay" for Prev/Next buttons to work.
#       This is found under "settings", then "keyboard and mouse".

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                          # REQUIRED dict, must be named 'app'
    'name' : 'Minecraft Hotbar', # Application name
    'macros' : [                 # List of button macros...
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
        ('Prev', [Keycode.PAGE_UP]),
        ('', []),
        ('Next', [Keycode.PAGE_DOWN]),
        # Encoder button ---
        ('', [])
    ]
}
