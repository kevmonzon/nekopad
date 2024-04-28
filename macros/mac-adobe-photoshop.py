# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Adobe Photoshop for Mac

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                       # REQUIRED dict, must be named 'app'
    'name' : 'Mac Photoshop', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('Undo', [Keycode.COMMAND, 'z']),
        ('Redo', [Keycode.COMMAND, 'Z']),
        ('Brush', 'B'),   # Cycle brush modes
        # 2nd row ----------
        ('B&W', 'd'),     # Default colors
        ('Marquee', 'M'), # Cycle rect/ellipse marquee (select)
        ('Eraser', 'E'),  # Cycle eraser modes
        # 3rd row ----------
        ('Swap', 'x'),    # Swap foreground/background colors
        ('Move', 'v'),    # Move layer
        ('Fill', 'G'),    # Cycle fill/gradient modes
        # 4th row ----------
        ('Eyedrop', 'I'), # Cycle eyedropper/measure modes
        ('Wand', 'W'),    # Cycle "magic wand" (selection) modes
        ('Heal', 'J'),    # Cycle "healing" modes
        # Encoder button ---
        ('', [Keycode.COMMAND, Keycode.OPTION, 'S']) # Save for web
    ]
}
