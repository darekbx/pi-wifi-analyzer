import pygame
import threading

from iw_wrapper import Iw
from color import Color

class RegionMenu:

	iw = None

	regions = ['00', 'PL', 'CN', 'JP', 'HK', 'US', 'FR']
	regionLoaded = False
	font = None
	selectedOption = -1

	def __init__(self, isRpi):
		pygame.init()
		self.iw = Iw(isRpi)
		self.font = pygame.font.SysFont("monospace", 14)

	def drawRegionsMenu(self, screen):
		if not self.regionLoaded:
			self.loadIwRegionAsync()
		for index,region in enumerate(self.regions):
			self.drawOption(region, index, screen)

	def drawOption(self, label, index, screen):
		xPos = 95
		yPos = 55 + index * 20

		if index == self.selectedOption:
			pygame.draw.circle(screen, Color.defaultLight, (xPos - 12,yPos + 8),3)

		screen.blit(self.font.render(label, 1, Color.defaultLight), (xPos, yPos))

	def confirmRegion(self):
		self.iw.setRegion(self.regions[self.selectedOption])

	def handleKeys(self, event, callback):
		if event.key == 49:
			self.selectedOption = max(0, self.selectedOption - 1)
		if event.key == 50:
			regionsCount = len(self.regions)
			self.selectedOption = min(regionsCount, self.selectedOption + 1)
		if event.key == 51:
			self.confirmRegion()
			callback()
		if event.key == 52:
			callback()
	
	def loadRegionWrapper(self):
		self.iw.loadRegion()
		if self.iw.region is not None:
			if self.iw.region in self.regions:
				self.selectedOption = self.regions.index(self.iw.region)
			else:
				self.selectedOption = self.regions[0]
			self.regionLoaded = True

	def loadIwRegionAsync(self):
		threading.Thread(target=self.loadRegionWrapper).start()