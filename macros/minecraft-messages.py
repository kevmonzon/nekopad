# SPDX-FileCopyrightText: 2021 Henry Gabryjelski for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Minecraft Messaging

# NOTE: There appears to be a line length limit. Exceeding that limit appears
#       to result in silent failure.  Therefore, the key sequences are split
#       across multiple lines.

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

# NOTE: There appears to be some delay when bringing up the command screen.

DELAY_AFTER_SLASH = 0.80 # required so minecraft has time to bring up command screen
DELAY_BEFORE_RETURN = 0.10

# NOTE: On PC, characters are sometimes lost due to lag.  No simple fix for
#       lost keystrokes is known.  However, the commands do work most of the time.


app = {                          # REQUIRED dict, must be named 'app'
    'name' : 'Minecraft (/msg)', # Application name
    'macros' : [                 # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('list', [
            '/', DELAY_AFTER_SLASH,
            'list',
            DELAY_BEFORE_RETURN, Keycode.RETURN, -Keycode.RETURN]),
        ('list', [
            '/', DELAY_AFTER_SLASH,
            'list',
            DELAY_BEFORE_RETURN, Keycode.RETURN, -Keycode.RETURN]),
        ('list', [
            '/', DELAY_AFTER_SLASH,
            'list',
            DELAY_BEFORE_RETURN, Keycode.RETURN, -Keycode.RETURN]),
        # 2nd row ----------
        ('', []),
        ('', []),
        ('', []),
        # 3rd row ----------
        ('', []),
        ('', []),
        ('', []),
        # 4th row ----------
        ('bed', [
            '/', DELAY_AFTER_SLASH,
            'msg @a Time for bed!',
            DELAY_BEFORE_RETURN, Keycode.RETURN, -Keycode.RETURN]),
        ('bed', [
            '/', DELAY_AFTER_SLASH,
            'msg @a Time for bed!',
            DELAY_BEFORE_RETURN, Keycode.RETURN, -Keycode.RETURN]),
        ('bed', [
            '/', DELAY_AFTER_SLASH,
            'msg @a Time for bed!',
            DELAY_BEFORE_RETURN, Keycode.RETURN, -Keycode.RETURN]),
        # Encoder button ---
        ('', [])
    ]
}
