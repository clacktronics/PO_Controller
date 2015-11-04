class device():
	def isConnected(self):
		return self.connected

	def isConnectedString(self):
		if self.connected == True:
			return 'Connected'
		else:
			return 'not connected'
