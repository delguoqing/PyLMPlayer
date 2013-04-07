from lm.type import lm_type_color
import lm_drawable
import lm_drawable_container

from pyglet.gl import *

class CDrawable(lm_drawable_container.CDrawable):
		
	def __init__(self, rect, max_depth, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(max_depth, inst_id, depth, parent)
		self._rect = rect