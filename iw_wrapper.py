import os
from iw_parser import IwParser

class Iw:

	scanResults = []
	region = None
	isForPI = False
	maxCapacity = 144

	regionGetCommand = "iw reg get"
	regionSetCommand = "sudo iw reg set {0}"
	searchArguments = "BSS|SSID|freq|signal"
	commandCosmose = "sudo iw dev wlp4s0 scan freq 2447 | egrep \"" + searchArguments + "\""
	commandPi = "sudo iw dev wlan0 scan | egrep \"" + searchArguments + "\""

	def setRegion(self, region):
		self.executeCommand(self.regionSetCommand.format(region))

	def loadRegion(self):
		if self.region is None:
			output = self.executeCommand(self.regionGetCommand)
			self.region = IwParser().parseRegion(output)
		return self.region

	def fetchFrequencies(self):
		output = self.executeCommand(self.regionGetCommand)
		return IwParser().parseFrequencies(output)

	def scan(self, isPassive = True, frequency = None):
		command = self.commandPi if self.isForPI else self.commandCosmose
		output = os.popen(command.format()).read()
		scanResult = IwParser().parseScan(output, self.searchArguments)
		if len(scanResult) > 0:
			dataCount = len(self.scanResults)
			if dataCount >= self.maxCapacity:
				self.scanResults.pop(0)
			self.scanResults.append(scanResult)

			#for r in scanResult:
			#	print r.bssid
			#	print self.executeCommand("sudo aireplay-ng -0 1 -a {} -c a8:96:75:32:9d:ec wlp4s0".format(r.bssid))

	def executeCommand(self, command):
		return os.popen(command).read()