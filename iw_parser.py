from scan_result import ScanResult

class IwParser:

	def parseRegion(self, output):
		regionStart = output.index(' ') + 1
		regionEnd = output.index(':')
		return output[regionStart:regionEnd]

	def parseFrequencies(self, output):
		frequencies = []
		lines = output.splitlines()
		for line in lines:
			if line[0] != '\t':
				continue
			commaIndex = line.index(',')
			line = line[2:commaIndex - 1]
			frequencies.append(line)
		return frequencies

	def parseScan(self, output, arguments):
		lines = output.splitlines()

		argumentsArray = arguments.split('|')
		sample = None
		samples = []

		for line in lines:
			tabPosition = line.find('\t')
			if tabPosition == -1:
				sample = ScanResult()
				sample.bssid = self.extractValue(line)
				samples.append(sample)
			
			if sample is not None and line.count('\t') == 1:
				for argument in argumentsArray:
					line = line.replace('\t', '')
					position = line.find(argument + ':')
					if position >= 0:
						if argument == 'BSS':
							sample.bssid = self.extractValue(line)
						if argument == 'SSID':
							sample.ssid = self.extractValue(line)
						if argument == 'freq':
							sample.frequency = int(self.extractValue(line))
						if argument == 'signal':
							sample.level = int(self.extractValue(line).rsplit('.', 1)[0])

		return samples

	def extractValue(self, line):
		spacePosition = line.find(' ')
		bracketPosition = line.find('(')
		if bracketPosition == -1:
			bracketPosition = len(line)
		return line[(spacePosition + 1):bracketPosition].strip()