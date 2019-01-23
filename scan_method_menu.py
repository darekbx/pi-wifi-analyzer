import pygame
import threading

from color import Color

class ScanMethodMenu:

	font = None
	selectedOption = 0

	def __init__(self):
		pygame.init()
		self.font = pygame.font.SysFont("monospace", 14)

	def drawMethodMenu(self, screen):
		self.drawOption("ACTIVE", 0, screen)
		self.drawOption("PASSIVE", 1, screen)

	def drawOption(self, label, index, screen):
		xPos = 95
		yPos = 125 + index * 20

		if index == self.selectedOption:
			pygame.draw.circle(screen, Color.defaultLight, (xPos - 12,yPos + 8),3)

		screen.blit(self.font.render(label, 1, Color.defaultLight), (xPos, yPos))

	def handleKeys(self, event, callback):
		if event.key == 49:
			self.selectedOption = max(0, self.selectedOption - 1)
		if event.key == 50:
			self.selectedOption = min(1, self.selectedOption + 1)
		if event.key == 51:
			callback(self.getMethod())
		if event.key == 52:
			callback()
	
	def getMethod(self):
		return {'method' : "" if self.selectedOption == 0 else "passive" }