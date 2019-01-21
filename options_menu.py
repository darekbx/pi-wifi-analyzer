import pygame

from color import Color
from bottom_menu import BottomMenu

class OptionsMenu:

	bottomMenu = None

	isOkActive = True
	isBackActive = True

	selectedOption = 1

	def __init__(self):
		self.bottomMenu = BottomMenu()
		self.font = pygame.font.SysFont("monospace", 14)

	def displayMenu(self, screen):

		self.drawOption("SET REGION", 0, screen)
		self.drawOption("SCAN METHOD", 1, screen)
		self.drawOption("SHOW FREQUENCIES", 2, screen)
		self.drawOption("CONTINUOUS SCAN", 3, screen)

		self.drawMenuButtons(screen)

	def handleKeys(self, event):
		if event.key == 49:
			self.selectedOption = max(0, self.selectedOption - 1)
		if event.key == 50:
			self.selectedOption = min(3, self.selectedOption + 1)
		if event.key == 51:
			a = 0
		if event.key == 52:
			d = 0

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
