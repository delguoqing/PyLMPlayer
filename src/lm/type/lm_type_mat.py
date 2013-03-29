import ctypes

class CType(object):
	
	def __init__(self, translate, scale, rotateskew):
		self.translate = translate
		self.scale = scale
		self.rotateskew = rotateskew
		
	def get_ctype(self):
		return (ctypes.c_float * 16)(
			self.scale[0], self.rotateskew[0], 0, 0,
			self.rotateskew[1], self.scale[1], 0, 0,
			0, 0, 1, 0,
			self.translate[0], self.translate[1], 0, 1,
		)