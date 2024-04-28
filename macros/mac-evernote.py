# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys: Evernote web application for Mac
# Contributed by Redditor s010sdc

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                      # REQUIRED dict, must be named 'app'
    'name' : 'Mac Evernote', # Application name
    'macros' : [             # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('New Nt', [Keycode.COMMAND, 'n']),
        ('New Bk', [Keycode.SHIFT, Keycode.COMMAND, 'n']),
        ('CP Lnk', [Keycode.CONTROL, Keycode.OPTION, Keycode.COMMAND, 'c']),
        # 2nd row ----------
        ('Move', [Keycode.CONTROL, Keycode.COMMAND, 'm']),
        ('Find', [Keycode.OPTION, Keycode.COMMAND, 'f']),
        ('Emoji', [Keycode.CONTROL, Keycode.COMMAND, ' ']),
        # 3rd row ----------
        ('Bullets', [Keycode.SHIFT, Keycode.COMMAND, 'u']),
        ('Nums', [Keycode.SHIFT, Keycode.COMMAND, 'o']),
        ('Check', [Keycode.SHIFT, Keycode.COMMAND, 't']),
        # 4th row ----------
        ('Date', [Keycode.SHIFT, Keycode.COMMAND, 'D']),
        ('Time', [Keycode.OPTION, Keycode.SHIFT, Keycode.COMMAND, 'D']),
        ('Divider', [Keycode.SHIFT, Keycode.COMMAND, 'H']),
        # Encoder button ---
        ('', [Keycode.COMMAND, 'w']) # Close window/tab
    ]
}
