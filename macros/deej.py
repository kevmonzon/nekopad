
# MACROPAD Hotkeys: Deej Compatibility

from customfunction import CustomFunction
import time
VOL_UP = "VOLUP"
VOL_DOWN = "VOLDOWN"
MUTE = "MUTE"
selectedApp = None
appValues = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
appSwitches = [True, True, True, True, True, True, True, True, True, True, True, True]

def setApp(macropad, *args, **kwargs):
    global selectedApp
    selectedApp = args[0]
    print("selected", selectedApp)


def sendValues(macropad, *args, **kwargs):
    if selectedApp is None:
        print("No app")
        return
    # global appValues
    # global appSwitches
    if kwargs["command"] == VOL_UP:
        appValues[selectedApp] = appValues[selectedApp] + 1
        if appValues[selectedApp] > 100:
            appValues[selectedApp] = 100
    if kwargs["command"] == VOL_DOWN:
        appValues[selectedApp] = appValues[selectedApp] - 1
        if appValues[selectedApp] < 0:
            appValues[selectedApp] = 0
    if kwargs["command"] == MUTE:
        appSwitches[selectedApp] = not appSwitches[selectedApp]

    out = []
    for idx, v in enumerate(appValues):
        if appSwitches[idx] == False:
            out.append(str(0))
        else:
            out.append(str(int(1023 * (v / 100))))
    string = "|".join(out)
    print(string)
    display_volume_screen(macropad, app["macros"][selectedApp][0], appValues[selectedApp])


## display override then time out
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import terminalio

from display import Display

def display_volume_screen(macropad, title='', volume=0):
    previous_group = macropad.display.root_group
    group = displayio.Group()
    group.append(Rect(0, 0, 128, 12, fill=0xFFFFFF))
    group.append(
        label.Label(
            terminalio.FONT,
            text=title,
            color=0x000000,
            anchored_position=(62, 0),
            anchor_point=(0.5, 0.0)
        )
    )
    group.append(
        label.Label(
            terminalio.FONT,
            text=str(volume)+"%",
            anchored_position=(64,25),
            anchor_point=(0.5,0.5)
        )
    )
    box_vol = int(128 * (volume/100))
    group.append(Rect(0, 40, box_vol, 24, fill=0xFFFFFF))
    macropad.display.root_group = group

    display = Display(macropad)
    display.reset_display()


app = {
    "name": "Deej",
    # 'order': 6,
    "macros": [
        ("Chrome", CustomFunction(setApp, 0)),
        ("Edge", CustomFunction(setApp, 1)),
        ("Discord", CustomFunction(setApp, 2)),
        ("-", CustomFunction(setApp, 3)),
        ("-", CustomFunction(setApp, 4)),
        ("-", CustomFunction(setApp, 5)),
        ("-", CustomFunction(setApp, 6)),
        ("-", CustomFunction(setApp, 7)),
        ("-", CustomFunction(setApp, 8)),
        ("Mic", CustomFunction(setApp, 9)),
        ("Current", CustomFunction(setApp, 10)),
        ("System", CustomFunction(setApp, 11)),
        ("x", CustomFunction(sendValues, command=MUTE)),
        ("-", CustomFunction(sendValues, command=VOL_DOWN)),
        ("+", CustomFunction(sendValues, command=VOL_UP)),
    ],
}
