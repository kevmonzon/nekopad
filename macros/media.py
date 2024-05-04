from adafruit_hid.consumer_control_code import ConsumerControlCode
from consumer import Toolbar
app = {
    'name' : 'Media',
    'order' : 3,
    'macros' : [
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
        ('Play/Pause', Toolbar(ConsumerControlCode.PLAY_PAUSE)),
        ('>>', [Toolbar(ConsumerControlCode.SCAN_NEXT_TRACK)]),
        # Encoder button ---
        ("", []),
        # Encoder <<
        ("", []),
        # Encoder >>
        ("", []),
    ]
}
