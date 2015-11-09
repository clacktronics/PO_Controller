import serial
from Arduino_read import Arduino
from IRCAM import IRCAM
import sys
from time import sleep
from device import device
from mapping_generator import parLed



class EntTec(parLed, device):

	def __init__(self):
		parLed.__init__(self)
		#char 126 is 7E in hex. It's used to start all DMX512 commands
		self.DMXOPEN=chr(126)
		#char 231 is E7 in hex. It's used to close all DMX512 commands
		self.DMXCLOSE=chr(231)

		#I named the "output only send dmx packet request" DMXINTENSITY as I don't have
		#any moving fixtures. Char 6 is the label , I don't know what Char 1 and Char 2 mean
		#but my sniffer log showed those values always to be the same so I guess it's good enough.
		self.DMXINTENSITY=chr(6)+chr(1)+chr(2)

		#this code seems to initialize the communications. Char 3 is a request for the controller's
		#parameters. I didn't bother reading that data, I'm just assuming it's an init string.
		self.DMXINIT1= chr(03)+chr(02)+chr(0)+chr(0)+chr(0)

		#likewise, char 10 requests the serial number of the unit. I'm not receiving it or using it
		#but the other softwares I tested did. You might want to.
		self.DMXINIT2= chr(10)+chr(02)+chr(0)+chr(0)+chr(0)

		#open serial port 4. This is where the USB virtual port hangs on my machine. You
		#might need to change this number. Find out what com port your DMX controller is on
		#and subtract 1, the ports are numbered 0-3 instead of 1-4
		self.connected = False

		self.dmxDataList=[chr(0)]*513 # this sets up an array of 513 bytes, the first item in the array ( dmxdata[0] ) is the previously mentioned spacer byte following the header. This makes the array math more obvious
		self.DMXValues = {'Red':255,'Green':254,'Blue':253,'White':252}

		#senddmx accepts the 513 byte long data string to keep the state of all the channels
		# the channel number and the value for that channel
		#senddmx writes to the serial port then returns the modified 513 byte array

	def connect(self, port):
		try:
			self.SerialDevice=serial.Serial(port) # '/dev/tty.usbserial-EN172718'
			#this writes the initialization codes to the DMX
			self.SerialDevice.write( self.DMXOPEN+self.DMXINIT1+self.DMXCLOSE)
			self.SerialDevice.write( self.DMXOPEN+self.DMXINIT2+self.DMXCLOSE)
			self.connected = True
			print "Yes Ent"
			return True
		except:
			self.connected = False
			print "No Ent"
			return False

	def disconnect(self):
		try:
			self.SerialDevice.close()
		except:
			pass

	def senddmx(self, chans, intensity):
		for chanN,chan in enumerate(chans):
			self.dmxDataList[chan]=chr(intensity[chanN])
			sdata=''.join(self.dmxDataList)
		if self.isConnected():
		    self.SerialDevice.write(self.DMXOPEN+self.DMXINTENSITY+sdata+self.DMXCLOSE)
		else:
			pass
				#print "Attempt to send, no device connected"

	def sendLights(self, lightsList, intensityList):
		#print self.getLampChannels(lightsList),self.getIntensity(intensityList)
		self.senddmx(self.getLampChannels(lightsList),self.getIntensity(intensityList))


	def all(self,n):
		self.senddmx(range(1,65),[n]*64)
		# Theeseeese are the LEDs for 8
		#51,35,17,1
	    #9,25,43,59

if __name__ == "__main__":
	from utils import map, clamp
	messages = [0] * 64
	mode = sys.argv[1]
	channelColours = ['Red','Green','Blue','White']
	numberColours = len(channelColours)
	defaultMap = {}
	for channelN,channel in enumerate(channelColours):
		defaultMap[channel] = range(channelN,64*numberColours,numberColours)
	DMXValues = [255,255,255,255]

	EntTec = EntTec()
	EntTec.connect('/dev/tty.usbserial-EN172718')


	if mode == "mirza":
		Arduino = Arduino()
		Arduino.connect('/dev/tty.usbmodemfa141',250000)
		pins = [59, 51, 43, 35, 25, 17, 9, 1]
		pins.reverse()
		print Arduino.cue()
		while True:
			sender = []
			output =  Arduino.readSequence()
			print output
			for i in output:
				sender.append(int(i) * 83)
			EntTec.sendLights(pins,sender)
	elif mode == "boulez":
		IRCAM = IRCAM()
		IRCAM.connect('0.0.0.0',7007)
		while True:
			message = IRCAM.getMessage()
			if message != None:
				print "in" + str(message)
				message = map(message, 0, 90, 0, 63)
				#messages = [0] * 64
				for cN,channel in enumerate(messages):
					if channel != 0:
						messages[cN] -= 2
				message = clamp(message, 0, 63)
				messages[message] = 20
				#EntTec.senddmx(range(1,65),messages)
				EntTec.senddmx(range(1,65),messages)
	elif mode == "test":
		while True:
			# EntTec.senddmx([6,7,8,9,10,11,12,13,14,15], [255,255,255,255,255,255,255,255,255,255])
			# sleep(1)
			# EntTec.senddmx([6,7,8,9,10,11,12,13,14,15], [0,255,0,255,0,255,0,255,0,255])
			# sleep(1)
			EntTec.sendLights([2,3], [255,255])
			sleep(.01)
			EntTec.sendLights([2,3], [0,0])
			sleep(.01)

	elif mode == "test2":
		while True:
			EntTec.all(255)
			sleep(.1)
			EntTec.all(0)
			sleep(.1)



	# print EntTec.RGBcans([1,4,8]):
	# 	 EntTec.senddmx(range(1,9),[250]*8)
	# 	 sleep(1)
	# 	 EntTec.senddmx(range(1,9),[0]*8)
	# 	 sleep(1)
