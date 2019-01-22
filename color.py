import random
import colorsys

class Color:
	defaultLight = (192, 200, 198)
	defaultDark = (29, 31, 33)
	black = (0, 0, 0)
	yellow = (240, 198, 116)
	teal = (94, 141, 135)
	frequency = (181, 189, 104)

	def randomColor(self):
		h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
		r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
		return r,g,b