import utils

class parLed():
    def __init__(self):
        self.numberOfLights = 64
        #
        # self.lightColours = ['Red', 'Green', 'Blue', 'White', 'Zoom']
        # self.lightIntensityOn = [255, 105, 0, 255, 255]
        # self.lightIntensityOff = [0, 0, 0, 0, 255]

        self.lightColours = ['Red']
        self.lightIntensityOn = [255]
        self.lightIntensityOff = [0]

        self.parLed = {}

        startingChannel = 1
        spacing = 0

        for light in range(1, self.numberOfLights +1):
            self.parLed[light] = {}
            for colour in self.lightColours:
                self.parLed[light][colour] = startingChannel
                startingChannel += 1
            startingChannel += spacing

    def getLampChannels(self, lamps):
        """takes list of lamp numbers and returns the DMX channels in order received"""
        returnList = []
        for lamp in lamps:
            for colour in self.lightColours:
                returnList.append(self.parLed[lamp][colour])
        return returnList

    def getIntensity(self, lampValues):
        """produce the values needed for each lamp"""
        returnList = []
        for value in lampValues:
            for propN, prop in enumerate(self.lightIntensityOn):
                #returnList.append(prop)
                returnList.append(utils.map(value, 0, 255, self.lightIntensityOff[propN], prop))
        return returnList

if __name__ == '__main__':
    parLed = parLed()
    print parLed.getLampChannels([1, 2, 3, 4])
    print parLed.getIntensity([100])
