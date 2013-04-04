import itertools
import collections
import lm_drawable

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
		if self.matrix:
			glPushMatrix()
			glMultMatrixf(self.matrix.get_ctype())
#		if self.color_mul:
#			glColor4f(self.color_mul.r,  self.color_mul.g, self.color_mul.b, self.color_mul.a)
		
		has_cxform = self.color_mul or self.color_add
		if has_cxform:
			render_state.push_cxform(self.color_add, self.color_mul)
			
		for drawable in self:
			drawable.draw(render_state)
		if self.matrix:
			glPopMatrix()
#		if self.color_mul:
#			glColor4f(1, 1, 1, 1)

		if has_cxform:
			render_state.pop_cxform()
			
	def __iter__(self):
		return itertools.ifilter(None, self._drawables)
		
	def destroy(self):
		for drawable in self:
			drawable.destroy()
		self._drawables = [None] * self._max_depth
		super(CDrawable, self).destroy()