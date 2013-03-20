class CType(object):
	
	def __init__(self, xmin, ymin, xmax, ymax):
		self.xmin = xmin
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax
		
	def get_center(self):
		return (self.xmin + self.xmax) * 0.5