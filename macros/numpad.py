from adafruit_hid.keycode import Keycode

app = {
    "name": "Numpad",
    "order": 1,
    "macros": [
        # 1st row ----------
        ("7", Keycode.KEYPAD_SEVEN),
        ("8", Keycode.KEYPAD_EIGHT),
        ("9", Keycode.KEYPAD_NINE),
        # 2nd row ----------
        ("4", Keycode.KEYPAD_FOUR),
        ("5", Keycode.KEYPAD_FIVE),
        ("6", Keycode.KEYPAD_SIX),
        # 3rd row ----------
        ("1", Keycode.KEYPAD_ONE),
        ("2", Keycode.KEYPAD_TWO),
        ("3", Keycode.KEYPAD_THREE),
        # 4th row ----------
        ("0", Keycode.KEYPAD_ZERO),
        (".", Keycode.KEYPAD_PERIOD),
        ("=", Keycode.KEYPAD_ENTER),
        # Encoder button ---
        ("", Keycode.BACKSPACE),
        # Encoder <<
        ("", Keycode.LEFT_ARROW),
        # Encoder >>
        ("", Keycode.RIGHT_ARROW),
    ],
}
