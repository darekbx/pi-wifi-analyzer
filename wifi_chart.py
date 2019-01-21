import os
import pygame
import itertools
import random
import sys
sys.path.insert(0, '/path/to/application/app/folder')

from sets import Set

from color import Color
from scan_result import ScanResult

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