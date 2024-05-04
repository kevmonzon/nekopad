## TEMPLATE
app = {                      # (required) dict, must be named 'app'
    'name' : '',            # (required) Application name
    # 'order' : 0,           # (optional) order in menu
    'macros' : [             # (required) List of button macros...
        # LABEL KEY SEQUENCE
        # 1st row ----------
        ('',          []),
        ('',          []),
        ('',          []),
        # 2nd row ----------
        ('',          []),
        ('',          []),
        ('',          []),
        # 3rd row ----------
        ('',          []),
        ('',          []),
        ('',          []),
        # 4th row ----------
        ('',          []),
        ('',          []),
        ('',          []),
        # Encoder button ---
        ('',          []),
        # Encoder << -------
        ('',          []),
        # Encoder >> -------
        ('',          []),
    ]
}

######
# Blank
"""
('', [])
"""

# Inserting Text
"""
('', "Hello World")
"""

# Inserting ConsumerControl (generic hardware controls)
"""
from adafruit_hid.consumer_control_code import ConsumerControlCode
from consumer import Toolbar
('Play/Pause', Toolbar(ConsumerControlCode.PLAY_PAUSE))
"""

# Inserting Single Keypress
"""
from adafruit_hid.keycode import Keycode
('RETURN', Keycode.ENTER)
('W', Keycode.W)
"""

# Inserting MouseControl
"""
from adafruit_hid.mouse import Mouse as Mousecode
from mouse import Mouse
('LeftClick', Mouse(Mousecode.LEFT_BUTTON))
('MouseUp', Mouse([0, -10, 0]))
('MouseDown', Mouse([0, 10, 0]))
('MouseLeft', Mouse([-10, 0, 0]))
('MouseRight', Mouse([10, 0, 0]))
('ScrollUp', Mouse([0, 0, 10]))
('ScrollDown', Mouse([0, 0, -10]))
"""

# Inserting Keycombo
"""
from adafruit_hid.keycode import Keycode
('CTRL+ALT+DEL', [Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.DELETE])
"""

# Inserting combinations
"""
from keyboard import Keyboard
from adafruit_hid.keycode import Keycode
('Hi User', [
    [Keycode.SHIFT, Keycode.H],
    2.0,
    Keycode.I,
    Keycode.ENTER,
    1.0,
    [Keycode.U, Keycode.S],
    3.0,
    Keycode.E,
    Keycode.R
]),
"""

# Inserting custom functions
# Note that you will need to manage your own code here
"""
from customfunction import CustomFunction
import supervisor
def restart_pico(macropad):
    supervisor.reload()

('Restart', CustomFunction(restart_pico))
"""


# Running custom functions flows like this
# macro -> Keyfactory -> CustomFunction -> YOUR_FUNCTION
