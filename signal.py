
class Signal(list):

    def connect(self, function):
        self.append(function)

    def disconnect(self, function):
        self.remove(function)

    def assigned(self):
        return len(self) > 0

    def emit(self, *args):
        for f in self: f(*args)

