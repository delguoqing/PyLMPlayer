from lm.type import lm_type_color
from lm.type import lm_type_blend_mode
from lm.type import lm_type_mat
from lm import lm_glb
from lm import lm_consts

import pyglet

class CDrawable(object):

	def __init__(self, inst_id, depth, parent=None):
		self.matrix = None
		self.clip_depth = 0

		self._parent = parent
		self.inst_id = inst_id

		self.depth = depth
		self._as_tween_only = False
		self._visible = True
		self.active = True
	
		# indexed data
		self.blend_mode_index = -1
		self.matrix_index = -1
		self.color_add_index = -1
		self.color_mul_index = -1
		
	def is_movieclip(self):
		return False
		
	def _get_forbid_timeline(self):
		return self._as_tween_only
	forbid_timeline = property(_get_forbid_timeline)
			
	def init(self, fully=False):
		pass
			
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		raise NotImplementedError
	
	def log(self, str):
		if self.char_id == 4:
			print "[sprite %d] " % self.char_id, str
	
	def destroy(self):
		self.color_add = None
		self.color_mul = None
		self.matrix = None
		self.blend_mode = None
		self._parent = None
		
	def clear(self):
		pass
	
	# indexed interface
	def set_blend_mode_index(self, blend_mode_index):
		self.blend_mode_index = blend_mode_index
	
	def set_matrix_index(self, matrix_index):
		if matrix_index != -1:
			self.matrix_index = matrix_index
	
	def set_cxform_index(self, color_add_index, color_mul_index):
		if color_add_index != -1:
			self.color_add_index = color_add_index
		if color_mul_index != -1:
			self.color_mul_index = color_mul_index