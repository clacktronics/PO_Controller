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
        #print c
        #output = [0] * 65
        #output[c-1] = 255
        return c

    def reset(self):
        self.test_init = 1

class testAll(device):
    def __init__(self):
        self.connected = True
        self.toggle = True

    def __str__(self):
        return "testAll"

    def all(self, output):
        if output == True:
            return [255] * 64
        else:
            return [0] * 64

class fadeAll(device):
    def __init__(self):
        self.connected = True
        self.direction = 1
        self.test_init = 0

    def __str__(self):
        return "fadeAll"

    def reset(self):
        self.test_init = 0

    def fade(self):
        sleep(.05)
        c = self.test_init
        if self.test_init >= 255:
            self.direction = -1
        elif self.test_init <= 0:
            self.direction = 1
        self.test_init += self.direction
        print c
        output = [c] * 65
        return output
