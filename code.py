import keyfactory
from adafruit_macropad import MacroPad
from app import App
from display import Display
import time
import rtc
MACRO_FOLDER = "/macros"

macropad = MacroPad()
screen = Display(macropad)
last_position = None
last_position2 = 0
last_encoder_key2 = None
sleeping = False
last_encoder_switch = macropad.encoder_switch_debounced.pressed
last_encoder_switch2 = macropad.encoder_switch_debounced2.pressed
key_count = 15  # key count
app_index = 0

# screen.splash_screen(file="splash.bmp", seconds=1)
# screen.initialize()
apps = App.load_all(MACRO_FOLDER)

if not apps:
    screen.setTitle("NO MACRO FILES FOUND")
    while True:
        pass

try:  # Test the USB HID connection
    macropad.keyboard.release_all()
except OSError as err:
    print(err)
    screen.setTitle("NO USB CONNECTION")
    while True:
        pass

prevTime = 0
timePassed = 0
while True:
    ## refresh screen whenever
    if timePassed == 3:
        screen.initialize()
        screen.setApp(apps[app_index])
        timePassed = 0
    timePassed = timePassed + (int(time.monotonic()) - prevTime)
    prevTime = int(time.monotonic())

    ## handles rot.enc.1 for selecting apps
    position = macropad.encoder
    if position != last_position:
        last_position = position
        app_index = position % len(apps)
        macropad.keyboard.release_all()
        screen.initialize()  ## re-init screen for stuff
        screen.setApp(apps[app_index])

    ### HANDLES KEYPRESSES
    macropad.encoder_switch_debounced.update()
    macropad.encoder_switch_debounced2.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    encoder_switch2 = macropad.encoder_switch_debounced2.pressed

    if encoder_switch != last_encoder_switch:  ## this is for rot.enc.1
        last_encoder_switch = encoder_switch
        key_number = 99  ## defines which key you want to trigger
        pressed = encoder_switch

    elif encoder_switch2 != last_encoder_switch2:  ## this is for rot.enc.2
        last_encoder_switch2 = encoder_switch2
        key_number = 12  ## defines which key you want to trigger
        pressed = encoder_switch2
    elif macropad.encoder2 != last_position2:  ## handles rotenc2 scroll
        if macropad.encoder2 < last_position2:
            key_number = 13
            pressed = True
            last_encoder_key2 = key_number
        if macropad.encoder2 > last_position2:
            key_number = 14
            pressed = True
            last_encoder_key2 = key_number
        last_position2 = macropad.encoder2
    else:
        if last_encoder_key2 != None:  ## clear macropad.encoder2 first
            key_number = last_encoder_key2
            pressed = False
            last_encoder_key2 = None
        else:  ## this is for the actual keypad
            event = macropad.keys.events.get()
            if not event or event.key_number >= len(apps[app_index].macros):
                continue  # No key events, or no corresponding macro, resume loop
            key_number = event.key_number
            pressed = event.pressed

    ### HANDLES KEYPRESSES
    sequence = apps[app_index].macros[key_number][1] if key_number < key_count else []
    if pressed:
        if type(sequence) is list:
            for item in sequence:
                if type(item) is list:  # We have a macro to execute
                    for subitem in item:  # Press the key combination
                        keyfactory.get(subitem).press(macropad)
                    for subitem in item:  # Immediately release the key combo
                        keyfactory.get(subitem).release(macropad)
                else:  # We have a key combination to press
                    keyfactory.get(item).press(macropad)
        else:  # We just have a single command to execute
            keyfactory.get(sequence).press(macropad)

    else:
        if type(sequence) is list:
            for item in sequence:
                if type(item) is not list:  # Release any still-pressed key combinations
                    keyfactory.get(item).release(macropad)
                # Macro key combinations should already have been released
        else:  # Release any still-pressed single commands
            keyfactory.get(sequence).release(macropad)
