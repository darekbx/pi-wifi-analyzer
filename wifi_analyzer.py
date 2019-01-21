import os
import sys
import pygame
import threading
import time

from iw_wrapper import Iw
from options_menu import OptionsMenu
from bottom_menu import BottomMenu
from color import Color
from wifi_chart import WifiChart
from scan_result import ScanResult

'''
TODO:

In menu select scanning device like wlan0

Bottom buttons: scan, reset, menu, histogram / chart

Menu:
 - scan fast one freq with 20 FPS 
 - set region: list with 6-8 ico codes
 - scan method: active, passive
 - print frequencies from current region
 - continous scan on/off
'''

class WifiAnalyzer():

	iw = Iw()
	wifiChart = None
	bottomMenu = None
	optionsMenu = None

	isFullScreen = False
	font = None
	screen = None
	stopScan = False

	isChart = True
	isContinusScan = False
	isActiveScan = True
	isMenuDisplayed = False

	def createScreen(self):
		pygame.init()
		self.wifiChart = WifiChart()
		self.bottomMenu = BottomMenu()
		self.font = pygame.font.SysFont("monospace", 14)

		if self.isFullScreen:
			size = pygame.display.list_modes()[0]
			self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		else:
			os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1000,800)
			self.screen = pygame.display.set_mode((320,240))
		
		self.erase()
		self.optionsMenu = OptionsMenu()

	def drawHeader(self):
		padding = 5
		self.screen.blit(self.font.render("Wifi Analyzer", 1, Color.defaultLight), (5, padding))
		
		# TODO: make battery percentage live
		self.screen.blit(self.font.render("battery xx%", 1, (204,102,102)), (220, padding))

	def drawInfo(self):
		pygame.draw.rect(self.screen, Color.teal, [7, 28, 302, 20])
		self.screen.blit(self.font.render("Region", 1, Color.defaultDark), (13, 29))
		self.screen.blit(self.font.render(self.iw.region, 1, Color.yellow), (68, 29))

		self.screen.blit(self.font.render("Continuous", 1, Color.defaultDark), (100, 29))
		self.screen.blit(self.font.render("YES" if self.isContinusScan else "NO", 1, Color.yellow), (190, 29))

		scanMethodOffset = 254 if self.isActiveScan else 246
		self.screen.blit(self.font.render("Active" if self.isActiveScan else "Passive", 1, Color.yellow), (scanMethodOffset, 29))

	def drawBottomMenu(self):
		self.bottomMenu.drawMenuItem("SCAN", 0, self.screen)
		self.bottomMenu.drawMenuItem("RSET", 79, self.screen)
		self.bottomMenu.drawMenuItem("MENU", 158, self.screen)
		self.bottomMenu.drawMenuItem("HIST" if self.isChart else "CHRT", 236, self.screen)

		singleLines = [
			[[69,230], [88,230]], 
			[[149,230], [168,230]], 
			[[228,230], [246,230]]
		]
		for line in singleLines:
			pygame.draw.line(self.screen, Color.defaultLight, line[0], line[1], True)

	def drawBorder(self):
		top = 26
		pygame.draw.lines(self.screen, Color.defaultLight, False, [(5,top), (5,230), (10,230)], 1)
		pygame.draw.lines(self.screen, Color.defaultLight, False, [(305,230), (310,230), (310,top), (5,top)], 1)

	def erase(self):
		self.screen.fill(Color.black)

	def runAsyncActions(self):
		self.loadIwRegion()
		self.scan()

	def loadIwRegion(self):
		threading.Thread(target=self.iw.loadRegion).start()

	def scan(self):
		threading.Thread(target=self.scanWorker).start()

	def scanWorker(self):
		if not self.stopScan:
			self.iw.scan()
			pygame.time.delay(500)
			self.scan()

	def handleKeys(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if self.isMenuDisplayed:
					self.optionsMenu.handleKeys(event)
				else:
					self.handleDefaultEvents(event)
						
			if event.type == pygame.QUIT:
				self.stopScan = True
				pygame.quit()
				quit()
	
	def handleDefaultEvents(self, event):
		if event.key == pygame.K_ESCAPE:
			self.stopScan = True
			pygame.quit()
			quit()
		if event.key == pygame.K_0:
			# Scan
			a = 0
		if event.key == pygame.K_1:
			# Reset
			b = 0

		if event.key == 51:
			# Menu
			self.isMenuDisplayed = not self.isMenuDisplayed 
			
		if event.key == 52:
			# Chart type
			d = 0

	def loop(self):
		while True:

			self.handleKeys()

			self.erase()
			self.drawBorder()
			self.drawHeader()

			if self.isMenuDisplayed:
				self.optionsMenu.displayMenu(self.screen)
			else:
				self.drawInfo()
				self.drawBottomMenu()
				self.wifiChart.draw(self.screen, self.iw.scanResults)
			
			pygame.time.delay(50)
			pygame.display.update()


wifiAnalyzer = WifiAnalyzer()
wifiAnalyzer.createScreen()
wifiAnalyzer.runAsyncActions()
wifiAnalyzer.loop()