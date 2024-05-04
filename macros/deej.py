# MACROPAD Hotkeys: Deej Compatibility

from customfunction import CustomFunction

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
    global appValues
    global appSwitches
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
