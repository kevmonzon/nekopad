# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Adobe Illustrator for Windows

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                         # REQUIRED dict, must be named 'app'
    'name' : 'Win Illustrator', # Application name
    'macros' : [                # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('Undo', [Keycode.CONTROL, 'z']),
        ('Redo', [Keycode.CONTROL, 'Z']),
        ('Pen', 'p'),     # Path-drawing tool
        # 2nd row ----------

        ('Select', 'v'),  # Select (path)
        ('Reflect', 'o'), # Reflect selection
        ('Rect', 'm'),    # Draw rectangle
        # 3rd row ----------
        ('Direct', 'a'),  # Direct (point) selection
        ('Rotate', 'r'),  # Rotate selection
        ('Oval', 'l'),    # Draw ellipse
        # 4th row ----------
        ('Eyedrop', 'i'), # Cycle eyedropper/measure modes
        ('Scale', 's'),   # Scale selection
        ('Text', 't'),    # Type tool
        # Encoder button ---
        ('', [Keycode.CONTROL, Keycode.ALT, 'S']) # Save for web
    ]
}
