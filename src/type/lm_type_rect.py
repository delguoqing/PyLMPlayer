class CType(object):
	
	def __init__(self, xmin, ymin, xmax, ymax):
		self.xmin = xmin
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax
		self.center_x = (self.xmin + self.xmax) * 0.5
		self.center_y = (self.ymin + self.ymax) * 0.5
		
	def get_center(self):
		return (self.center_x, self.center_y)
