from consumer import Toolbar
from mouse import Mouse
from sleeper import Sleep
from keyboard import Keyboard
from midi import Midi
from customfunction import CustomFunction

def get(item):
    if isinstance(item, Toolbar):
        return item
    elif isinstance(item, Mouse):
        return item
    elif isinstance(item, Midi):
        return item
    elif isinstance(item, float):
        return Sleep(item)
    elif isinstance(item, CustomFunction):
        return item
    else:
        return Keyboard(item)


# might define custom types here