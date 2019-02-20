import pygame

from color import Color
from bottom_menu import BottomMenu
from region_menu import RegionMenu
from scan_method_menu import ScanMethodMenu
from frequency_select import FrequencySelect

class OptionsScreen:

	bottomMenu = None
	regionMenu = None
	frequencySelect = None
	scanMethodMenu = ScanMethodMenu()

	isOkActive = True
	isBackActive = True

	selectedOption = 0
	hideMenu = False
	result = None

	def __init__(self, isRpi):
		self.bottomMenu = BottomMenu()
		self.regionMenu = RegionMenu(isRpi)
		self.frequencySelect = FrequencySelect(isRpi)
		self.font = pygame.font.SysFont("monospace", 14)

	def displayMenu(self, screen):
		if not self.hideMenu:
			self.drawOption("SET REGION", 0, screen)
			self.drawOption("SCAN METHOD", 1, screen)
			self.drawOption("SHOW FREQUENCIES", 2, screen)
			self.drawOption("CONTINUOUS SCAN", 3, screen)
		else:
			if self.selectedOption == 0:
				self.regionMenu.drawRegionsMenu(screen)
			elif self.selectedOption == 1:
				self.scanMethodMenu.drawMethodMenu(screen)
			elif self.selectedOption == 2:
				self.frequencySelect.drawFrequencyMenu(screen)

		self.drawMenuButtons(screen)

	def handleKeys(self, event, callback):
		if not self.hideMenu:
			if event.key == 49:
				self.selectedOption = max(0, self.selectedOption - 1)
			if event.key == 50:
				self.selectedOption = min(3, self.selectedOption + 1)
			if event.key == 51:
				self.confirmOption()
			if event.key == 52:
				callback(self.result)
		else:
			if self.selectedOption == 0:
				self.regionMenu.handleKeys(event, self.subMenuGoBack)
			elif self.selectedOption == 1:
				self.scanMethodMenu.handleKeys(event, self.subMenuGoBack)
			elif self.selectedOption == 2:
				self.frequencySelect.handleKeys(event, self.subMenuGoBack)

	def confirmOption(self):
		self.hideMenu = True

	def subMenuGoBack(self, result=None):
		self.hideMenu = False
		self.result = result

	def drawOption(self, label, index, screen):
		xPos = 95
		yPos = 85 + index * 20

		if index == self.selectedOption:
			pygame.draw.circle(screen, Color.defaultLight, (xPos - 12,yPos + 8),3)

		screen.blit(self.font.render(label, 1, Color.defaultLight), (xPos, yPos))

	def drawMenuButtons(self, screen):
		self.bottomMenu.drawMenuArrow(u"\u2191", 0, screen)
		self.bottomMenu.drawMenuArrow(u"\u2193", 79, screen)

		self.bottomMenu.drawMenuItem(" OK" if self.isOkActive else "", 158, screen)
		self.bottomMenu.drawMenuArrow(u"\u2190" if self.isBackActive else "", 236, screen)

		singleLines = [
			[[69,230], [88,230]], 
			[[149,230], [168,230]], 
			[[228,230], [246,230]]
		]
		for line in singleLines:
			pygame.draw.line(screen, Color.defaultLight, line[0], line[1], True)
