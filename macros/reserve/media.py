# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Consumer Control codes (media keys)

# The syntax for Consumer Control macros is a little peculiar, in order to
# maintain backward compatibility with the original keycode-only macro files.
# The third item for each macro is a list in brackets, and each value within
# is normally an integer (Keycode), float (delay) or string (typed literally).
# Consumer Control codes are distinguished by enclosing them in a list within
# the list, which is why you'll see double brackets [[ ]] below.
# Like Keycodes, Consumer Control codes can be positive (press) or negative
# (release), and float values can be inserted for pauses.

# To reference Consumer Control codes, import ConsumerControlCode like so...
from adafruit_hid.consumer_control_code import ConsumerControlCode
from consumer import Toolbar

# You can still import Keycode as well if a macro file mixes types!
# See other macro files for typical Keycode examples.

app = {               # REQUIRED dict, must be named 'app'
    'name' : 'Media[]', # Application name
    'order' : 3,
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('', []),
        ('Vol+', [Toolbar(ConsumerControlCode.VOLUME_INCREMENT)]),
        ('Bright+', [Toolbar(ConsumerControlCode.BRIGHTNESS_INCREMENT)]),
        # 2nd row ----------
        ('', []),
        ('Vol-', [Toolbar(ConsumerControlCode.VOLUME_DECREMENT)]),
        ('Bright-', [Toolbar(ConsumerControlCode.BRIGHTNESS_DECREMENT)]),
        # 3rd row ----------
        ('', []),
        ('Mute', [Toolbar(ConsumerControlCode.MUTE)]),
        ('', []),
        # 4th row ----------
        ('<<', [Toolbar(ConsumerControlCode.SCAN_PREVIOUS_TRACK)]),
        ('Play/Pause', [Toolbar(ConsumerControlCode.PLAY_PAUSE)]),
        ('>>', [Toolbar(ConsumerControlCode.SCAN_NEXT_TRACK)]),
        # Encoder button ---
        ('', [])
    ]
}