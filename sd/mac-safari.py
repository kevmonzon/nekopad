# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Safari web browser for Mac

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Mac Safari', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('< Back', [Keycode.COMMAND, '[']),
        ('Fwd >', [Keycode.COMMAND, ']']),
        ('Up', [Keycode.SHIFT, ' ']),      # Scroll up
        # 2nd row ----------
        ('< Tab', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        ('Tab >', [Keycode.CONTROL, Keycode.TAB]),
        ('Down', ' '),                     # Scroll down
        # 3rd row ----------
        ('Reload', [Keycode.COMMAND, 'r']),
        ('Home', [Keycode.COMMAND, 'H']),
        ('Private', [Keycode.COMMAND, 'N']),
        # 4th row ----------
        ('Ada', [Keycode.COMMAND, 'n', -Keycode.COMMAND,
                           'www.adafruit.com\n']),   # Adafruit in new window
        ('Digi', [Keycode.COMMAND, 'n', -Keycode.COMMAND,
                            'www.digikey.com\n']),   # Digi-Key in new window
        ('Hacks', [Keycode.COMMAND, 'n', -Keycode.COMMAND,
                             'www.hackaday.com\n']), # Hack-a-Day in new win
        # Encoder button ---
        ('', [Keycode.COMMAND, 'w']) # Close window/tab
    ]
}
