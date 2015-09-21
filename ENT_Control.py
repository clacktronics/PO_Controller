
import serial
from Arduino_read import Arduino
import sys

class EntTec:

	def __init__(self,port):
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
		self.EntTec=serial.Serial(port) # '/dev/tty.usbserial-EN172718'

		#this writes the initialization codes to the DMX
		self.EntTec.write( self.DMXOPEN+self.DMXINIT1+self.DMXCLOSE)
		self.EntTec.write( self.DMXOPEN+self.DMXINIT2+self.DMXCLOSE)

		# this sets up an array of 513 bytes, the first item in the array ( dmxdata[0] ) is the previously
		#mentioned spacer byte following the header. This makes the array math more obvious
		self.dmxDataList=[chr(0)]*513

		#senddmx accepts the 513 byte long data string to keep the state of all the channels
		# the channel number and the value for that channel
		#senddmx writes to the serial port then returns the modified 513 byte array
 
	def senddmx(self, chans, intensity):
	        # because the spacer bit is [0], the channel number is the array item number
	        # set the channel number to the proper value
	        for chanN,chan in enumerate(chans):
	        	outputDMX = int(intensity[chanN]) * 85
	       		self.dmxDataList[chan]=chr(outputDMX)
	        # join turns the array data into a string we can send down the DMX
	        sdata=''.join(self.dmxDataList)
	        # write the data to the serial port, this sends the data to your fixture
	        self.EntTec.write(self.DMXOPEN+self.DMXINTENSITY+sdata+self.DMXCLOSE)
	        # return the data with the new value in place

	def all(self,n):
		self.senddmx(range(1,65),[n]*64)



if __name__ == "__main__":
	OperaPins = range(1,64,8)
	print OperaPins
	EntTec = EntTec('/dev/tty.usbserial-EN172718')
	Arduino = Arduino('/dev/tty.usbmodemfd131',250000)
	Arduino.cue()
	while True:
		output = Arduino.readSequence()
		EntTec.senddmx(OperaPins,output)

