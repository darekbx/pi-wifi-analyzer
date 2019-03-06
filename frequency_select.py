import pygame
import threading

from iw_wrapper import Iw
from color import Color

class FrequencySelect:

	iw = None

	frequencies = None
	font = None
	selectedOption = 0
	maxFrequenciesOnScreen = 8

	def __init__(self, isRpi):
		pygame.init()
		self.iw = Iw(isRpi)
		self.font = pygame.font.SysFont("monospace", 14)

	def reset(self):
		self.frequencies = None

	def drawFrequencyMenu(self, screen):
		if self.frequencies is None:
			self.loadIwFrequenciesAsync()
		else:
			startIndex = min(self.selectedOption - self.maxFrequenciesOnScreen, 0)
			for index, frequency in enumerate(self.frequencies[startIndex, self.maxFrequenciesOnScreen):
				self.drawOption(str(frequency), index, screen)
		
	def drawOption(self, label, index, screen):
		xPos = 95
		yPos = 55 + index * 20

		if index == self.selectedOption:
			pygame.draw.circle(screen, Color.defaultLight, (xPos - 12, yPos + 8),3)

		screen.blit(self.font.render(label, 1, Color.defaultLight), (xPos, yPos))

	def handleKeys(self, event, callback):
		if event.key == 49:
			self.selectedOption = max(0, self.selectedOption - 1)
		if event.key == 50:
			if self.frequencies is not None:
				frequenciesCount = len(self.frequencies)
				self.selectedOption = min(frequenciesCount, self.selectedOption + 1)
		if event.key == 51:
			callback(self.getFrequency())
		if event.key == 52:
			callback()

	def getFrequency(self):
		return {'frequency' : self.frequencies[self.selectedOption] }

	def loadFrequenciesWrapper(self):
		self.frequencies = self.iw.fetchChannels()

	def loadIwFrequenciesAsync(self):
		threading.Thread(target=self.loadFrequenciesWrapper).start()