import os
from iw_parser import IwParser

class Iw:

	scanResults = []
	region = None
	isForPI = False

	regionCommand = "iw reg get"
	searchArguments = "BSS|SSID|freq|signal"
	commandCosmose = "sudo iw dev wlp4s0 scan | egrep \"" + searchArguments + "\""
	commandPi = "sudo iw dev wlan0 scan | egrep \"" + searchArguments + "\""

	def loadRegion(self):
		if self.region is None:
			output = self.executeCommand(self.regionCommand)
			self.region = IwParser().parseRegion(output)
		return self.region

	def fetchFrequencies(self):
		output = self.executeCommand(self.regionCommand)
		return IwParser().parseFrequencies(output)

	def scan(self, isPassive = True, frequency = None):
		command = self.commandPi if self.isForPI else self.commandCosmose
		output = os.popen(command.format()).read()
		scanResult = IwParser().parseScan(output, self.searchArguments)
		if len(scanResult) > 0:
			self.scanResults.append(scanResult)

	def executeCommand(self, command):
		return os.popen(command).read()