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
		if self.color_mul:
			glColor4i(self.color_mul.rB,  self.color_mul.gB, self.color_mul.bB, self.color_mul.aB)
		for drawable in self:
			drawable.draw(render_state)
		if self.matrix:
			glPopMatrix()
		if self.color_mul:
			glColor4i(255, 255, 255, 255)
			
	def __iter__(self):
		return itertools.ifilter(None, self._drawables)
		
	def destroy(self):
		for drawable in self:
			drawable.destroy()
		self._drawables = [None] * self._max_depth
		super(CDrawable, self).destroy()