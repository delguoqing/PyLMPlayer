import pyglet
import lm_drawable
from lm.util import lm_shader
from lm.type import lm_type_color

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, color, rect, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent=parent)
		self._color = color
		self._rect = rect
		self._create_vertex_list()
		
	def _create_vertex_list(self):
		self._vertex_list = pyglet.graphics.vertex_list(4,
			('v2f/static', (_r.xmin, _r.ymax, _r.xmax, _r.ymax, _r.xmax, 
				_r.ymin, _r.xmin, _r.ymin)),
			('c4B/static', 
				(self._color.rB, self._color.gB, self._color.bB, 
					self._color.aB) * 4)
		)
		
	def destroy(self):
		super(CDrawable, self).destroy()
		self._vertex_list.delete()
		
	def draw(self, render_state):
		render_state.update_cxform()
		render_state.set_enable_texture(False)
		self._vertex_list.draw(GL_QUADS)
		render_state.set_enable_texture(True)
