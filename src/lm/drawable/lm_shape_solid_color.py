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
		self._group = None		
		self._create_vertex_list()
		
	def _create_vertex_list(self):
		self._vertex_list = self._batch.add(4, GL_QUADS, self._group,
				'v2i/dynamic', 
				'c4B')
						
	def refresh(self):
		_matd = self._is_mat_dirty
		_cxfd = self._is_cxform_dirty
		super(CDrawable, self).refresh()
		
		if _matd:
			_rect = self._rect
			x0, y0 = self._tot_mat.get_transformed_point(_rect.xmin, _rect.ymin)
			x1, y1 = self._tot_mat.get_transformed_point(_rect.xmax, _rect.ymin)
			x2, y2 = self._tot_mat.get_transformed_point(_rect.xmax, _rect.ymax)
			x3, y3 = self._tot_mat.get_transformed_point(_rect.xmin, _rect.ymax)
			
			self._vertex_list.vertices[:] = [x0, y0, x1, y1, x2, y2, x3, y3]
			
		if _cxfd:
			v = self._color * self._tot_cmul + self._tot_cadd
			self._vertex_list.colors[:] = [v.rB, v.gB, v.bB, v.aB] * 4

	def clear(self):
		self._vertex_list.vertices[:] = [0] * 8
		self._is_mat_dirty = True		
		
	def destroy(self):
		super(CDrawable, self).destroy()
		self._vertex_list.delete()			