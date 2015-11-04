import serial
from device import device

class Arduino(device):
	''' Class for controlling the Arduino and streaming data from it'''
	def __init__(self,port,baud):

		self.connected = False
		self.port = port
		self.baud = baud
		self.connect()


	def __str__(self):
			return "Arduino"

	def connect(self):
		try:
			self.Arduino = serial.Serial(self.port, self.baud)
			self.connected = True
			print 'Yes Arduino'
			return True
		except:
			self.connected = False
			print 'No Arduino'
			return False

	def cue(self):
		if self.isConnected():
			self.Arduino.write('x')
			while True:
				if self.Arduino.readline().strip() == "'s' to start and 'x' to reset":
					self.Arduino.write('s')
					return True
		else:
			return 'Method cue does not work as Arduino is not connected'

	def stop(self):
		self.Arduino.write('x')

	def readSequence(self):

		while True:
			if self.connected:
				output = self.Arduino.readline()
				try:
					int(output[0])
					return output[:8]
				except:
					pass
			else:
				print "Attempt to send, no device connected"


if __name__ == '__main__':
	Arduino = Arduino('/dev/tty.usbmodemfa141',250000)
	Arduino.cue()
	if Arduino.isConnected():
		while True:
			print Arduino.readSequence()
