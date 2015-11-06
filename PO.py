from Tkinter import *
#from ttk import *
from math import sin, cos, pi
from ENT_Control import EntTec
from Arduino_read import Arduino
from IRCAM import IRCAM
import threading
from time import sleep
import os, sys, utils

#===============================================================================
# GLOBAL VARS
#===============================================================================

# Works out a DMX map for all the lights (starts at 0)
channelColours = ['Red','Green','Blue','White','Zoom']
DMXValues = [255,255,255,255,255,255]
numberColours = len(channelColours)

channels = {} # global for the dmx channel boxes, it is filled when DMXaddresUtil is called
defaultMap = {} # global for the default mapping for said channels


# mapping arduino pins to roof (needed???)
arduinoMap = []
for arduino in range(64):
	if arduino % 8:
		arduinoMap.append(0)
	else:
		arduinoMap.append(1)



#===============================================================================
# GUI CLASSES
#===============================================================================

class controlFrame(Frame):
	def __init__(self, parent):
		self.parent = parent
	def initUI(self):
		buttonDims = {'width':20}
		buttonDims.update(styleKwargs)

		self.ctrlFrame = Frame()
		self.ctrlFrame.grid(row=0,column=0)
		self.drawConnect()

		Label(self.ctrlFrame, text="Cue", width=3, **styleKwargs).grid(row=0,column=0)
		Label(self.ctrlFrame, text="255", width=3, **styleKwargs).grid(row=0,column=1)

		Label(self.ctrlFrame, text="Haroon", **styleKwargs).grid(row=1, columnspan=2, column=0)

		StartArduino = Button(self.ctrlFrame, text="Start Arduino",command=HaroonThread.start, **buttonDims)
		StartArduino.grid(row=2, columnspan=2, column=0)

		KillArduino = Button(self.ctrlFrame, text="Kill Arduino",command=HaroonThread.stop, **buttonDims)
		KillArduino.grid(row=3, columnspan=2, column=0)

		Label(self.ctrlFrame, text="Boulez", **styleKwargs).grid(row=4, columnspan=2, column=0)

		StartIrcam = Button(self.ctrlFrame, text="Start IRCAM",command=IrcamThread.start, **buttonDims)
		StartIrcam.grid(row=5, columnspan=2, column=0)
		KillIrcam = Button(self.ctrlFrame, text="Kill IRCAM",command=IrcamThread.stop, **buttonDims)
		KillIrcam.grid(row=6, columnspan=2, column=0)

		Label(self.ctrlFrame, text="Test Patterns", **styleKwargs).grid(row=7, columnspan=2, column=0)

		Acending = Button(self.ctrlFrame, text="Start Acending",command=IrcamThread.start, **buttonDims)
		Acending.grid(row=8, columnspan=2, column=0)
		KillAcending = Button(self.ctrlFrame, text="Kill Acending",command=IrcamThread.stop, **buttonDims)
		KillAcending.grid(row=9, columnspan=2, column=0)

		allon = Button(self.ctrlFrame, text="All on",command=IrcamThread.start, **buttonDims)
		allon.grid(row=10, columnspan=2, column=0)
		alloff = Button(self.ctrlFrame, text="All off",command=IrcamThread.stop, **buttonDims)
		alloff.grid(row=11, columnspan=2, column=0)


	def drawConnect(self):
		self.arduinoSelect = StringVar(self.ctrlFrame)
		self.arduinoSelect.set(ArduinoPort)
		PortSelectOut = OptionMenu(self.ctrlFrame, self.arduinoSelect,*ports)
		PortSelectOut.grid(row=14, columnspan=2, column=0)
		Label(self.ctrlFrame, text="Status: %s" % Arduino.isConnectedString() , **styleKwargs).grid(row=15, columnspan=2, column=0)

		self.EntSelect = StringVar(self.ctrlFrame)
		self.EntSelect.set('tty.usbserial-EN172718')
		PortSelectOut = OptionMenu(self.ctrlFrame, self.EntSelect,*ports)
		PortSelectOut.grid(row=16, columnspan=2, column=0)
		Label(self.ctrlFrame, text="Status: %s" % EntTec.isConnectedString() , **styleKwargs).grid(row=17, columnspan=2, column=0)

		connectButton = Button(self.ctrlFrame, text="Reload Connections", command=connectDevices)
		connectButton.grid(row=30, columnspan=2, column=0)

	def getEntPort(self):
		return self.EntSelect.get()

	def getArdPort(self):
		return self.arduinoSelect.get()

	def drawControl(self):
		pass


#===============================================================================
# CONTROL CLASSES
#===============================================================================

class ThreadedMapper(threading.Thread):

	def __init__(self,input_device,output_device):
		self.input_device = input_device
		self.output_device = output_device
		self.playThread = False
		self.mode = self.input_device.__str__()

		self.thread = threading.Thread(target=self.action)
		self.thread.setDaemon(True)
		self.thread.start()

	def action(self):
		print self.input_device
		while True:
			if self.playThread:
				if self.mode == 'Arduino':
					print "Playing Arduino"
					self.input_device.cue()
					while True:
						output = self.input_device.readSequence()
						self.output_device.senddmx(OperaPins,output)
						if not self.playThread:
							print "Stopping Arduino"
							self.input_device.stop()
							self.output_device.all(0)
							break

				elif self.mode == "IRCAM":
					print "Listening to IRCAM"
					while True:
						message = self.input_device.getMessage()
						message = self.rangeMapper(message, 0, 360, 0, 63)
						print message
						messages = [0] * 64
						messages[message] = 3
						self.output_device.senddmx(range(1,65),messages)
						if not self.playThread:
							print "Stopping IRCAM"
							self.output_device.all(0)
							break
			sleep(0.1)

	def rangeMapper(self,x, in_min, in_max, out_min, out_max):
		return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

	def start(self):
		print 'start!'
		self.playThread = True

	def stop(self):
		self.playThread = False

#===============================================================================
# MAIN PROGRAM
#===============================================================================

if __name__ == "__main__":

	# Get ports (exclude bluetooth ports)
	ports = [port for port in os.listdir('/dev/') if port[:4] == 'tty.' and port[:8] != 'tty.Blue' ]

	ArduinoPort = ''
	for port in ports:
		if port[:12] == 'tty.usbmodem':
			ArduinoPort = port



	# Setup master frame
	styleKwargs = {'background':'#E8E9E8','highlightbackground':'#E8E9E8'}
	master = Tk()
	master.configure(**styleKwargs)
	master.minsize(width=1000,height=600)
	master.title('Paris Opera - Haroon Mirza')

	def connectDevices():
		#HaroonThread.__init__(Arduino,EntTec)
		#IrcamThread.__init__(IRCAM,EntTec)
		try: Arduino.disconnect()
		except: pass
		Arduino.connect('/dev/%s' % app.getArdPort(), 250000)

		try: EntTec.disconnect()
		except: pass
		EntTec.connect('/dev/%s' % app.getEntPort()) #'/dev/tty.usbserial-EN172718'

		IRCAM.connect('localhost',7007)
		app.drawConnect()

	# Setup classes for
	EntTec = EntTec()
	Arduino = Arduino()
	IRCAM = IRCAM()

	# Initiate threads for running translating from one deivce to another
	HaroonThread = ThreadedMapper(Arduino,EntTec)
	IrcamThread = ThreadedMapper(IRCAM,EntTec)

	# Setup GUI class
	app = controlFrame(master)
	app.initUI()
	connectDevices()




	OperaPins = range(1,64,8)

	# master.bind("<Button-1>", lightCan.lampSelect)

	# Control buttons


	#


	master.mainloop()
