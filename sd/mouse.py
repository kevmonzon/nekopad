# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Mouse control

# The syntax for Mouse macros is highly peculiar, in order to maintain
# backward compatibility with the original keycode-only macro files.
# The third item for each macro is a list in brackets, and each value within
# is normally an integer (Keycode), float (delay) or string (typed literally).
# Consumer Control codes were added as list-within-list, and then mouse
# further complicates this by adding dicts-within-list. Each mouse-related
# dict can have any mix of keys 'buttons' w/integer mask of button values
# (positive to press, negative to release), 'x' w/horizontal motion,
# 'y' w/vertical and 'wheel' with scrollwheel motion.

# To reference Mouse constants, import Mouse like so...
from adafruit_hid.mouse import Mouse
# You can still import Keycode and/or ConsumerControl as well if a macro file
# mixes types! See other macro files for typical Keycode examples.

app = {               # REQUIRED dict, must be named 'app'
    'name' : 'Mouse', # Application name
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('L', [{'buttons':Mouse.LEFT_BUTTON}]),
        ('M', [{'buttons':Mouse.MIDDLE_BUTTON}]),
        ('R', [{'buttons':Mouse.RIGHT_BUTTON}]),
        # 2nd row ----------
        ('', []),
        ('Up', [{'y':-10}]),
        ('', []),
        # 3rd row ----------
        ('Left', [{'x':-10}]),
        ('', []),
        ('Right', [{'x':10}]),
        # 4th row ----------
        ('', []),
        ('Down', [{'y':10}]),
        ('', []),
        # Encoder button ---
        ('', [])
    ]
}
