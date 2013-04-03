from lm.type import lm_type_color
from lm.type import lm_type_blend_mode
from lm.type import lm_type_mat

import pyglet
import lm_render_state

class CDrawable(object):

	def __init__(self, inst_id, depth, parent=None):
		self.color_add = None
		self.color_mul = None
		self.matrix = None
		self.blend_mode = None

		self.parent = parent
		self.inst_id = inst_id

		self.depth = depth

		if parent is None:
			self._render_state = lm_render_state.CObj()
			
	def draw(self, render_state):
		raise NotImplementedError
	
	def set_cxform(self, cadd, cmul):
		if cadd:
			self.color_add = cadd
		if cmul:
			self.color_mul = cmul
	
	def get_color_add(self):
		return self.color_add
		
	def get_color_mul(self):
		return self.color_mul
		
	def set_matrix(self, matrix):
		if matrix:
			self.matrix = matrix

	def get_matrix(self):
		return self.matrix
		
	def set_blend_mode(self, blend_mode):
		self.blend_mode = blend_mode
	
	def destroy(self):
		self.color_add = None
		self.color_mul = None
		self.matrix = None
		self.blend_mode = None
		self.parent = None
		
	def clear(self):
		pass