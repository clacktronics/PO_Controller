from device import device
from time import sleep

class testCircle(device):
    def __init__(self):
        self.connected = True
        self.test_init = 1

    def __str__(self):
        return "testCircle"

    def circle(self):
        sleep(.2)
        c = self.test_init
        if self.test_init >= 64:
            self.test_init = 1
        else:
            self.test_init += 1
        output = [0] * 65
        output[c] = 255
        return output

    def reset(self):
        self.test_init = 1

class testAll(device):
    def __init__(self):
        self.connected = True
        self.toggle = True

    def __str__(self):
        return "testAll"

    def all(self):
        sleep(.6)
        output = self.toggle
        self.toggle = not self.toggle
        if output == True:
            return [255] * 64
        else:
            return [0] * 64
