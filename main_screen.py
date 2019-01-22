import pygame

from color import Color
from bottom_menu import BottomMenu

class MainScreen:

	font = None
	bottomMenu = None

	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 12)
		self.bottomMenu = BottomMenu()

	def drawMainMenu(self, screen, isChart, isScanning):
		self.bottomMenu.drawMenuItem("STOP" if isScanning else "SCAN", 0, screen)
		self.bottomMenu.drawMenuItem("RSET", 79, screen)
		self.bottomMenu.drawMenuItem("MENU", 158, screen)
		self.bottomMenu.drawMenuItem("HIST" if isChart else "CHRT", 236, screen)

		singleLines = [
			[[69,230], [88,230]], 
			[[149,230], [168,230]], 
			[[228,230], [246,230]]
		]
		for line in singleLines:
			pygame.draw.line(screen, Color.defaultLight, line[0], line[1], True)

	def drawBorder(self, screen):
		top = 26
		pygame.draw.lines(screen, Color.defaultLight, False, [(5,top), (5,230), (10,230)], 1)
		pygame.draw.lines(screen, Color.defaultLight, False, [(305,230), (310,230), (310,top), (5,top)], 1)

	def drawHeader(self, screen):
		padding = 5
		screen.blit(self.font.render("Wifi Analyzer", 1, Color.defaultLight), (5, padding))
		
		# TODO: make battery percentage live
		screen.blit(self.font.render("battery xx%", 1, (204,102,102)), (220, padding))

	def drawInfo(self, screen, isContinusScan, isActiveScan, region):
		pygame.draw.rect(screen, Color.teal, [7, 28, 302, 20])
		screen.blit(self.font.render("Region", 1, Color.defaultDark), (13, 29))
		screen.blit(self.font.render(region, 1, Color.yellow), (68, 29))

		screen.blit(self.font.render("Continuous", 1, Color.defaultDark), (100, 29))
		screen.blit(self.font.render("YES" if isContinusScan else "NO", 1, Color.yellow), (190, 29))

		scanMethodOffset = 254 if isActiveScan else 246
		screen.blit(self.font.render("Active" if isActiveScan else "Passive", 1, Color.yellow), (scanMethodOffset, 29))
