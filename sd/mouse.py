from adafruit_hid.mouse import Mouse as Mousecode
from mouse import Mouse
app = {
    'name' : 'Mouse',
    'order' : 2,
    'macros' : [
        # 1st row ----------
        ('L', Mouse(Mousecode.LEFT_BUTTON)),
        ('M', Mouse(Mousecode.MIDDLE_BUTTON)),
        ('R', Mouse(Mousecode.RIGHT_BUTTON)),
        # 2nd row ----------
        ('ScrUp', Mouse([0,0,5])),
        ('', []),
        ('ScrDown', Mouse([0,0,-5])),
        # 3rd row ----------
        ('', []),
        ('Up', Mouse([0,-10,0])),
        ('', []),
        # 4th row ----------
        ('Left', Mouse([-10,0,0])),
        ('Down', Mouse([0,10,0])),
        ('Right', Mouse([10,0,0])),
        # Encoder button ---
        ("", []),
        # Encoder <<
        ("", []),
        # Encoder >>
        ("", []),
    ],
}
