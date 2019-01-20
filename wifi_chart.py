import os
import pygame
import itertools
from sets import Set
import random
import colorsys
#
# TODO: move to file
#
class ScanResult():
	bssid = ''
	ssid = ''
	frequency = ''
	level = ''

	def __init__(self, frequency, level):
		self.frequency = frequency
		self.level = level
		return

	def toString(self):
		return "%s\n%s\n%s\n%s\n" % (self.bssid, self.ssid, self.frfrequencyeq, self.level) 

class WifiChart:

	font = None
	worstDBm = -100
	bestDBm = -30
	leftX = 12
	bottomY = 200
	areaWidth = 300
	levelMultipler = 2

	cache = []

	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 12)
	def draw(self, screen, data):
		self.drawAxes(screen)
		#self.drawBarResults(screen, data)
		self.drawLineResults(screen, data)

	def drawAxes(self, screen):
		pygame.draw.line(screen, Color.defaultLight, [self.leftX, self.bottomY], [300, self.bottomY], True)

	def drawLineResults(self, screen, results):
		x = len(self.cache) + self.leftX
		cacheEntry = []

		for index, cacheEntry in enumerate(self.cache):
			for level in cacheEntry:
				pygame.draw.circle(screen, Color.defaultLight, [index + self.leftX, level], 1)

		for result in results:
			level = self.bottomY + int((self.worstDBm - result.level) * self.levelMultipler)
			
			if random.randint(0,20) % 5 == 0:
				level = level + random.randint(0, 6)

			pygame.draw.circle(screen, Color.defaultLight, [x, level], 1)
			cacheEntry.append(level)

		self.cache.append(cacheEntry)


	def drawBarResults(self, screen, results):
		y = self.bottomY
		frequencyResults = itertools.groupby(data, key=lambda x: x.frequency)
		uniqueFrequencies = Set([r.frequency for r in results])
		chunkSize = self.chunkSize(len(uniqueFrequencies))
		for index, (frequency, results) in enumerate(frequencyResults):
			x = index * chunkSize + self.leftX
			freqString = "{0}".format(frequency)
			screen.blit(self.font.render(freqString, 1, Color.frequency), (x, y + 5))
			pygame.draw.line(screen, Color.defaultLight, [x + 0, y], [x + 0, y + 3], True)

			resultsList = list(results)
			resultRatio = chunkSize / len(resultsList)
			for innerIndex, result in enumerate(resultsList):
				level = (self.worstDBm - result.level) * self.levelMultipler
				innerX = x + innerIndex * resultRatio # append value to innerIndex to make padding between result lines
				pygame.draw.rect(screen, Color.defaultLight, [innerX, y, resultRatio - 1, level])

	def chunkSize(self, frequenciesCount):
		return 300.0 / frequenciesCount







#
# Mock
#
class Color:
	defaultLight = (240, 230, 220)
	frequency = (240, 150, 100)


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1000,800)
screen = pygame.display.set_mode((320,240))
pygame.init()

wifiChart = WifiChart()

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()

	screen.fill((0,0,0))

	top = 26
	pygame.draw.lines(screen, Color.defaultLight, False, [(5,top), (5,230), (10,230)], 1)
	pygame.draw.lines(screen, Color.defaultLight, False, [(305,230), (310,230), (310,top), (5,top)], 1)
	
	data = [
		ScanResult(2412, -90),
		ScanResult(2412, -50),
		ScanResult(2412, -40),
		ScanResult(2417, -76),
		ScanResult(2422, -87),
		ScanResult(2427, -54),
		ScanResult(2427, -59),
		ScanResult(2427, -78),
		ScanResult(2427, -44),
		ScanResult(2447, -91),
		ScanResult(2447, -88),
		ScanResult(2452, -33),
		ScanResult(2452, -45),
		ScanResult(2452, -55),
		ScanResult(2462, -64),
		ScanResult(2472, -75),
		ScanResult(2472, -73),
		ScanResult(2472, -71),
		ScanResult(2472, -55),
		ScanResult(2472, -78),
		ScanResult(2472, -79),
		ScanResult(2472, -80),
		ScanResult(2484, -66)
	]


	wifiChart.draw(screen, data)
	pygame.time.delay(250)
	pygame.display.update()
#
#
#

