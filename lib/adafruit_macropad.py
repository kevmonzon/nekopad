import busio
import adafruit_displayio_ssd1306
from displayio import I2CDisplay as I2CDisplayBus

import board
import digitalio
import rotaryio
import keypad
import displayio

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_base import KeyboardLayoutBase
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange
from adafruit_simple_text_display import SimpleTextDisplay
from adafruit_debouncer import Debouncer

try:
  # Only used for typing
  from typing import Tuple, Optional, Union, Iterator
  from keypad import Keys
  import adafruit_hid  # pylint:disable=ungrouped-imports
except ImportError:
  pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MacroPad.git"


displayio.release_displays()

display_i2c = busio.I2C(board.GP27, board.GP26)
display_bus = I2CDisplayBus(display_i2c, device_address=0x3C)
BOARD_DISPLAY = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)


ROTATED_KEYMAP_0 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
ROTATED_KEYMAP_90 = (2, 5, 8, 11, 1, 4, 7, 10, 0, 3, 6, 9)
ROTATED_KEYMAP_180 = (11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
ROTATED_KEYMAP_270 = (9, 6, 3, 0, 10, 7, 4, 1, 11, 8, 5, 2)

# See https://cdn-shop.adafruit.com/product-files/5228/5223-ds.pdf#page=13
_DISPLAY_SLEEP_COMMAND = 0xAE
_DISPLAY_WAKE_COMMAND = 0xAF

keycodes = Keycode


# pylint: disable=too-many-lines, disable=invalid-name, too-many-instance-attributes, too-many-public-methods, too-many-arguments
class MacroPad:
  Keycode = Keycode
  ConsumerControlCode = ConsumerControlCode
  Mouse = Mouse

  def __init__(
    self,
    rotation: int = 0,
    midi_in_channel: int = 1,
    midi_out_channel: int = 1,
    layout_class: type[KeyboardLayoutBase] = KeyboardLayoutUS,
    keycode_class: type[Keycode] = Keycode,
  ):

    # Define rotary encoder and encoder switch:
    self._encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP18)
    self._encoder_switch = digitalio.DigitalInOut(board.GP0)
    self._encoder_switch.switch_to_input(pull=digitalio.Pull.UP)
    self._debounced_switch = Debouncer(self._encoder_switch)

    # RAE
    self._encoder2 = rotaryio.IncrementalEncoder(board.GP19, board.GP20)
    self._encoder2_switch = digitalio.DigitalInOut(board.GP21)
    self._encoder2_switch.switch_to_input(pull=digitalio.Pull.UP)
    self._debounced_switch2 = Debouncer(self._encoder2_switch)

    # Define display:
    if not isinstance(BOARD_DISPLAY, type(None)):
      self.display = BOARD_DISPLAY
      self.display.bus.send(_DISPLAY_WAKE_COMMAND, b"")
    self._display_sleep = False

    # Define key and pixel maps based on rotation:
    self._key_pins = None
    self._keys = None
    self.rotate(rotation)

    # Define HID:
    self._keyboard = None
    self._keyboard_layout = None
    self._consumer_control = None
    self._mouse = None
    self._layout_class = layout_class
    self.Keycode = keycode_class
    # pylint:disable=global-statement
    global keycodes
    keycodes = keycode_class
    # pylint:enable=global-statement

    # Define MIDI:
    try:
      self._midi = adafruit_midi.MIDI(
        midi_in=usb_midi.ports[0],
        # MIDI uses channels 1-16. CircuitPython uses 0-15. Ergo -1.
        in_channel=midi_in_channel - 1,
        midi_out=usb_midi.ports[1],
        out_channel=midi_out_channel - 1,
      )
    except IndexError:
      # No MIDI ports available.
      self._midi = None

  def rotate(self, rotation):
    if rotation not in (0, 90, 180, 270):
      raise ValueError("Only 90 degree rotations are supported.")

    self._rotation = rotation

    def _keys_and_pixels(
      order: Tuple[int, int, int, int, int, int, int, int, int, int, int, int]
    ) -> None:
      self._key_pins = [getattr(board, "GP%d" % (num + 1)) for num in order]

    if rotation == 0:
      _keys_and_pixels(order=ROTATED_KEYMAP_0)

    if rotation == 90:
      _keys_and_pixels(order=ROTATED_KEYMAP_90)

    if rotation == 180:
      _keys_and_pixels(order=ROTATED_KEYMAP_180)

    if rotation == 270:
      _keys_and_pixels(order=ROTATED_KEYMAP_270)

    # Define keys:
    if self._keys is not None:
      self._keys.deinit()
    self._keys = keypad.Keys(self._key_pins, value_when_pressed=False, pull=True)

    self.display.rotation = rotation

  @property
  def rotation(self) -> int:
    return self._rotation

  @rotation.setter
  def rotation(self, new_rotation) -> None:
    self.rotate(new_rotation)

  @property
  def display_sleep(self) -> bool:
    return self._display_sleep

  @display_sleep.setter
  def display_sleep(self, sleep: bool) -> None:
    if self._display_sleep == sleep:
      return
    if sleep:
      command = _DISPLAY_SLEEP_COMMAND
    else:
      command = _DISPLAY_WAKE_COMMAND
    self.display.bus.send(command, b"")
    self._display_sleep = sleep

  @property
  def red_led(self) -> bool:
    return self._led.value

  @red_led.setter
  def red_led(self, value: bool) -> None:
    self._led.value = value

  @property
  def keys(self) -> Keys:
    return self._keys

  @property
  def encoder(self) -> int:
    """
    The rotary encoder relative rotation position. Always begins at 0 when the code is run, so
    the value returned is relative to the initial location.

    The following example prints the relative position to the serial console.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        while True:
            print(macropad.encoder)
    """
    return self._encoder.position * -1

  @property
  def encoder_switch(self) -> bool:
    """
    The rotary encoder switch. Returns ``True`` when pressed.

    The following example prints the status of the rotary encoder switch to the serial console.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        while True:
            print(macropad.encoder_switch)
    """
    return not self._encoder_switch.value

  @property
  def encoder_switch_debounced(self) -> Debouncer:
    """
    The rotary encoder switch debounced. Allows for ``encoder_switch_debounced.pressed`` and
    ``encoder_switch_debounced.released``. Requires you to include
    ``encoder_switch_debounced.update()`` inside your loop.

    The following example prints to the serial console when the rotary encoder switch is
    pressed and released.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        while True:
            macropad.encoder_switch_debounced.update()
            if macropad.encoder_switch_debounced.pressed:
                print("Pressed!")
            if macropad.encoder_switch_debounced.released:
                print("Released!")
    """
    self._debounced_switch.pressed = self._debounced_switch.fell
    self._debounced_switch.released = self._debounced_switch.rose
    return self._debounced_switch

  @property
  def encoder2(self) -> int:
    return self._encoder2.position * -1

  @property
  def encoder2_switch(self) -> bool:
    return not self._encoder2_switch.value

  @property
  def encoder2_switch_debounced(self) -> Debouncer:
    self._debounced_switch2.pressed = self._debounced_switch2.fell
    self._debounced_switch2.released = self._debounced_switch2.rose
    return self._debounced_switch2

  @property
  def keyboard(self) -> adafruit_hid.keyboard.Keyboard:
    """
    A keyboard object used to send HID reports. For details, see the ``Keyboard`` documentation
    in CircuitPython HID: https://circuitpython.readthedocs.io/projects/hid/en/latest/index.html

    The following example types out the letter "a" when the rotary encoder switch is pressed.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        while True:
            if macropad.encoder_switch:
                macropad.keyboard.send(macropad.Keycode.A)
    """
    if self._keyboard is None:
        self._keyboard = Keyboard(usb_hid.devices)
    return self._keyboard

  @property
  def keyboard_layout(self) -> adafruit_hid.keyboard_layout_base.KeyboardLayoutBase:
    """
    Map ASCII characters to the appropriate key presses on a standard US PC keyboard.
    Non-ASCII characters and most control characters will raise an exception. Required to send
    a string of characters.

    The following example sends the string ``"Hello World"`` when the rotary encoder switch is
    pressed.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        while True:
            if macropad.encoder_switch:
                macropad.keyboard_layout.write("Hello World")
    """
    if self._keyboard_layout is None:
        # This will need to be updated if we add more layouts. Currently there is only US.
        self._keyboard_layout = self._layout_class(self.keyboard)
    return self._keyboard_layout

  @property
  def consumer_control(self) -> adafruit_hid.consumer_control.ConsumerControl:
    """
    Send ConsumerControl code reports, used by multimedia keyboards, remote controls, etc.

    The following example decreases the volume when the rotary encoder switch is pressed.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        while True:
            if macropad.encoder_switch:
                macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_DECREMENT)
    """
    if self._consumer_control is None:
        self._consumer_control = ConsumerControl(usb_hid.devices)
    return self._consumer_control

  @property
  def mouse(self) -> adafruit_hid.mouse.Mouse:
    """
    Send USB HID mouse reports.

    The following example sends a left mouse button click when the rotary encoder switch is
    pressed.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        while True:
            if macropad.encoder_switch:
                macropad.mouse.click(macropad.Mouse.LEFT_BUTTON)
    """
    if self._mouse is None:
        self._mouse = Mouse(usb_hid.devices)
    return self._mouse

  @property
  def midi(self) -> adafruit_midi.MIDI:
    """
    The MIDI object. Used to send and receive MIDI messages. For more details, see the
    ``adafruit_midi`` documentation in CircuitPython MIDI:
    https://circuitpython.readthedocs.io/projects/midi/en/latest/

    The following example plays a single note by MIDI number, at full velocity.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("NoteOn/NoteOff MIDI using note number")
        macropad.midi.send(macropad.NoteOn(44, 127))
        time.sleep(0.5)
        macropad.midi.send(macropad.NoteOff(44, 0))
        time.sleep(1)

    The following example reads incoming MIDI messages.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("Read incoming MIDI messages")
        msg_in = macropad.midi.receive()
        if msg_in is not None:
            print("Received:", msg_in.__dict__)
    """
    return self._midi

  @staticmethod
  def NoteOn(
    note: Union[int, str], velocity: int = 127, *, channel: Optional[int] = None
  ) -> NoteOn:
    """
    Note On Change MIDI message. For more details, see the ``adafruit_midi.note_on``
    documentation in CircuitPython MIDI:
    https://circuitpython.readthedocs.io/projects/midi/en/latest/

    :param note: The note (key) number either as an int (0-127) or a str which is parsed, e.g.
                  “C4” (middle C) is 60, “A4” is 69.
    :param velocity: The strike velocity, 0-127, 0 is equivalent to a Note Off, defaults to
                      127.
    :param channel: The channel number of the MIDI message where appropriate. This is updated
                    by MIDI.send() method.

    The following example plays a single note by MIDI number, at full velocity.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("NoteOn/NoteOff MIDI using note number")
        macropad.midi.send(macropad.NoteOn(44, 127))
        time.sleep(0.5)
        macropad.midi.send(macropad.NoteOff(44, 0))
        time.sleep(1)

    The following example plays a chord.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("Multiple notes on/off in one message")
        macropad.midi.send([macropad.NoteOn(44, 127),
                            macropad.NoteOn(48, 127),
                            macropad.NoteOn(51, 127)])
        time.sleep(1)
        macropad.midi.send([macropad.NoteOff(44, 0),
                            macropad.NoteOff(48, 0),
                            macropad.NoteOff(51, 0)])
        time.sleep(1)
    """
    return NoteOn(note=note, velocity=velocity, channel=channel)

  @staticmethod
  def NoteOff(
    note: Union[int, str], velocity: int = 127, *, channel: Optional[int] = None
  ) -> NoteOff:
    """
    Note Off Change MIDI message. For more details, see the ``adafruit_midi.note_off``
    documentation in CircuitPython MIDI:
    https://circuitpython.readthedocs.io/projects/midi/en/latest/

    :param note: The note (key) number either as an int (0-127) or a str which is parsed, e.g.
                  “C4” (middle C) is 60, “A4” is 69.
    :param velocity: The release velocity, 0-127, defaults to 0.
    :param channel: The channel number of the MIDI message where appropriate. This is updated
                    by MIDI.send() method.

    The following example plays a single note by MIDI number, at half velocity.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("NoteOn/NoteOff using note name")
        macropad.midi.send(macropad.NoteOn("G#2", 64))
        time.sleep(0.5)
        macropad.midi.send(macropad.NoteOff("G#2", 0))
        time.sleep(1)
    """
    return NoteOff(note=note, velocity=velocity, channel=channel)

  @staticmethod
  def PitchBend(pitch_bend: int, *, channel: Optional[int] = None) -> PitchBend:
    """
    Pitch Bend Change MIDI message. For more details, see the ``adafruit_midi.pitch_bend``
    documentation in CircuitPython MIDI:
    https://circuitpython.readthedocs.io/projects/midi/en/latest/

    :param pitch_bend: A 14bit unsigned int representing the degree of bend from 0 through 8192
                        (midpoint, no bend) to 16383.
    :param channel: The channel number of the MIDI message where appropriate. This is updated
                    by MIDI.send() method.

    The following example sets a pitch bend.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("Set pitch bend")
        macropad.midi.send(macropad.PitchBend(4096))

    The following example sweeps a pitch bend.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("Sweep pitch bend")
        for i in range(0, 4096, 8):
            macropad.midi.send(macropad.PitchBend(i))
        for i in range(0, 4096, 8):
            macropad.midi.send(macropad.PitchBend(4096-i))
    """
    return PitchBend(pitch_bend=pitch_bend, channel=channel)

  @staticmethod
  def ControlChange(
    control: int, value: int, *, channel: Optional[int] = None
  ) -> ControlChange:
    """
    Control Change MIDI message. For more details, see the ``adafruit_midi.control_change``
    documentation in CircuitPython MIDI:
    https://circuitpython.readthedocs.io/projects/midi/en/latest/

    :param control: The control number, 0-127.
    :param value: The 7bit value of the control, 0-127.
    :param channel: The channel number of the MIDI message where appropriate. This is updated
                    by MIDI.send() method.

    The following example sets a control change value.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("Set a CC value")
        macropad.midi.send(macropad.ControlChange(7, 64))

    The following example sweeps a control change value.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("Sweep a CC value")
        for i in range(127):
            macropad.midi.send(macropad.ControlChange(1, i))
            time.sleep(0.01)
        for i in range(127):
            macropad.midi.send(macropad.ControlChange(1, 127-i))
            time.sleep(0.01)
    """
    return ControlChange(control=control, value=value, channel=channel)

  @staticmethod
  def ProgramChange(patch: int, *, channel: Optional[int] = None) -> ProgramChange:
    """
    Program Change MIDI message. For more details, see the ``adafruit_midi.program_change``
    documentation in CircuitPython MIDI:
    https://circuitpython.readthedocs.io/projects/midi/en/latest/

    :param patch: The note (key) number either as an int (0-127) or a str which is parsed,
                  e.g. “C4” (middle C) is 60, “A4” is 69.
    :param channel: The channel number of the MIDI message where appropriate. This is updated
                    by MIDI.send() method.

    The following example sends a program change for bank switching.

    .. code-block:: python

        import time
        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        print("Send ProgramChange bank messages")
        macropad.midi.send(macropad.ProgramChange(63))
        time.sleep(2)
        macropad.midi.send(macropad.ProgramChange(8))
        time.sleep(2)
    """
    return ProgramChange(patch=patch, channel=channel)

  def display_image(
    self,
    file_name: Optional[str] = None,
    position: Optional[Tuple[int, int]] = None,
  ) -> None:
    """
    Display an image on the built-in display.

    :param str file_name: The path to a compatible bitmap image, e.g. ``"/image.bmp"``. Must be
                          a string.
    :param tuple position: Optional ``(x, y)`` coordinates to place the image.

    The following example displays an image called "image.bmp" located in / on the CIRCUITPY
    drive on the display.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad()

        macropad.display_image("image.bmp")

        while True:
            pass
    """
    if not file_name:
      return
    if not position:
      position = (0, 0)
    group = displayio.Group(scale=1)
    self.display.root_group = group
    with open(file_name, "rb") as image_file:
      background = displayio.OnDiskBitmap(image_file)
      sprite = displayio.TileGrid(
          background,
          pixel_shader=background.pixel_shader,
          x=position[0],
          y=position[1],
      )
      group.append(sprite)
      self.display.refresh()

  @staticmethod
  def display_text(
    title: Optional[str] = None,
    title_scale: int = 1,
    title_length: int = 80,
    text_scale: int = 1,
    font: Optional[str] = None,
  ) -> SimpleTextDisplay:
    """
    Display lines of text on the built-in display. Note that if you instantiate this without
    a title, it will display the first (``[0]``) line of text at the top of the display - use
    this feature to have a dynamic "title".

    :param str title: The title displayed above the data. Set ``title="Title text"`` to provide
                      a title. Defaults to None.
    :param int title_scale: Scale the size of the title. Not necessary if no title is provided.
                            Defaults to 1.
    :param int title_length: The maximum number of characters allowed in the title. Only
                                necessary if the title is longer than the default 80 characters.
                              Defaults to 80.
    :param int text_scale: Scale the size of the data lines. Scales the title as well.
                            Defaults to 1.
    :param ~FontProtocol|None font: The custom font to use to display the text. Defaults to the
                                    built-in ``terminalio.FONT``. For more details, see:
                                    https://docs.circuitpython.org/en/latest/shared-bindings/fontio/index.html

    The following example displays a title and lines of text indicating which key is pressed,
    the relative position of the rotary encoder, and whether the encoder switch is pressed.
    Note that the key press line does not show up until a key is pressed.

    .. code-block:: python

        from adafruit_bitmap_font import bitmap_font
        from adafruit_macropad import MacroPad
        from displayio import Bitmap

        macropad = MacroPad()

        custom_font = bitmap_font.load_font("/Arial12.bdf", Bitmap)
        text_lines = macropad.display_text(title="MacroPad Info", font=custom_font)

        while True:
            key_event = macropad.keys.events.get()
            if key_event:
                text_lines[0].text = "Key {} pressed!".format(key_event.key_number)
            text_lines[1].text = "Rotary encoder {}".format(macropad.encoder)
            text_lines[2].text = "Encoder switch: {}".format(macropad.encoder_switch)
            text_lines.show()
    """
    return SimpleTextDisplay(
      title=title,
      title_color=SimpleTextDisplay.WHITE,
      title_scale=title_scale,
      title_length=title_length,
      text_scale=text_scale,
      font=font,
      colors=(SimpleTextDisplay.WHITE,),
      display=BOARD_DISPLAY,
    )
