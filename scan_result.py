class ScanResult():
	bssid = ''
	ssid = ''
	frequency = ''
	level = ''

	def __init__(self, frequency = '', level = ''):
		self.frequency = frequency
		self.level = level
		return

	def toString(self):
		return "%s\n%s\n%s\n%s\n" % (self.bssid, self.ssid, self.frequency, self.level) 
