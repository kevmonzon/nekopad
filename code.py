import keyfactory
from adafruit_macropad import MacroPad
from app import App
from display import Display

MACRO_FOLDER = '/macros'

macropad = MacroPad()
screen = Display(macropad)
last_position = None
last_position2 = 0
sleeping = False
last_encoder_switch = macropad.encoder_switch_debounced.pressed
last_encoder_switch2 = macropad.encoder2_switch_debounced.pressed
app_index = 0

# screen.splash_screen(file = 'splash.bmp', seconds = 1)
screen.initialize()
apps = App.load_all(MACRO_FOLDER)

if not apps:
    screen.setTitle('NO MACRO FILES FOUND')
    while True:
        pass

try: # Test the USB HID connection
    macropad.keyboard.release_all()
except OSError as err:
    print(err)
    screen.setTitle('NO USB CONNECTION')
    while True:
        pass

while True:

    ## treat encoder2 as input
    position2 = macropad.encoder2

    # if position2 != last_position2:
    if position2 > last_position2:
        print('++')
    if position2 < last_position2:
        print('--')

    macropad.encoder2_switch_debounced.update()
    encoder2_switch = macropad.encoder2_switch_debounced.pressed

    if encoder2_switch != last_encoder_switch2:
        last_encoder_switch2 = encoder2_switch
        key_number = 13
        pressed = encoder2_switch
        print(encoder2_switch)
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(app[app_index].macros):
            continue
        key_number = event.key_number
        pressed = event.pressed



    position = macropad.encoder
    if position != last_position:
        last_position = position
        app_index = position % len(apps)
        macropad.keyboard.release_all()
        screen.setApp(apps[app_index])

    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        key_number = 12
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    sequence = apps[app_index].macros[key_number][1] if key_number < 12  else []
    if pressed:
        if not sleeping and key_number < 12:
            print()
        elif key_number is 12:
            if not sleeping:
                screen.sleep()
            else:
                screen.resume()
            sleeping = not sleeping

        if type(sequence) is list:
            for item in sequence:
                if type(item) is list: # We have a macro to execute
                    for subitem in item: # Press the key combination
                        keyfactory.get(subitem).press(macropad)
                    for subitem in item: # Immediately release the key combo
                        keyfactory.get(subitem).release(macropad)
                else: # We have a key combination to press
                    keyfactory.get(item).press(macropad)
        else: # We just have a single command to execute
            keyfactory.get(sequence).press(macropad)

    else:
        if type(sequence) is list: 
            for item in sequence:
                if type(item) is not list: # Release any still-pressed key combinations
                    keyfactory.get(item).release(macropad)
                # Macro key cobinations should already have been released
        else: # Release any still-pressed single commands
            keyfactory.get(sequence).release(macropad)
        if not sleeping and key_number < 12: # No pixel for encoder button
            print()
