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
# GLOBAL VARS
#===============================================================================

all64Lights = range(1,65)

#===============================================================================
# GUI CLASSES
#===============================================================================

class controlFrame(Frame):
	"""Main window for the control of the program"""
	def __init__(self, parent):
		self.parent = parent

	def initUI(self):
		"""Renders the GUI"""
		self.buttonDims = {'width':20}
		self.buttonDims.update(styleKwargs)
		self.cueNumber = IntVar()
		self.cueNumber.set('0')

		self.ctrlFrame = Frame(**styleKwargs)
		spacerFrame = Frame()
		spacerFrame.grid(row=0, column=1, padx=100)
		self.testFrame = Frame(**styleKwargs)
		self.cnctFrame = Frame(**styleKwargs)


		self.drawControl()
		self.drawTest()
		self.drawConnect()

	def drawControl(self, arduino='#E8E9E8', ircam='#E8E9E8'):
		"Draw the control settings"

		#self.drawCue()

		Label(self.ctrlFrame, text="Haroon", **styleKwargs).grid(row=1, columnspan=2, column=0)

		StartArduino = Button(self.ctrlFrame, text="Start Arduino",command=startHaroon, width=20, highlightbackground=arduino)
		StartArduino.grid(row=2, columnspan=2, column=0)

		KillArduino = Button(self.ctrlFrame, text="Stop Arduino",command=stopHaroon, **self.buttonDims)
		KillArduino.grid(row=3, columnspan=2, column=0)

		Label(self.ctrlFrame, text="Boulez", **styleKwargs).grid(row=4, columnspan=2, column=0)

		StartIrcam = Button(self.ctrlFrame, text="Start IRCAM",command=startIrcam, width=20, highlightbackground=ircam)
		StartIrcam.grid(row=5, columnspan=2, column=0)
		Label(self.ctrlFrame, text="Make Network settings", **styleKwargs).grid(row=6, columnspan=2, column=0)
		Label(self.ctrlFrame, text="IP Address 192.168.1.2", **styleKwargs).grid(row=7, columnspan=2, column=0)
		Label(self.ctrlFrame, text="Will listen at port 7000", **styleKwargs).grid(row=8, columnspan=2, column=0)
		Label(self.ctrlFrame, text=" ", **styleKwargs).grid(row=9, columnspan=2, column=0)
		Label(self.ctrlFrame, text="Close and re-open program to restart IRCAM", **styleKwargs).grid(row=10, columnspan=2, column=0)
		#KillIrcam = Button(self.ctrlFrame, text="Stop IRCAM",command=stopIrcam, **self.buttonDims)
		#KillIrcam.grid(row=6, columnspan=2, column=0)

		self.ctrlFrame.grid(row=0,column=0, padx=50)

	def drawCue(self):
		"Draw the cue settings"

		Label(self.ctrlFrame, text="Cue", width=3, **styleKwargs).grid(row=0,column=0)
		Label(self.ctrlFrame, textvariable=self.cueNumber, width=3, **styleKwargs).grid(row=0,column=1)

	def drawTest(self):
		"Draw the test settings"

		Label(self.testFrame, text="Test Patterns", **styleKwargs).grid(row=7, columnspan=2, column=0)

		Acending = Button(self.testFrame, text="Start Acending",command=CircleThread.start, **self.buttonDims)
		Acending.grid(row=8, columnspan=2, column=0)
		KillAcending = Button(self.testFrame, text="Stop Acending",command=CircleThread.stop, **self.buttonDims)
		KillAcending.grid(row=9, columnspan=2, column=0)

		allon = Button(self.testFrame, text="All on",command=AllThread.start, **self.buttonDims)
		allon.grid(row=10, columnspan=2, column=0)
		alloff = Button(self.testFrame, text="All off",command=AllThread.stop, **self.buttonDims)
		alloff.grid(row=11, columnspan=2, column=0)

		fadeon = Button(self.testFrame, text="Fade on",command=FadeThread.start, **self.buttonDims)
		fadeon.grid(row=12, columnspan=2, column=0)
		fadeoff = Button(self.testFrame, text="Fade off",command=FadeThread.stop, **self.buttonDims)
		fadeoff.grid(row=13, columnspan=2, column=0)

		self.testFrame.grid(row=0,column=2, padx=50)


	def drawConnect(self):
		"Draw the connect settings"

		# Get ports (exclude bluetooth ports)
		ports = [port for port in os.listdir('/dev/') if port[:4] == 'tty.' and port[:8] != 'tty.Blue' ]

		ArduinoPort = ''
		for port in ports:
			if port[:12] == 'tty.usbmodem':
				ArduinoPort = port

		"""Connection status render"""
		self.arduinoSelect = StringVar(self.cnctFrame)
		self.arduinoSelect.set(ArduinoPort)
		PortSelectOut = OptionMenu(self.cnctFrame, self.arduinoSelect,*ports)
		PortSelectOut.grid(row=14, columnspan=2, column=0)
		Label(self.cnctFrame, text="Status: %s" % Arduino.isConnectedString() , **styleKwargs).grid(row=15, columnspan=2, column=0)

		self.EntSelect = StringVar(self.cnctFrame)
		self.EntSelect.set('tty.usbserial-EN172718')
		PortSelectOut = OptionMenu(self.cnctFrame, self.EntSelect,*ports)
		PortSelectOut.grid(row=16, columnspan=2, column=0)
		Label(self.cnctFrame, text="Status: %s" % EntTec.isConnectedString() , **styleKwargs).grid(row=17, columnspan=2, column=0)

		#Label(self.cnctFrame, text="IP", **styleKwargs).grid(row=18, columnspan=1, column=0)
		#IPadd = Entry(self.cnctFrame, width=5, **styleKwargs).grid(row=19, columnspan=2, column=0)
		#Label(self.cnctFrame, text="Port", **styleKwargs).grid(row=20, columnspan=1, column=0)
		#portadd = Entry(self.cnctFrame, width=4, **styleKwargs).grid(row=21, columnspan=2, column=0)


		connectButton = Button(self.cnctFrame, text="Reload Connections", command=connectDevices, **styleKwargs)
		connectButton.grid(row=30, columnspan=2, column=0)

		self.cnctFrame.grid(row=1,column=2, padx=50)


	def getEntPort(self):
		return self.EntSelect.get()

	def getArdPort(self):
		return self.arduinoSelect.get()


