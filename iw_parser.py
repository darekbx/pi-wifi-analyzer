
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