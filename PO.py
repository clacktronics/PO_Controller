from Tkinter import *
from math import sin, cos, pi
from ENT_Control import EntTec
from Arduino_read import Arduino
from IRCAM import IRCAM
import threading
from time import sleep
import os, sys, utils

#========================================================================
# GLOBAL VARS
#========================================================================

# Works out a DMX map for all the lights (starts at 0)
channelColours = ['Red','Green','Blue','White','Zoom', 'bob']
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

#========================================================================
# GUI CLASSES
#========================================================================

#========================================================================
# CONTROL CLASSES
#========================================================================


class ThreadedMapper(threading.Thread):

	def __init__(self,input_device,output_device):
		self.input_device = input_device
		self.output_device = output_device
		self.playThread = False

		self.thread = threading.Thread(target=self.action)
		self.thread.setDaemon(True)
		self.thread.start()

	def action(self):
		while True:
			if self.playThread:
				if self.input_device == "Arduino":
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


				elif self.input_device == "IRCAM":
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
		self.playThread = True

	def stop(self):
		self.playThread = False

#========================================================================
# MAIN PROGRAM
#========================================================================

if __name__ == "__main__":
	try:
		EntTec = EntTec('/dev/' + EnttecPort,defaultMap)
		print "yes", EntTec
	except:

		EntTec = None

	try:
		Arduino = Arduino('/dev/' + ArduinoPort,250000)
	except:
		print "no", Arduino
		Arduino = None

	try:
		IRCAM = IRCAM(IrcamIP,IrcamPort)
	except:
		print "no", IRCAM
		IRCAM = None

	# Initiate threads for running translating from one deivce to another
	HaroonThread = ThreadedMapper(Arduino,EntTec)
	IrcamThread = ThreadedMapper(IRCAM,EntTec)

	# Make GUI
	master = Tk()
	styleKwargs = {'background':'#E8E9E8','highlightbackground':'#E8E9E8'}

	master.configure(**styleKwargs)
	master.minsize(width=1000,height=600)
	master.title('Paris Opera - Haroon Mirza')

	OperaPins = range(1,64,8)

	# master.bind("<Button-1>", lightCan.lampSelect)

	# Control buttons

	ControlButtonFrame = Frame(padx=10)
	ControlButtonFrame.grid(row=0,column=0)
	#
	buttonDims = {'width':20}
	buttonDims.update(styleKwargs)
	#
	Label(ControlButtonFrame, text="Cue", width=3, **styleKwargs).grid(row=0,column=0)
	Label(ControlButtonFrame, text="255", width=3, **styleKwargs).grid(row=0,column=1)

	Label(ControlButtonFrame, text="Haroon", **styleKwargs).grid(row=1, columnspan=2, column=0)

	StartArduino = Button(ControlButtonFrame, text="Start Arduino",command=HaroonThread.start, **buttonDims)
	StartArduino.grid(row=2, columnspan=2, column=0)

	KillArduino = Button(ControlButtonFrame, text="Kill Arduino",command=HaroonThread.stop, **buttonDims)
	KillArduino.grid(row=3, columnspan=2, column=0)

	Label(ControlButtonFrame, text="Boulez", **styleKwargs).grid(row=4, columnspan=2, column=0)

	StartIrcam = Button(ControlButtonFrame, text="Start IRCAM",command=IrcamThread.start, **buttonDims)
	StartIrcam.grid(row=5, columnspan=2, column=0)
	KillIrcam = Button(ControlButtonFrame, text="Kill IRCAM",command=IrcamThread.stop, **buttonDims)
	KillIrcam.grid(row=6, columnspan=2, column=0)

	Label(ControlButtonFrame, text="Test Patterns", **styleKwargs).grid(row=7, columnspan=2, column=0)

	Acending = Button(ControlButtonFrame, text="Start Acending",command=IrcamThread.start, **buttonDims)
	Acending.grid(row=8, columnspan=2, column=0)
	KillAcending = Button(ControlButtonFrame, text="Kill Acending",command=IrcamThread.stop, **buttonDims)
	KillAcending.grid(row=9, columnspan=2, column=0)

	allon = Button(ControlButtonFrame, text="All on",command=IrcamThread.start, **buttonDims)
	allon.grid(row=10, columnspan=2, column=0)
	alloff = Button(ControlButtonFrame, text="All off",command=IrcamThread.stop, **buttonDims)
	alloff.grid(row=11, columnspan=2, column=0)

	master.mainloop()
