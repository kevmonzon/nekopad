# MACROPAD Hotkeys: Helldiver II

import time
import supervisor
from sleeper import Sleep
from adafruit_hid.keycode import Keycode
from customfunction import CustomFunction
from keyboard import Keyboard
from adafruit_macropad import MacroPad
from display import Display

def restart():
    supervisor.reload()

def test_display_splash(macropad, kwargs):
    macropad.display_image(kwargs['file'])
    print(kwargs['display'])
    return

def checkargs(macropad, *args):
    for idx, i in args:
        print(idx+i)

app = {
    'name' : 'System',
    # 'order': 6,
    'macros' : [

        ('Restart', CustomFunction(restart)),
        ('CAD', [Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.DELETE]),
        ('', []),
        ('', []),
        ('', []),
        ('Splash', CustomFunction(test_display_splash, {'file': 'splash.bmp', 'display':'display this test'})),
        ('test', CustomFunction(checkargs, 'test', '1','3'))

    ]
}