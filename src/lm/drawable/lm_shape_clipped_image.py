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
#		self._group = lm_drawable_group.CGroup(self._texture, 770, 771, self._abs_depth)
		self._group = pyglet.sprite.SpriteGroup(self._texture, 770, 771, parent=None)
		self._create_vertex_list()
		
	def _create_vertex_list(self):
		self._vertex_list = self._batch.add(4, GL_QUADS, self._group,
				'v2i/dynamic', 
				'c4B', ('t3f', self._tex_coords))
					
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
			
			self._vertex_list.vertices[:] = [x3, y3, x2, y2, x1, y1, x0, y0]
			
#			print self._tot_mat
#			print x0, y0, x1, y1, x2, y2, x3, y3
			
		if _cxfd:
			_c = self._tot_cmul
			# Ignore color add a.t.m
			self._vertex_list.colors[:] = [_c.rB, _c.gB, _c.bB, _c.aB] * 4
			
#			print _c.rB, _c.gB, _c.bB, _c.aB

			
	def clear(self):
		self._vertex_list.vertices[:] = [0] * 8
#		print "cleared?"
		self._is_mat_dirty = True
		
	def destroy(self):
		super(CDrawable, self).destroy()
		self._vertex_list.delete()