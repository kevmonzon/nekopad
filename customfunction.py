class CustomFunction:
    def __init__(self, function, *args):
        self.function = function
        self.args = args

    def press(self, macropad):
        self.function(macropad, *self.args)

    def release(self, macropad):
        macropad.keyboard.release_all()

