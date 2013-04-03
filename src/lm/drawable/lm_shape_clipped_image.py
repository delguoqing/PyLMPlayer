import pyglet
import lm_drawable
import lm_drawable_group
from lm.util import lm_shader
from lm.type import lm_type_rect
from lm.type import lm_type_color

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, texture, rect, tex_coords, inst_id, depth, parent=None):
		super(CDrawable, self).__init__(inst_id, depth, parent)
		self._texture = texture
		self._rect = rect
		self._tex_coords = tex_coords
		self._create_vertex_list()
		
	def _create_vertex_list(self):
		_r = self._rect
		self._vertex_list = pyglet.graphics.vertex_list(4,
			('v2f/static', (_r.xmin, _r.ymax, _r.xmax, _r.ymax, _r.xmax, 
				_r.ymin, _r.xmin, _r.ymin)),
			('t3f/static', self._tex_coords)
		)
		
	def draw(self, render_state):
		self._vertex_list.draw(GL_QUADS)
		
	def destroy(self):
		super(CDrawable, self).destroy()
		self._vertex_list.delete()