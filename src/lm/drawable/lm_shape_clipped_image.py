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
		
		scale_tx = _r.width * 1.0 / self._texture.width
		scale_ty = _r.height * 1.0 / self._texture.height

		_tex_coords = None
		if scale_tx != 1.0:
			_tex_coords = _tex_coords or list(self._tex_coords)
			_tx_len = _tex_coords[-9] - _tex_coords[-3]
			_tex_coords[-6] = _tex_coords[-9] = _tex_coords[-3] + _tx_len * scale_tx
		if scale_ty != 1.0:
			_tex_coords = _tex_coords or list(self._tex_coords)
			_ty_len = _tex_coords[-8] - _tex_coords[-5]
			_tex_coords[-8] = _tex_coords[-11] = _tex_coords[-5] + _ty_len * scale_ty
			
		_tex_coords = _tex_coords or self._tex_coords
			
		self._vertex_list = pyglet.graphics.vertex_list(4,
			('v2f/static', (_r.xmin, _r.ymax, _r.xmax, _r.ymax, _r.xmax, 
				_r.ymin, _r.xmin, _r.ymin)),
			('t3f/static', _tex_coords)
		)
		
	def draw(self, render_state):
		render_state.draw_image(self._vertex_list)
		
	def destroy(self):
		super(CDrawable, self).destroy()
		self._vertex_list.delete()