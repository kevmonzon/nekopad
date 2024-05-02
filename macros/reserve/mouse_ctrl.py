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
# from adafruit_hid.mouse import Mouse as MouseCode
# from mouse import Mouse

# You can still import Keycode and/or ConsumerControl as well if a macro file
# mixes types! See other macro files for typical Keycode examples.
from adafruit_hid.mouse import Mouse as MouseCode # REQUIRED if using Keycode.* values
from mouse import Mouse
app = {               # REQUIRED dict, must be named 'app'
    'name' : 'MouseC', # Application name
    'order' : 2,
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('L', Mouse(MouseCode.LEFT_BUTTON)),
        ('M', Mouse(MouseCode.MIDDLE_BUTTON)),
        ('R', Mouse(MouseCode.RIGHT_BUTTON)),
        # 2nd row ----------
        # ('ScrUp', Mouse(MouseCode.move(0,0,-5))),
        # ('Up', Mouse(MouseCode.move(0,-10,0))),
        # ('ScrDown', Mouse(MouseCode.move(0,0,5))),
        ('ScrUp', Mouse([0,0,-5])),
        ('', []),
        ('ScrDown', Mouse([0,0,5])),
        # 3rd row ----------
        ('', []),
        ('Up', Mouse([0,-10,0])),
        ('', []),
        # ('Right', Mouse(MouseCode.move(10,0,0))),
        # 4th row ----------
        ('Left', Mouse([-10,0,0])),
        ('Down', Mouse([0,10,0])),
        ('Right', Mouse([10,0,0])),
        # Encoder button ---
        ('', [])
    ]
}
