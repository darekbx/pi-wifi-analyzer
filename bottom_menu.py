import pygame

from color import Color

class BottomMenu:

	font = None
	arrowsFont = None

	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 14)
		self.arrowsFont = pygame.font.SysFont("monospace", 18, 1)
	
	def drawMenuArrow(self, text, leftOffset, screen):
		self.drawYellowBox(screen, leftOffset)
		label = self.arrowsFont.render(text, 1, Color.defaultDark)
		screen.blit(label, (34 + leftOffset, 220))

	def drawMenuItem(self, text, leftOffset, screen):
		self.drawYellowBox(screen, leftOffset)
		label = self.font.render(text, 1, Color.defaultDark)
		screen.blit(label, (24 + leftOffset, 221))       
		
	def drawYellowBox(self, screen, leftOffset):
		pygame.draw.rect(screen, Color.yellow, [15 + leftOffset, 220, 50, 18])