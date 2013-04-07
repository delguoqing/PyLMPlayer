import itertools
import collections
import lm_drawable

from ctypes import *
from pyglet.gl import *


class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, max_depth, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent=parent)
		self._drawables = [None] * max_depth
		self._max_depth = max_depth
			
	def add_drawable(self, drawable, depth):
		self._drawables[depth] = drawable
	
	def get_drawable(self, depth):
		return self._drawables[depth]
		
	def remove_drawable(self, depth):
		self._drawables[depth] = None

	def draw(self, render_state):
		render_state.push_matrix(self.matrix)
		render_state.push_cxform(self.color_add, self.color_mul)
		render_state.push_blend_mode(self.blend_mode)
		
		clip_depth = 0
		
		for drawable in self:
			if not drawable.clip_depth:
				drawable.draw(render_state)
				if clip_depth and drawable.depth == clip_depth:
					glDisable(GL_SCISSOR_TEST)
			else:
				# Set Scissors
				# Assume that:
				# 1. no nested scissor
				# 2. no rotated or skewed scissor
				# improve this!
				clip_depth = drawable.clip_depth
				glEnable(GL_SCISSOR_TEST)
				mat = (GLfloat * 16)()
				glGetFloatv(GL_MODELVIEW_MATRIX, mat)
				_r = drawable._rect
				glScissor(int(_r.xmin * mat[0] + mat[12]), 272-int(_r.ymax * mat[5] + mat[13]), int(_r.width * mat[0]), int(_r.height * mat[5]))
			
		render_state.pop_matrix()
		render_state.pop_cxform()
		render_state.pop_blend_mode()		
			
	def __iter__(self):
		return itertools.ifilter(None, self._drawables)
		
	def destroy(self):
		for drawable in self:
			drawable.destroy()
		self._drawables = [None] * self._max_depth
		super(CDrawable, self).destroy()