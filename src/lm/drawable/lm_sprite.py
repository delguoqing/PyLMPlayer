from lm.type import lm_type_color
import lm_drawable
import lm_drawable_container

from pyglet.gl import *

class CDrawable(lm_drawable_container.CDrawable):
				
	def draw(self):
		glPushMatrix()
		glMultMatrixf(self.matrix.get_ctype())
		
		for drawable in self:
			if self._is_dirty:
				drawable.apply_cxform(self._tot_cadd, self._tot_cmul)
			drawable.draw()
		self._is_dirty = False
		
		glPopMatrix()