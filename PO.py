from Tkinter import *
from math import sin, cos, pi
from ENT_Control import EntTec
from Arduino_read import Arduino
from IRCAM import IRCAM
import threading
from time import sleep
import os, sys

#========================================================================
# GLOBAL VARS
#========================================================================

channels = {}
arduinoMap = []
channelColours = ['Red','Green','Blue','White']
DMXValues = [255,255,255,255]
numberChannels = 16
numberColours = len(channelColours)
defaultMap = {}
for channelN,channel in enumerate(channelColours):
	defaultMap[channel] = range(channelN,64*numberColours,numberColours)
for arduino in range(64):
	if arduino % 8:
		arduinoMap.append(0)
	else:
		arduinoMap.append(1)

print defaultMap

#========================================================================
# GUI CLASSES
#========================================================================

class DMXaddressUtil():

	def __init__(self,master,channelColours):
		self.frame = master
		self.channelColours = channelColours
		self.numberColours = len(self.channelColours)
		
		self.render('00-15',1)
	# Channel Labels
	

	def render(self,addRange,highlight):
		addRanges = addRange.replace('-','')
		addLow = int(addRanges[:2])
		addHigh = int(addRanges[2:])+1
		relief = 'solid'
		highlightColor = '#E8E9E8'

		bgColours = {'Red':'#FFCCCC','Green':'#CCFFCC','Blue':'#66CCFF','White':'#FFFFEB'}

		#======OVERALL=DMX=MESSAGE=SETTINGS======================

		# DMX value label
		Label(self.frame, text='Value',bg='#E8E9E8').grid(row=0,column=1)
		# DMX intensity values for all channels
		for rowN,row in enumerate(channelColours):
			DMXValues[rowN] = Entry(self.frame,width=3,bg='#FFE0B2',bd=1,relief=relief,highlightbackground=highlightColor)
			DMXValues[rowN].grid(row=rowN+1,column=1)
			DMXValues[rowN].insert(END,255)

		#======OVERALL=DMX=MESSAGE=SETTINGS======================

		# light channel labeling
		for lN,channel in enumerate(range(addLow,addHigh)):
			Label(self.frame, text=channel,bg='#E8E9E8').grid(row=0,column=lN+2)

		# address values for all DMX channels
		for rowN,row in enumerate(channelColours):
			channels[row] = {}
			Label(self.frame, text=row,bg='#E8E9E8').grid(row=rowN+1,column=0)
			for cN,channel in enumerate(range(addLow,addHigh)):
				if channel != highlight:
					highlightColor = '#E8E9E8'
				else:
					highlightColor = 'red'
				channels[row][channel] = Entry(self.frame,width=4,bg=bgColours[row],bd=1,relief=relief,highlightbackground=highlightColor)
				channels[row][channel].insert(END,defaultMap[row][channel])
				channels[row][channel].grid(row=rowN+1,column=cN+2)

		# Option Buttons

		OPTIONS = ['00-15','16-31','32-47','48-63']
		variable = StringVar(self.frame)
		variable.set(addRange)

		sel = OptionMenu(self.frame, variable,*OPTIONS,command=self.render)
		sel.config(width=10,bg='#FFE0B2')
		
		


		sel.grid(row=self.numberColours+2,column=1,columnspan=2)



	def applyUpdate(self):
		print "apply" 

class lightCanvas:

	def __init__(self,canvas):
		self.canvas = canvas
		self.lightpositions = {}

	def render(self,*kwargs):
		lights = 64
		lightSize = 0
		smallerLight = 8
		biggerLight = 4
		increment = (pi*2) / lights
		xoffset = 300
		yoffset = 250

		for light in range(lights ):
			self.lightpositions[light] = {}
			angle = light * increment 
			
			self.lightpositions[light]['x'] = xpos = round(xoffset + sin(angle) * 200,2)
			self.lightpositions[light]['y'] = ypos = round(yoffset + cos(angle) * 200,2)

			if light % 16 == 0:
				lightSize = smallerLight + biggerLight
				xpos -= biggerLight / 2
				ypos -= biggerLight / 2
			else:
				lightSize = smallerLight

			self.canvas.create_oval(xpos,ypos,xpos+lightSize,ypos+lightSize,fill='black',activefill='red')
		self.canvas.grid(row=0,column=1)

	def lampSelect(self,event):
		# using the map created at render, works out the lamp that is clicked
		for light in self.lightpositions:
			if 	self.lightpositions[light]['x'] <= event.x and \
				self.lightpositions[light]['x']+12 >= event.x and \
				self.lightpositions[light]['y'] <= event.y and \
				self.lightpositions[light]['y']+12 >= event.y:
					print "light %d!!" % light
					if light < 16:
						addRange = '00-15'
					elif light >= 16 and light < 32:
						addRange = '16-31'
					elif light >=32 and light < 48:
						addRange = '32-47'
					else:
						addRange = '48-63'

					DMXutil.render(addRange,light)


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
		
		print input_device.type

	def action(self):
		while True:
			if self.input_device.type == "Arduino":
				if self.playThread:
					print "Playing Arduino"
					self.input_device.cue()
					while True:
						output =  self.input_device.readSequence()
						self.output_device.senddmx(OperaPins,output)
						if not self.playThread:
							print "Stopping Arduino"
							self.input_device.stop()
							self.output_device.all(0)
							break
					

			elif self.input_device.type == "IRCAM":
				if self.playThread:
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
		print "stop"
		self.playThread = False

