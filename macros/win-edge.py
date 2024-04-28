# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Microsoft Edge web browser for Windows

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                      # REQUIRED dict, must be named 'app'
    'name' : 'Windows Edge', # Application name
    'macros' : [             # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('< Back', [Keycode.ALT, Keycode.LEFT_ARROW]),
        ('Fwd >', [Keycode.ALT, Keycode.RIGHT_ARROW]),
        ('Up', [Keycode.SHIFT, ' ']),      # Scroll up
        # 2nd row ----------
        ('- Size', [Keycode.CONTROL, Keycode.KEYPAD_MINUS]),
        ('Size +', [Keycode.CONTROL, Keycode.KEYPAD_PLUS]),
        ('Down', ' '),                     # Scroll down
        # 3rd row ----------
        ('Reload', [Keycode.CONTROL, 'r']),
        ('Home', [Keycode.ALT, Keycode.HOME]),
        ('Private', [Keycode.CONTROL, 'N']),
        # 4th row ----------
        ('Ada', [Keycode.CONTROL, 'n', -Keycode.COMMAND,
                           'www.adafruit.com\n']),   # Adafruit in new window
        ('Digi', [Keycode.CONTROL, 'n', -Keycode.COMMAND,
                            'www.digikey.com\n']),   # Digi-Key in new window
        ('Hacks', [Keycode.CONTROL, 'n', -Keycode.COMMAND,
                             'www.hackaday.com\n']), # Hack-a-Day in new win
        # Encoder button ---
        ('', [Keycode.CONTROL, 'w']) # Close tab
    ]
}
