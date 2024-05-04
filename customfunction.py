class CustomFunction:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def press(self, macropad):
        self.function(macropad, *self.args, **self.kwargs)

    def release(self, macropad):
        macropad.keyboard.release_all()