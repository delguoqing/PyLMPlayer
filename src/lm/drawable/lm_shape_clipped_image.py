import pyglet
import lm_drawable
from lm.util import lm_shader
from lm.type import lm_type_rect
from lm.type import lm_type_color

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, texture, rect, parent=None):
		super(CDrawable, self).__init__(parent)
		self._texture = texture
		self._is_mat_dirty = True
		self._is_cxform_dirty = True
		self._rect = rect
		self._create_vertex_list()
		
	def _create_vertex_list(self):
		self._vertex_list = self._batch.add(4, GL_QUADS, self._group,
				'v2i/dynamic', 
				'c4B', ('t2B', (0, 0, 1, 0, 1, 1, 0, 1)))
				
	def refresh(self):
		_matd = self._is_mat_dirty
		_cxfd = self._is_cxform_dirty
		super(CDrawable, self).refresh()
		
		if _matd:
			self._vertex_list.vertices[:] = []
		if _cxfd:
			self._vertex_list.colors[:] = []