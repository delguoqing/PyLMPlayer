import pyglet
import lm_drawable
from lm.util import lm_shader
from lm.type import lm_type_color

from pyglet.gl import *

class CDrawable(lm_drawable.CDrawable):
	
	def __init__(self, color, rect, parent=None):
		super(CDrawable, self).__init__(parent)
		self._color = color
		self._rect = rect
		
		self._vertex_list = self._batch.
		
	def refresh(self):
		_matd = self._is_mat_dirty
		_cxfd = self._is_cxform_dirty
		super(CDrawable, self).refresh()
		
		if _matd:
			self._vertex_list.vertices[:] = []
		if _cxfd:
			v = self._color * self._tot_cmul + self._tot_cadd
			self._vertex_list.colors[:] = [v.rB, v.gB, v.bB, v.aB] * 4