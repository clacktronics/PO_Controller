# Python libraries
from Tkinter import *
from time import sleep

import os, sys, utils, threading

# My modules
from ENT_Control import EntTec
from Arduino_read import Arduino
from Processing_Control import processing
from IRCAM import IRCAM
from test_gen import testCircle, testAll, fadeAll

from utils import map, clamp

#===============================================================================
# GUI CLASSES
#===============================================================================

class controlFrame(Frame):
	"""Main window for the control of the program"""
	def __init__(self, parent):
		self.parent = parent

	def initUI(self):
		"""Renders the GUI"""
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

		Acending = Button(self.ctrlFrame, text="Start Acending",command=CircleThread.start, **buttonDims)
		Acending.grid(row=8, columnspan=2, column=0)
		KillAcending = Button(self.ctrlFrame, text="Kill Acending",command=CircleThread.stop, **buttonDims)
		KillAcending.grid(row=9, columnspan=2, column=0)

		allon = Button(self.ctrlFrame, text="All on",command=AllThread.start, **buttonDims)
		allon.grid(row=10, columnspan=2, column=0)
		alloff = Button(self.ctrlFrame, text="All off",command=AllThread.stop, **buttonDims)
		alloff.grid(row=11, columnspan=2, column=0)

		fadeon = Button(self.ctrlFrame, text="Fade on",command=FadeThread.start, **buttonDims)
		fadeon.grid(row=12, columnspan=2, column=0)
		fadeoff = Button(self.ctrlFrame, text="Fade off",command=FadeThread.stop, **buttonDims)
		fadeoff.grid(row=13, columnspan=2, column=0)


	def drawConnect(self):
		"""Connection status render"""
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
		"""Runs a loop within a thread, different action depending on input_device"""
		print '%s thread initiated /n' % self.input_device
		while True:

			if self.playThread:

			# Arduino Mode
				if self.mode == 'Arduino':
					print "Start Arduino"
					self.input_device.cue() # Send a start command to the Arduino over serial
					ArduinoLights = [59, 51, 43, 35, 25, 17, 9, 1] # Mapping of the 8 arduono lights
					#ArduinoLights = [1, 2, 3, 4, 5, 6, 7, 8]
					#ArduinoLights.reverse()
					# This loop waits for each step from the arduino then it passes the values to the DMX device
					# It only ends when the user presses the button to set playThread False
					while True:
						ArduinoStep = [] # New empty list for the DMX send
						output = self.input_device.readSequence() # this blocks until it can return a value
						# string to list > this could be done more efficiently using list()?
						for i in output:
							ArduinoStep.append(self.rangeMapper(int(i), 0, 3, 0, 255))

						# Send list to DMX output
						self.output_device.sendLights(ArduinoLights,ArduinoStep)

						# Terminate when button sets playThread False, closes port
						if not self.playThread:
							print "Stopping Arduino"
							self.input_device.stop()
							self.output_device.all(0)
							break

			# IRCAM Mode
				elif self.mode == "IRCAM":
					print "Listening to IRCAM"
					messages = [0] * 64
					while True:
						message = self.input_device.getMessage()
						if message != None:
							print message
							message = map(message, 0, 360, 0, 64)
							message = clamp(message, 0, 64)
							messages[message] = 255

							for cN,channel in enumerate(messages):
								if channel != 0:
									messages[cN] -= 85

							self.output_device.sendLights(range(1,65),messages)
							if not self.playThread:
								print "Stopping IRCAM"
								self.output_device.all(0)
								break

			# testCircle Mode
				elif self.mode == "testCircle":
					while True:
						output = self.input_device.circle()
						self.output_device.sendLights(range(1,65),output)

						if not self.playThread:
							print "Stopping Circle test"
							self.input_device.reset()
							self.output_device.all(0)
							break

			# testAll Mode
				elif self.mode == "testAll":
					while True:
						if self.playThread:
							output = self.input_device.all(True)
							self.output_device.sendLights(range(1,65), output)
						elif not self.playThread:
							print 'stop'
							output = self.input_device.all(False)
							self.output_device.sendLights(range(1,65), output)
							break

			# fadeAll Mode
				elif self.mode == "fadeAll":
							while True:
								output = self.input_device.fade()
								self.output_device.sendLights(range(1,65),output)

								if not self.playThread:
									print "Stopping fade test"
									self.input_device.reset()
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

	# Setup classes for the things the program controls
	EntTec = EntTec()
	Arduino = Arduino()
	IRCAM = IRCAM()
	Oscilliscope =  processing()
	testCircle = testCircle()
	testAll = testAll()
	fadeAll = fadeAll()

	# Initiate threads for running translating from one deivce to another
	HaroonThread = ThreadedMapper(Arduino,EntTec)
	IrcamThread = ThreadedMapper(IRCAM,EntTec)
	CircleThread = ThreadedMapper(testCircle,EntTec)
	AllThread = ThreadedMapper(testAll,EntTec)
	FadeThread = ThreadedMapper(fadeAll,EntTec)

	# Setup GUI class
	app = controlFrame(master)
	app.initUI()
	connectDevices()




	OperaPins = range(1,64,8)

	# master.bind("<Button-1>", lightCan.lampSelect)

	# Control buttons


	#


	master.mainloop()
