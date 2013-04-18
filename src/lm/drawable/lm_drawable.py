from lm.type import lm_type_color
from lm.type import lm_type_blend_mode
from lm.type import lm_type_mat
from lm import lm_glb

import pyglet

class CDrawable(object):

	def __init__(self, inst_id, depth, parent=None):
		self.color_add = None
		self.color_mul = None
		self.matrix = None
		self.blend_mode = None
		self.clip_depth = 0

		self.parent = parent
		self.inst_id = inst_id

		self.depth = depth
		self._as_tween_only = False
		self._inited = False
	
	def is_movieclip(self):
		return False
		
	def _get_forbid_timeline(self):
		return self._as_tween_only
	forbid_timeline = property(_get_forbid_timeline)
				
	def update(self, render_state, draw=True):
		raise NotImplementedError
	
	def set_cxform(self, cadd, cmul):
		if cadd:
			if cadd == lm_glb.null_cadd:
				self.color_add = None
			else:
				self.color_add = cadd
		if cmul:
			if cmul == lm_glb.null_cmul:
				self.color_mul = None
			else:
				self.color_mul = cmul
	
	def get_color_add(self):
		return self.color_add
		
	def get_color_mul(self):
		return self.color_mul
		
	def get_blend_mode(self):
		return self.blend_mode
		
	def set_matrix(self, matrix):
		if matrix is not None:
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