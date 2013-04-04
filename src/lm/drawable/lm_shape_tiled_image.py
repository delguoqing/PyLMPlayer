import pyglet
import lm_drawable
import lm_shape_clipped_image

from lm.util import lm_shader

from pyglet.gl import *

# As far as I see, this is identical to lm_shape_clipped_image
# so....
class CDrawable(lm_shape_clipped_image.CDrawable):
	
	def _create_vertex_list(self):
		_r = self._rect
		
		_vertices = []
		_tex_coords = []
		count = 0
		for _y in xrange(_r.ymin, _r.ymax, self._texture.height):
			for _x in xrange(_r.xmin, _r.xmax, self._texture.width):

				_xmin = _x
				_xmax = _x + self._texture.width
				_ymin = _y
				_ymax = _y + self._texture.height
								
				_vertices += (_xmin, _ymax, _xmax, _ymax, _xmax, 
				_ymin, _xmin, _ymin)
				_tex_coords += self._tex_coords
				
				if _xmax > _r.xmax:
					_vertices[-4] = _vertices[-6] = _r.xmax
					_tex_coords[-6] = _tex_coords[-9] = (_r.xmax - _xmin) * 1.0 / self._texture.width
				if _ymax > _r.ymax:
					_vertices[-5] = _vertices[-7] = _r.ymax
					_tex_coords[-8] = _tex_coords[-11] = (_r.ymax - _ymin) * 1.0 / self._texture.height
				
				count += 1	
					

		self._vertex_list = pyglet.graphics.vertex_list(4 * count,
			('v2f/static', _vertices),
			('t3f/static', _tex_coords)
		)