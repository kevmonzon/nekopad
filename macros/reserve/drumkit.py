# MACROPAD Hotkeys: Drum Kit
# https://en.wikipedia.org/wiki/General_MIDI#Percussion

from midi import Midi

app = {
    'name' : 'Drum Kit[]',
    'order': 9,
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        ('HatFot', Midi(44)),
        ('HatCls', Midi(42)),
        ('HatOpn', Midi(46)),
        # 2nd row ----------
        ('XStick', Midi(37)),
        ('Snare',  Midi(38)),
        ('Rod',    Midi(91)),
        # 3rd row ----------
        ('FlorTom', Midi(43)),
        ('LowTom',  Midi(47)),
        ('HiTom',   Midi(48)),
        # 4th row ----------
        ('Bass',    Midi(35)),
        ('Kick',    Midi(36)),
        ('Cowbell', Midi(56))
    ]
}