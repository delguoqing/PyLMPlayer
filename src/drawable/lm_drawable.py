class CDrawable(object):

	def __init__(self, tag):
		pass
		
	def draw(self):
		raise NotImplementedError
	
	def set_color_add(self, color):
		pass
		
	def set_color_mul(self, color):
		pass
		
	def set_pos(self, pos):
		pass
		
	def set_matrix(self, mat):
		pass	

	def set_visible(self, b):
		pass
			
	def set_blend_mode(self, mode):
		pass
		
	def destroy(self):
		pass