#========================================================================
# MAIN PROGRAM
#========================================================================

if __name__ == "__main__":


	def initSetup(*args):

		def quitProgram():
			sys.exit('User Quit')

		def cont():
			global EnttecPort,ArduinoPort,IrcamIP,IrcamPort 
			print PortSelectOut
			EnttecPort = Out_device.get()
			ArduinoPort = In_device.get()
			IrcamIP = NetworkIP.get()
			IrcamPort = NetworkPort.get()
			print "Ports Submitted"
			master2.destroy()
			return EnttecPort,ArduinoPort,IrcamIP,IrcamPort



		avPorts = [port for port in os.listdir('/dev/') if port[:4] == 'tty.' and port[:8] != 'tty.Blue' ]

		if avPorts == None: 
			avPorts = ['']
				
		master2 = Tk()
		master2.title('Configuration')

		for e in args:
			Label(master2, text="%s Not working" % e,bg='#E8E9E8').pack()

		# Serial Port Settings
		Label(master2, text="Arduino Input",bg='#E8E9E8').pack()

		In_device = StringVar(master2)
		Input1 = avPorts[0]
		for dev in avPorts:
			if dev[:10] == "tty.usbmod":
				In_device.set(dev)
				break
		
		
		PortSelectIn = OptionMenu(master2, In_device,*avPorts).pack()


		Label(master2, text="DMX output device",bg='#E8E9E8').pack()

		Out_device = StringVar(master2)
		Out_device.set('tty.usbserial-EN172718')
		PortSelectOut = OptionMenu(master2, Out_device,*avPorts).pack()

		# Networking Settings
		NetworkIP = StringVar(master2)
		NetworkIP.set('localhost')

		NetworkPort = IntVar(master2)
		NetworkPort.set('7003')

		Label(master2, text="Netowrk Receive Address",bg='#E8E9E8').pack()
		NetowrkIP = Entry(master2,width=20,bd=1,textvariable=NetworkIP).pack()
		Label(master2, text="Port",bg='#E8E9E8').pack()
		Netowrkport = Entry(master2,width=6,bd=1,textvariable=NetworkPort).pack()

		# Action Buttons
		submitPorts = Button(master2, text="Continue",command=cont).pack()
		cancel = Button(master2, text="Abort",command=quitProgram).pack()

		master2.mainloop()


	EnttecPort = ''
	ArduinoPort = ''
	IrcamIP = ''
	IrcamPort = 0

	initSetup()

	portsWorking = False
	while not portsWorking:
			try:

				EntTec = EntTec('/dev/' + EnttecPort,defaultMap)

				Arduino = Arduino('/dev/' + ArduinoPort,250000)

				IRCAM = IRCAM(IrcamIP,IrcamPort)

				portsWorking = True
			except Exception as e:
				initSetup(e)




	



	master = Tk()

	styleKwargs = {'background':'#E8E9E8','highlightbackground':'#E8E9E8'}

	master.configure(**styleKwargs)
	master.minsize(width=1000,height=600)
	master.title('Paris Opera - Haroon Mirza')

	OperaPins = range(1,64,8)

	HaroonThread = ThreadedMapper(Arduino,EntTec)
	IrcamThread = ThreadedMapper(IRCAM,EntTec)

	DMXaddressesFrame = Frame(padx=10,pady=10,**styleKwargs)
	DMXutil = DMXaddressUtil(DMXaddressesFrame,channelColours)
	DMXaddressesFrame.grid(row=1,column=1)

	OperaCanvas = Canvas(width=600, height=500,**styleKwargs)
	lightCan = lightCanvas(OperaCanvas)
	lightCan.render()
	master.bind("<Button-1>", lightCan.lampSelect)

	ControlButtonFrame = Frame(padx=10, **styleKwargs)
	ControlButtonFrame.grid(row=0,column=0)

	buttonDims = {'width':20} 
	buttonDims.update(styleKwargs)

	StartArduino = Button(ControlButtonFrame, text="Start Arduino",command=HaroonThread.start, **buttonDims)
	StartIrcam = Button(ControlButtonFrame, text="Start IRCAM",command=IrcamThread.start, **buttonDims)
	KillArduino = Button(ControlButtonFrame, text="Kill Arduino",command=HaroonThread.stop, **buttonDims)
	KillIrcam = Button(ControlButtonFrame, text="Kill IRCAM",command=IrcamThread.stop, **buttonDims)

	Label(ControlButtonFrame, text="Haroon", **styleKwargs).grid(row=0,column=0)

	StartArduino.grid(row=1,column=0)
	KillArduino.grid(row=2,column=0)

	Label(ControlButtonFrame, text=" ", **styleKwargs).grid(row=3,column=0)

	Label(ControlButtonFrame, text="Boulez", **styleKwargs).grid(row=4,column=0)

	StartIrcam.grid(row=5,column=0)
	KillIrcam.grid(row=6,column=0)




	master.mainloop()
