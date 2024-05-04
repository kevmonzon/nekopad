# Nekopad

A derivative of the
[Macropad Hotkeys](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/LICENSE)
example from the
[Adafruit Learning System Guide](https://learn.adafruit.com/macropad-hotkeys/project-code).

* Uses derived code from [deckerego/Macropad_Hotkeys](https://github.com/deckerego/Macropad_Hotkeys)

# Hardware
* Raspberry Pico W
* 0.96in OLED Display i2c
* x12 switches
* x2 rotary encoder

# Wiring
* Switches
  * GP1-12
* Rotary Switches
  * GP16-17
* Rotary Encoder
  * GP18-21
* Display
  * GP26-27

# Modifications
* Derivative of Adafruit Macropad Hardware and Software
* Used [deckerego/Macropad_Hotkeys] repo as basis for cleaned up files
* Used SSD1306 displayio driver
* No speaker, no RGB
* +1 Rotary encoder

## Using

Example implementation is provided at `sd/_template.py_`

Create a file under `macros/` and add 


## Configuration

The `macros/` folder has a list of macro templates to chose from, all of which
can be altered at your whim. First make sure to mount your Macropad in read/write
mode (see [Updating](#updating)) and then open up the `.py` examples in the
`macros/` folder. Note that each has a list of settings, including:

- The name that will show at the top of the OLED display
- The sequential order that it will be shown when rotating the encoder dial
- A list of macros, sorted by row

Each macro consists of an LED color, a label to appear on the OLED display,
and a sequence of keys. A "key" can be text, a keyboard key, a consumer control
key (like play/pause), a mouse action, or a MIDI note. More than one key can
be specified in a sequence.


## Installing

First make sure that your Macropad has the
[latest version of CircuitPython installed](https://circuitpython.org/board/adafruit_macropad_rp2040/).
See [https://learn.adafruit.com/adafruit-macropad-rp2040/circuitpython](https://learn.adafruit.com/adafruit-macropad-rp2040/circuitpython)
for instructions on how to update the Macropad to have the latest version of
CircuitPython.

When installing Macropad Hotkeys for the first time, extract the latest
[MacroPad Hotkeys.zip](https://github.com/deckerego/Macropad_Hotkeys/releases/latest)
into a directory, then copy the contents of that extracted archive
into the CIRCUITPY drive that appears when you plug in your Macropad.
Ensure that the contents of the `lib/` subdirectory are also copied - these are
the precompiled Adafruit libraries that power the Macropad.

