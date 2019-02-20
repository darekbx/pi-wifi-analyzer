import array, fcntl
from time import sleep

class ButtonsWrapper:

	_IOC_NRBITS = 8
	_IOC_TYPEBITS = 8
	_IOC_SIZEBITS = 14
	_IOC_DIRBITS = 2
	_IOC_DIRMASK = (1 << _IOC_DIRBITS) -1
	_IOC_NRMASK = (1 << _IOC_NRBITS) -1
	_IOC_TYPEMASK = (1 << _IOC_TYPEBITS ) -1
	_IOC_NRSHIFT = 0
	_IOC_TYPESHIFT = _IOC_NRSHIFT+_IOC_NRBITS
	_IOC_SIZESHIFT = _IOC_TYPESHIFT+_IOC_TYPEBITS
	_IOC_DIRSHIFT = _IOC_SIZESHIFT+_IOC_SIZEBITS
	_IOC_NONE = 0
	_IOC_WRITE = 1
	_IOC_READ = 2

	pressedButton = 0

	def getLastPressedKey(self):
		value = self.pressedButton
		self.pressedButton = 0
		return value

	def handleButtonPress(self, pygameKeyCode):
		self.pressedButton = pygameKeyCode

	def _IOC(self, dir, type, nr, size):
		ioc = (dir << self._IOC_DIRSHIFT ) | (type << self._IOC_TYPESHIFT ) | (nr << self._IOC_NRSHIFT ) | (size << self._IOC_SIZESHIFT)
		if ioc > 2147483647: ioc -= 4294967296
		return ioc

	def _IOR(self, type,nr,size):
		return self._IOC(self._IOC_READ, type, nr, size)
	
	def run(self):
		LCD4DPI_GET_KEYS = self._IOR(ord('K'), 1, 4)
		buf = array.array('h',[0])

		with open('/dev/fb1', 'rw') as fd:
			while True:
				fcntl.ioctl(fd, LCD4DPI_GET_KEYS, buf, 1) # execute ioctl call to read the keys
				keys = buf[0]
				if not keys & 0b00001:
					print "Key 1"
				if not keys & 0b00010:
					print "Key 2"
					self.handleButtonPress(52)
				if not keys & 0b00100:
					print "Key 3"
					self.handleButtonPress(51)
				if not keys & 0b01000:
					print "Key 4"
					self.handleButtonPress(50)
				if not keys & 0b10000:
					print "Key 5"
					self.handleButtonPress(49)
				if keys != 0b11111:
					print
				if keys == 0b01110: # exit if top and bottom pressed
					break
				sleep(0.2)