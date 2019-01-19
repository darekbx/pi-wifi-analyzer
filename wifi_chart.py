import os
import pygame
import itertools


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
	bottomY = 210

	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 12)
	def draw(self, screen, data):
		self.drawAxes(screen)
		self.drawResults(screen, data)

	def drawAxes(self, screen):
		pygame.draw.line(screen, Color.defaultLight, [10, self.bottomY], [305, self.bottomY], True)

	def drawResults(self, screen, results):
		y = self.bottomY
		chunkSize = self.chunkSize(len(results))
		frequencyResults = itertools.groupby(data, key=lambda x: x.frequency)
		for index, (frequency, results) in enumerate(frequencyResults):
			
			x = index * chunkSize + 10
			freqString = "{0}MHz".format(frequency)
			screen.blit(self.font.render(freqString, 1, Color.frequency), (x, y + 5))

			for innerIndex, result in enumerate(results):
				innerOffset = innerIndex * 5 # 5 - should be dynamic
				innerX = x + 15 + innerOffset
				pygame.draw.line(screen, Color.defaultLight, [innerX, y], [innerX, y + result.level], True)

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
		ScanResult(2412, -89),
		ScanResult(2417, -76),
		ScanResult(2422, -87),
		ScanResult(2427, -54),
		ScanResult(2427, -44)
	]


	wifiChart.draw(screen, data)
	pygame.time.delay(50)
	pygame.display.update()
#
#
#

