import serial

class Arduino:

	def __init__(self,port,baud):
		self.Arduino = serial.Serial(port, baud)
		self.type = 'Arduino'

	def cue(self):
		self.Arduino.write('x')
		while True:
			if self.Arduino.readline().strip() == "'s' to start and 'x' to reset":
				self.Arduino.write('s')
				return True

	def stop(self):
		self.Arduino.write('x')

	def readSequence(self):
		
		while True:
			output = self.Arduino.readline()
			try:
				int(output[0])
				return output[:9]
			except:
				pass




if __name__ == '__main__':
	Arduino = Arduino('/dev/tty.usbmodemfd131',250000)
	Arduino.cue()
	while True:
		print Arduino.readSequence()