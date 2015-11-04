import subprocess, os, signal
from device import device
from time import sleep

class processing(device):
	""" Launches the Oscilliscope program """
	def __init__(self, dir):
		self.dir = dir

	def open(self):
		cwd = os.getcwd()
		directory = '--sketch=' + cwd + '/' + self.dir
		cmd = ['processing-java', directory, '--run']
		print cmd
		self.program = subprocess.Popen(cmd)

	def kill(self):
		self.program.kill()
		print 'ended it'



if __name__ == '__main__':
	processing = processing('Oscilliscope')
	processing.open()
	sleep(5)
	print 'end!!'
	processing.kill()
