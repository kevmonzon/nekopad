class CustomFunction:
    def __init__(self, function, *kwargs):
        self.function = function
        self.kwargs = kwargs

    def press(self, macropad):
        self.function(macropad, *self.kwargs)

    def release(self, macropad):
        macropad.keyboard.release_all()