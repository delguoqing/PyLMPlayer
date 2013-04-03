from lm.type import lm_type_color
import lm_drawable
import lm_drawable_container

from pyglet.gl import *

class CDrawable(lm_drawable_container.CDrawable):
		
	def clear(self):
		# Clear all shapes' view, but no remove
		for _d in self:
			_d.clear()