import os
import pygame
import itertools
import random

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
	levelMultipler = 2.2

	def __init__(self):
		self.font = pygame.font.SysFont("monospace", 12)
	
	def draw(self, screen, data):
		self.drawAxes(screen)
		#self.drawBarResults(screen, data)
		self.drawLineResults(screen, data)

	def drawAxes(self, screen):
		pygame.draw.line(screen, Color.defaultLight, [self.leftX, self.bottomY], [300, self.bottomY], True)

	def drawLineResults(self, screen, results):
		x = self.leftX
		for result in results:

			for scanSample in result:
				level = (self.bottomY) + int((self.worstDBm - scanSample.level) * self.levelMultipler)
				pygame.draw.circle(screen, Color.defaultLight, [x, level], 1)

			x = x + 2

	def drawBarResults(self, screen, results):
		y = self.bottomY
		for result in results:
			frequencyResults = itertools.groupby(result, key=lambda x: x.frequency)
			uniqueFrequencies = Set([r.frequency for r in result])
			chunkSize = self.chunkSize(len(uniqueFrequencies))
			for index, (frequency, result) in enumerate(frequencyResults):
				x = index * chunkSize + self.leftX
				freqString = "{0}".format(frequency)
				screen.blit(self.font.render(freqString, 1, Color.frequency), (x, y + 5))
				pygame.draw.line(screen, Color.defaultLight, [x + 0, y], [x + 0, y + 3], True)

				resultList = list(result)
				resultRatio = 4#chunkSize / len(resultList)
				for innerIndex, scanSample in enumerate(resultList):
					level = (self.worstDBm - scanSample.level) * self.levelMultipler
					innerX = x + innerIndex * resultRatio # append value to innerIndex to make padding between result lines
					pygame.draw.rect(screen, Color.defaultLight, [innerX, y, resultRatio - 1, level])

	def chunkSize(self, frequenciesCount):
		return 300.0 / frequenciesCount