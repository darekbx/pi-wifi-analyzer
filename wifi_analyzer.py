import sys
import pygame
import threading
import time

from iw_wrapper import Iw

'''
Bottom buttons: scan, reset, menu, histogram / chart

Display: region, is continous scan, scan method

Menu:
 - set region: list with 6-8 ico codes
 - scan method: active, passive
 - print frequencies from current region
 - continous scan on/off
'''

class Color:
	defaultLight = (192, 200, 198)
	defaultDark = (29, 31, 33)
	black = (0, 0, 0)
	yellow = (240, 198, 116)
	teal = (94, 141, 135)

class WifiAnalyzer():

	iw = Iw()

	isFullScreen = False
	font = None
	screen = None

	isChart = True

	def createScreen(self):
		pygame.init()
		self.font = pygame.font.SysFont("monospace", 14)

		if self.isFullScreen:
			size = pygame.display.list_modes()[0]
			self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((320,240))
		
		self.erase()

	def drawHeader(self):
		padding = 5
		self.screen.blit(self.font.render("Wifi Analyzer", 1, Color.defaultLight), (5, padding))
		
		# TODO: make battery percentage live
		self.screen.blit(self.font.render("battery xx%", 1, (204,102,102)), (220, padding))

	def drawInfo(self):
		pygame.draw.rect(self.screen, Color.teal, [7, 28, 302, 20])
		self.screen.blit(self.font.render("Region", 1, Color.defaultDark), (13, 29))
		self.screen.blit(self.font.render(self.iw.region, 1, Color.yellow), (68, 29))

	def drawMenu(self):
		self.drawMenuItem("SCAN", 0)
		self.drawMenuItem("RSET", 79)
		self.drawMenuItem("MENU", 158)
		self.drawMenuItem("HIST" if self.isChart else "CHRT", 236)

	def drawMenuItem(self, text, leftOffset):
		pygame.draw.rect(self.screen, Color.yellow, [15 + leftOffset, 220, 50, 18])
		label = self.font.render(text, 1, Color.defaultDark)
		self.screen.blit(label, (23 + leftOffset, 221))

	def drawBorder(self):
		top = 26
		pygame.draw.lines(self.screen, Color.defaultLight, False, [(5,top), (5,230), (10,230)], 1)
		pygame.draw.lines(self.screen, Color.defaultLight, False, [(305,230), (310,230), (310,top), (5,top)], 1)

		singleLines = [
			[[69,230], [88,230]], 
			[[149,230], [168,230]], 
			[[228,230], [246,230]]
		]
		for line in singleLines:
			pygame.draw.line(self.screen, Color.defaultLight, line[0], line[1], True)

	def erase(self):
		self.screen.fill(Color.black)

	def runAsyncActions(self):
		self.loadIwRegion()

	def loadIwRegion(self):
		threading.Thread(target=self.iw.loadRegion).start()

	def loop(self):
		i = 0
		while True:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
				    pygame.quit()
				    quit()

			self.erase()
			self.drawBorder()
			self.drawHeader()
			self.drawMenu()
			self.drawInfo()

			pygame.draw.lines(self.screen, (80,0,0), False, [(i,100), (150,200), (200,100)], 1)
			pygame.display.update()
			pygame.time.delay(50)
			i = i + 1

wifiAnalyzer = WifiAnalyzer()
wifiAnalyzer.createScreen()
wifiAnalyzer.runAsyncActions()
wifiAnalyzer.loop()