#===============================================================================
# CONTROL CLASSES
#===============================================================================

def startHaroon():
	IrcamThread.stop()
	app.drawControl(arduino='#F00')
	HaroonThread.start()

def stopHaroon():
	app.drawControl()
	HaroonThread.stop()

def startIrcam():
	HaroonThread.stop()
	IRCAM.disconnect()
	IRCAM.connect('0.0.0.0',7000)
	app.drawControl(ircam='#F00')
	IrcamThread.start()

def stopIrcam():
	IrcamThread.stop()
	app.drawControl()




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
		sys.stdout.write("%s thread initiated\n" % self.input_device)
		while True:

			if self.playThread:

			# Arduino Mode
				if self.mode == 'Arduino':
					#print "Start Arduino"
					ArduinoLights = [57, 49, 41, 33, 25, 17, 9, 1] # Mapping of the 8 arduono lights
					#ArduinoLights = [1, 2, 3, 4, 5, 6, 7, 8]
					ArduinoLights.reverse()
					step = 0
					self.input_device.cue() # Send a start command to the Arduino over serial

					# This loop waits for each step from the arduino then it passes the values to the DMX device
					# It only ends when the user presses the button to set playThread False
					while True:
						if self.input_device.isConnected() == False:
							print "Arduino Not connected"
							self.playThread = False
						else:
							ArduinoStep = [] # New empty list for the DMX send
							output = self.input_device.readSequence() # this blocks until it can return a value
							step += 1
							#app.cueNumber.set(step)
							# string to list > this could be done more efficiently using list()?
							for i in output:
								ArduinoStep.append(self.rangeMapper(int(i), 0, 3, 0, 255))
							# Send list to DMX output
							if step >= 0: # <=466
								self.output_device.sendLights(ArduinoLights,ArduinoStep)
							elif step == 465:
								self.output_device.all(0)
							else:
								self.output_device.all(255)
							# Stop playing if end of sequence
							if step >= 2131:
								self.playThread = False

						# Terminate when button sets playThread False, closes port
						if not self.playThread:
							# print "Stopping Arduino"
							self.input_device.stop()
							self.output_device.all(0)
							#app.cueNumber.set('0')
							break

			# IRCAM Mode
				elif self.mode == "IRCAM":
					self.cue = 0
					print "Listening for IRCAM"
					messages = [0] * 65
					lastMessages = []
					lastspat = None
					lastpitch = None
					self.output_device.sendLights(all64Lights,messages)
					while True:

						message = self.input_device.getMessage()

						print message

						if message.get('cue', None) != None:
							#app.cueNumber.set(message['cue'])
							self.cue = message['cue']

						elif self.cue >= 22 and self.cue <= 31:
							fade = 51
							if message.get('spat', None) != None:

								message = message['spat']
								message = map(message, 0, 360, 0, 64)
								message = clamp(message, 1, 64)
								messages[message] = 255

						elif self.cue >= 209:
							fade = 15
							if message.get('pitch', None) != None:

								message = message['pitch']
								message = clamp(message, 50, 100)
								message = map(message, 50, 100, 4, 64)
								#message = clamp(message, 1, 64)
								messages[message] = 255
								#print "pitch %d " % message

						else:
							self.output_device.all(0)


						for cN,channel in enumerate(messages):
							if channel != 0:
								messages[cN] -= fade

						if messages != lastMessages:
							lastMessages = messages[:]
							self.output_device.sendLights(all64Lights,messages)

						if not self.playThread:
							print "Stopping IRCAM"
							self.output_device.all(0)
							# self.input_device.disconnect()
							#app.cueNumber.set('0')
							break

			# testCircle Mode
				elif self.mode == "testCircle":
					while True:
						output = self.input_device.circle()
						if output == 1:
							last_output = 64
						else:
							last_output = output - 1
						self.output_device.sendLights([last_output, output],[0, 255])
						#app.cueNumber.set(str(output))



						if not self.playThread:
							print "Stopping Circle test"
							#app.cueNumber.set('0')
							self.input_device.reset()
							self.output_device.all(0)

							break

			# testAll Mode
				elif self.mode == "testAll":
					while True:
						if self.playThread:
							self.output_device.sendLights(all64Lights, [255]*64)
						elif not self.playThread:
							print 'stop'
							self.output_device.sendLights(all64Lights, [0]*64)
							break
						sleep(0.1)

			# fadeAll Mode
				elif self.mode == "fadeAll":
							while True:
								output = self.input_device.fade()
								#app.cueNumber.set(str(output))
								self.output_device.sendLights(all64Lights,[output]*64)

								if not self.playThread:
									print "Stopping fade test"
									#app.cueNumber.set('0')
									self.input_device.reset()
									self.output_device.all(0)
									break

			sleep(0.1)

	def rangeMapper(self,x, in_min, in_max, out_min, out_max):
		return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

	def start(self):
		self.playThread = True

	def stop(self):
		self.playThread = False

#===============================================================================
# MAIN PROGRAM
#===============================================================================

if __name__ == "__main__":





	# Setup master frame
	styleKwargs = {'background':'#E8E9E8','highlightbackground':'#E8E9E8'}
	master = Tk()
	master.configure(**styleKwargs)
	master.minsize(width=500,height=400)
	master.title('Paris Opera - Haroon Mirza')

	def connectDevices():

		try: Arduino.disconnect()
		except: pass
		Arduino.connect('/dev/%s' % app.getArdPort(), 250000)

		try:
			EntTec.disconnect()
		except: pass
		EntTec.connect('/dev/%s' % app.getEntPort()) #'/dev/tty.usbserial-EN172718'

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
	master.mainloop()
