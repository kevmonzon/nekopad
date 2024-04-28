# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

# rae
from adafruit_hid.consumer_control_code import ConsumerControlCode

# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros"


# CLASSES AND FUNCTIONS ----------------
class App:
  """Class representing a host-side application, for which we have a set
  of macro sequences. Project code was originally more complex and
  this was helpful, but maybe it's excessive now?"""

  def __init__(self, appdata):
    self.name = appdata["name"]
    self.macros = appdata["macros"]

  def switch(self):
    """Activate application settings; update OLED labels and LED
    colors."""
    group[13].text = self.name  # Application name
    if self.name:
      rect.fill = 0xFFFFFF
    else:  # empty app name indicates blank screen for which we dimm header
      rect.fill = 0x000000
    for i in range(12):
      if i < len(self.macros):  # Key in use, set label + LED color
        group[i].text = self.macros[i][0]
      else:  # Key not in use, no label or LED
        group[i].text = ""
    macropad.keyboard.release_all()
    macropad.consumer_control.release()
    macropad.mouse.release_all()
    macropad.display.refresh()
## HELPERS

## SPLASH SCREEN
def splash_screen():
  macropad.display_image("test.bmp")
  macropad.display.refresh()
  time.sleep(2)

# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = True
splash_screen()

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
  x = key_index % 3
  y = key_index // 3
  group.append(
    label.Label(
      terminalio.FONT,
      text="",
      color=0xFFFFFF,
      anchored_position=(
        (macropad.display.width - 1) * x / 2,
        macropad.display.height - 1 - (3 - y) * 12,
      ),
      anchor_point=(x / 2, 1.0),
    )
  )
rect = Rect(0, 0, macropad.display.width, 13, fill=0xFFFFFF)
group.append(rect)
group.append(
  label.Label(
    terminalio.FONT,
    text="",
    color=0x000000,
    anchored_position=(macropad.display.width // 2, -2),
    anchor_point=(0.5, 0.0),
  )
)
macropad.display.root_group = group

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
  if filename.endswith(".py") and not filename.startswith("._"):
    try:
      module = __import__(MACRO_FOLDER + "/" + filename[:-3])
      apps.append(App(module.app))
    except (
      SyntaxError,
      ImportError,
      AttributeError,
      KeyError,
      NameError,
      IndexError,
      TypeError,
    ) as err:
      print("ERROR in", filename)
      import traceback

      traceback.print_exception(err, err, err.__traceback__)

if not apps:
  group[13].text = "NO MACRO FILES FOUND"
  macropad.display.refresh()
  while True:
    pass

last_position = 0
last_position2 = 0
last_encoder_switch = macropad.encoder_switch_debounced.pressed
last_encoder_switch2 = macropad.encoder2_switch_debounced.pressed
app_index = 0
apps[app_index].switch()

# MAIN LOOP ----------------------------
while True:
  ## treat encoder2 as keyboard??
  position2 = macropad.encoder2
  if position2 != last_position2:
    if position2 > last_position2:
      macropad.consumer_control.release()
      macropad.consumer_control.press(ConsumerControlCode.VOLUME_INCREMENT)
      macropad.consumer_control.release()
    if position2 < last_position2:
      macropad.consumer_control.release()
      macropad.consumer_control.press(ConsumerControlCode.VOLUME_DECREMENT)
      macropad.consumer_control.release()
    last_position2 = position2

  # Read encoder position. If it's changed, switch apps.
  position = macropad.encoder
  if position != last_position:
    app_index = position % len(apps)
    apps[app_index].switch()
    last_position = position

  # Handle encoder button. If state has changed, and if there's a
  # corresponding macro, set up variables to act on this just like
  # the keypad keys, as if it were a 13th key/macro.
  macropad.encoder_switch_debounced.update()
  encoder_switch = macropad.encoder_switch_debounced.pressed
  if encoder_switch != last_encoder_switch:
    last_encoder_switch = encoder_switch
    if len(apps[app_index].macros) < 13:
      continue  # No 13th macro, just resume main loop
    key_number = 12  # else process below as 13th macro
    pressed = encoder_switch
  else:
    event = macropad.keys.events.get()
    if not event or event.key_number >= len(apps[app_index].macros):
      continue  # No key events, or no corresponding macro, resume loop
    key_number = event.key_number
    pressed = event.pressed
  # If code reaches here, a key or the encoder button WAS pressed/released
  # and there IS a corresponding macro available for it...other situations
  # are avoided by 'continue' statements above which resume the loop.

  sequence = apps[app_index].macros[key_number][1]
  if pressed:
    # 'sequence' is an arbitrary-length list, each item is one of:
    # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
    # Negative integer: (absolute value) key released
    # Float (e.g. 0.25): delay in seconds
    # String (e.g. "Foo"): corresponding keys pressed & released
    # List []: one or more Consumer Control codes (can also do float delay)
    # Dict {}: mouse buttons/motion (might extend in future)

    for item in sequence:
      if isinstance(item, int):
        if item >= 0:
          macropad.keyboard.press(item)
        else:
          macropad.keyboard.release(-item)
      elif isinstance(item, float):
        time.sleep(item)
      elif isinstance(item, str):
        macropad.keyboard_layout.write(item)
      elif isinstance(item, list):
        for code in item:
          if isinstance(code, int):
            macropad.consumer_control.release()
            macropad.consumer_control.press(code)
          if isinstance(code, float):
            time.sleep(code)
      elif isinstance(item, dict):
        if "buttons" in item:
          if item["buttons"] >= 0:
            macropad.mouse.press(item["buttons"])
          else:
            macropad.mouse.release(-item["buttons"])
        macropad.mouse.move(
          item["x"] if "x" in item else 0,
          item["y"] if "y" in item else 0,
          item["wheel"] if "wheel" in item else 0,
        )
  else:
      # Release any still-pressed keys, consumer codes, mouse buttons
      # Keys and mouse buttons are individually released this way (rather
      # than release_all()) because pad supports multi-key rollover, e.g.
      # could have a meta key or right-mouse held down by one macro and
      # press/release keys/buttons with others. Navigate popups, etc.
    for item in sequence:
      if isinstance(item, int):
        if item >= 0:
          macropad.keyboard.release(item)
      elif isinstance(item, dict):
        if "buttons" in item:
          if item["buttons"] >= 0:
              macropad.mouse.release(item["buttons"])
    macropad.consumer_control.release()


