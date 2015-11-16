import subprocess, os, signal
from device import device
from time import sleep

class processing(device):
	""" Launches the Oscilliscope program """
	def __init__(self):
		pass
	def open(self, dir):
		cwd = os.getcwd()
		print type(dir)
		directory = '--sketch=' + cwd + '/' + dir
		cmd = ['processing-java', directory, '--run']
		print cmd
		self.program = subprocess.Popen(cmd)

	def kill(self):
		self.program.kill()
		print 'ended it'

if __name__ == '__main__':
	processing = processing()
	processing.open('Oscilliscope')
	sleep(5)
	print 'end!!'
	processing.kill()
