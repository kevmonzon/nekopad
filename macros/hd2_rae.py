# MACROPAD Hotkeys: Helldiver II

import time
import random
from adafruit_hid.keycode import Keycode
from customfunction import CustomFunction

START_INPUT_DELAY = 0.6
KEY_DELAY = 0.01

START_INPUT = Keycode.LEFT_CONTROL
# START_INPUT = Keycode.LEFT_SHIFT

UP = Keycode.UP_ARROW
DOWN = Keycode.DOWN_ARROW
LEFT = Keycode.LEFT_ARROW
RIGHT = Keycode.RIGHT_ARROW
# UP = Keycode.W
# DOWN = Keycode.S
# LEFT = Keycode.A
# RIGHT = Keycode.D

def stratagem(macropad, *argv):
    macropad.keyboard.press(START_INPUT)
    time.sleep(START_INPUT_DELAY)
    for key in argv:
        macropad.keyboard.press(key)
        random_number = random.randint(0,9) * 0.01
        macropad.keyboard.release(key)
        time.sleep(KEY_DELAY + random_number) 
    # macropad.keyboard.release(START_INPUT)
    
    # keys = [START_INPUT, START_INPUT_DELAY]
    # for key in argv:
    #     random_number = random.randint(0,9) * 0.01
    #     keys += [key, KEY_DELAY+random_number, -key, KEY_DELAY+random_number]
        
    # return keys
    time.sleep(1)


app = {
    'name' : 'Helldivers II',
    'order': 6,
    'macros' : [

        ('Shld', CustomFunction(stratagem, DOWN, UP, LEFT, RIGHT, LEFT, RIGHT)),
        ('Qsr', CustomFunction(stratagem, DOWN, DOWN, UP, LEFT, RIGHT)),
        ('EAirStr', CustomFunction(stratagem, UP, RIGHT, DOWN, RIGHT)),
        ('EClustr', CustomFunction(stratagem, UP, RIGHT, DOWN, DOWN, RIGHT)),
        ('',          []),
        ('',          []),
        ('',          []),
        ('',          []),
        ('',          []),
        ('',          []),
        ('1UP', CustomFunction(stratagem, UP, DOWN, RIGHT, LEFT, UP)),
        ('Resoup', CustomFunction(stratagem, DOWN, DOWN, UP, RIGHT)),
        
        # Encoder button ---
        ('',          []),
    ]
}