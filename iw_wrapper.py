import os
from iw_parser import IwParser

class Iw:

	region = None

	regionCommand = "iw reg get"

	def loadRegion(self):
		if self.region is None:
			output = self.executeCommand(self.regionCommand)
			self.region = IwParser().parseRegion(output)
		return self.region

	def fetchFrequencies(self):
		output = self.executeCommand(self.regionCommand)
		return IwParser().parseFrequencies(output)

	def executeCommand(self, command):
		return os.popen(command).read()
