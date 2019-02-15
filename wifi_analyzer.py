import os
import sys
import pygame
import threading
import time

from iw_wrapper import Iw
from color import Color
from wifi_chart import WifiChart
from scan_result import ScanResult
from main_screen import MainScreen
from options_screen import OptionsScreen
from buttons_wrapper import ButtonsWrapper

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

	buttonsWrapper = ButtonsWrapper()
	iw = Iw()
	wifiChart = None
	optionsScreen = None
	mainScreen = None

	isRpi = False
	font = None
	screen = None
	isScanning = True

	isChart = True
	isContinusScan = False
	isActiveScan = True
	isMenuDisplayed = False

	lastScanTime = 0

	def createScreen(self):
		pygame.init()
		self.wifiChart = WifiChart()
		self.mainScreen = MainScreen()
		self.font = pygame.font.SysFont("monospace", 14)

		if self.isRpi:
			size = pygame.display.list_modes()[0]
			self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		else:
			os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1000,800)
			self.screen = pygame.display.set_mode((320,240))
		
		self.handleButtons()
		self.eraseScreen()
		self.optionsScreen = OptionsScreen()

	def eraseScreen(self):
		self.screen.fill(Color.black)

	def reset(self):
		self.iw.resetScanResults()

	def refresh(self):
		self.iw.resetRegion()
		self.loadIwRegion()
	
	def startStopScan(self):
		self.isScanning = not self.isScanning
		if self.isScanning:
			self.scan()

	def runAsyncActions(self):
		self.loadIwRegion()
		self.scan()

	def loadIwRegion(self):
		threading.Thread(target=self.iw.loadRegion).start()

	def scan(self):
		threading.Thread(target=self.scanWorker).start()

	def handleButtons(self):
		threading.Thread(target=self.buttonsWorker).start()

	def buttonsWorker(self):
		try:
			self.buttonsWrapper.run()
		except:
			print('Unable to start buttons worker')

	def scanWorker(self):
		if self.isScanning:
			scanStartTime= self.getTimeInMs()
			self.iw.scan(self.isActiveScan, None)	
			currentTime = self.getTimeInMs()
			self.lastScanTime = currentTime - scanStartTime
			pygame.time.delay(100)
			self.scan()

	def getTimeInMs(self):
		return int(round(time.time() * 1000))

	def hideOptionsMenu(self, result = None):
		self.isMenuDisplayed = False
		if result is not None:
			self.handleResult(result)
		self.refresh()

	def handleResult(self, result):
		if 'method' in result:
			self.isActiveScan = result['method'] == ''
		if 'frequency' in result:
			# TODO: handle frequency
			print result

	def handleKeys(self):
		if self.isRpi:
			pressedButton = self.buttonsWrapper.getLastPressedKey()
			if pressedButton != 0:
				buttonEvent = pygame.event.Event(pygame.KEYDOWN)
				buttonEvent.key = pressedButton
				self.handleKeyEvent(buttonEvent)
		else:
			for event in pygame.event.get():
				self.handleKeyEvent(event)
	
	def handleKeyEvent(self, event):
		if event.type == pygame.KEYDOWN:
			if self.isMenuDisplayed:
				self.optionsScreen.handleKeys(event, self.hideOptionsMenu)
			else:
				self.handleDefaultEvents(event)
					
		if event.type == pygame.QUIT:
			self.endProgram()

	def handleDefaultEvents(self, event):
		if event.key == pygame.K_ESCAPE:
			self.endProgram()
		if event.key == 49:
			# Scan
			self.startStopScan()
		if event.key == 50:
			# Reset
			self.reset()
		if event.key == 51:
			# Menu
			self.isMenuDisplayed = not self.isMenuDisplayed
		if event.key == 52:
			# Chart type
			''

	def endProgram(self):
		self.isScanning = False
		pygame.quit()
		quit()

	def loop(self):
		loopDelay = 50
		while True:

			self.handleKeys()
			self.eraseScreen()

			self.mainScreen.drawBorder(self.screen)
			self.mainScreen.drawHeader(self.screen)

			if self.isMenuDisplayed:
				self.optionsScreen.displayMenu(self.screen)
			else:
				self.mainScreen.drawInfo(self.screen, self.isContinusScan, self.isActiveScan, self.iw.region)
				self.mainScreen.drawMainMenu(self.screen, self.isChart, self.isScanning)
				self.wifiChart.draw(self.screen, self.iw.scanResults)
				self.screen.blit(self.font.render("{}ms".format(self.lastScanTime), 1, Color.defaultLight), (240, 205))
	
			
			pygame.time.delay(loopDelay)
			pygame.display.update()


wifiAnalyzer = WifiAnalyzer()
wifiAnalyzer.createScreen()
wifiAnalyzer.runAsyncActions()
wifiAnalyzer.loop()