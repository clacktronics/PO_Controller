from Tkinter import *
from math import sin, cos, pi
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
print arduinoMap

def printfoo():
	print "foo"

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
		# DMX value label
		Label(self.frame, text='Value',bg='#E8E9E8').grid(row=0,column=1)
		# DMX intensity values for all channels
		for rowN,row in enumerate(channelColours):
			DMXValues[rowN] = Entry(self.frame,width=3,bg='#FFE0B2',bd=1,relief=relief,highlightbackground=highlightColor)
			DMXValues[rowN].grid(row=rowN+1,column=1)
			DMXValues[rowN].insert(END,255)


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

		# Arduino mapping
		for lN,channel in enumerate(range(addLow,addHigh)):
			pass

		# Option Buttons

		OPTIONS = ['00-15','16-31','32-47','48-63']
		variable = StringVar(self.frame)
		variable.set(addRange)

		sel = OptionMenu(self.frame, variable,*OPTIONS,command=self.render)
		sel.config(width=10,bg='#FFE0B2')
		
		
		applyButton = Button(self.frame, text="Apply",command=self.applyUpdate)

		sel.grid(row=self.numberColours+2,column=1,columnspan=2)
		applyButton.grid(row=self.numberColours+2,column=3,columnspan=2)

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

		for light in range(64):
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





master = Tk()
master.configure(background='#E8E9E8')
master.title('Paris Opera - Haroon Mirza')


DMXaddressesFrame = Frame(padx=10,pady=10)
DMXaddressesFrame.configure(background='#E8E9E8')
DMXutil = DMXaddressUtil(DMXaddressesFrame,channelColours)
DMXaddressesFrame.grid(row=1,column=1)

OperaCanvas = Canvas(master,bg='#E8E9E8',highlightbackground='#E8E9E8', width=600, height=500)
lightCan = lightCanvas(OperaCanvas)
lightCan.render()
master.bind("<Button-1>", lightCan.lampSelect)


master.mainloop()
