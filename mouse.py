class Mouse:
    def __init__(self, keycode):
        self.keycode = keycode

    def press(self, macropad):
        if isinstance(self.keycode, list):
            self.move(macropad, self.keycode[0],self.keycode[1],self.keycode[2])
            return None
        if self.keycode < 0:
            macropad.mouse.release(self.keycode)
        else:
            macropad.mouse.press(self.keycode)

    def release(self, macropad):
        if isinstance(self.keycode, list):
            return None
        macropad.mouse.release(self.keycode)

    def move(self, macropad, x = 0, y = 0, z = 0):
        macropad.mouse.move(x,y,z)
