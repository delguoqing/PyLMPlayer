import collections
from lm.util import lm_shader
from lm.type import lm_type_color
from lm.type import lm_type_blend_mode

from pyglet.gl import *

class CObj(object):

	def __init__(self):
		self._texture = None
		self._shader = lm_shader.cxform_shader
		self._color_stack = collections.deque()
		self._matrix_stack = collections.deque()
		self._color_pool = collections.deque()
		
	def _get_cached_color(self):
		if self._color_pool:
			return self._color_pool.pop()
		return lm_type_color.CType(0.0, 0.0, 0.0, 0.0)
		
	def begin(self):
		self._shader.bind()
		self._shader.uniformi("sampler", 0)
		self._shader.uniformi("use_texture", 1)
		self._use_texture = True
		self._color_stack.append((lm_type_color.null_cadd, lm_type_color.null_cmul))
		self._is_color_dirty = True
		self._empty_blend_mode_cnt = []		
		self._blend_mode_stack = collections.deque()		
		self._last_blend_mode = lm_type_blend_mode.null_blend
		
	def set_enable_texture(self, flag):
		if flag != self._use_texture:
			self._use_texture = flag
			self._shader.uniformi("use_texture", int(flag))
		
	def push_cxform(self, cadd, cmul):
		cadd = cadd or lm_type_color.null_cadd
		cmul = cmul or lm_type_color.null_cmul
		oadd, omul = self._color_stack[-1]
		
		new_cadd = self._get_cached_color()
		new_cmul = self._get_cached_color()
		
		cadd.mul(omul, new_cadd)
		new_cadd.add(oadd, new_cadd)
		
		cmul.mul(omul, new_cmul)
		
		self._color_stack.append((new_cadd, new_cmul))
		self._is_color_dirty = True
		
	def pop_cxform(self):
		cadd, cmul = self._color_stack.pop()
		self._color_pool.append(cadd)
		self._color_pool.append(cmul)		
		self._is_color_dirty = True

	def update_blend_mode(self):
		if not self._blend_mode_stack:
			return
		top = self._blend_mode_stack[-1]
		if self._last_blend_mode == top:
			return
		self._last_blend_mode = top
		top.set()
		
	def update_cxform(self):
		if not self._color_stack \
			or not self._is_color_dirty:
			return
			
		cadd, cmul = self._color_stack[-1]
		self._shader.uniformf("color_add", cadd.r, cadd.g, cadd.b, cadd.a)
		self._shader.uniformf("color_mul", cmul.r, cmul.g, cmul.b, cmul.a)
		self._is_color_dirty = False
		
	def push_matrix(self, matrix):
		self._matrix_stack.append(matrix)
		if matrix:
			matrix.set()
		
	def pop_matrix(self):
		matrix = self._matrix_stack.pop()
		if matrix:
			matrix.unset()
		
	def push_blend_mode(self, blend_mode):
		if blend_mode or not self._blend_mode_stack:
			if not blend_mode: blend_mode = lm_type_blend_mode.null_blend
			self._blend_mode_stack.append(blend_mode)
			self._empty_blend_mode_cnt.append(0)
		else:
			self._empty_blend_mode_cnt[-1] += 1
		
	# Assume that only one blend mode applies at the same time
	def pop_blend_mode(self):
		if self._empty_blend_mode_cnt[-1] == 0:
			self._empty_blend_mode_cnt.pop(-1)
			last = self._blend_mode_stack.pop()
		else:
			self._empty_blend_mode_cnt[-1] -= 1
			
	def draw_image(self, vertex_list):
		self.update_blend_mode()
		self.update_cxform()
		vertex_list.draw(GL_QUADS)
		
	def draw_solid(self, vertex_list):
		self.update_blend_mode()	
		self.update_cxform()
		self.set_enable_texture(False)
		vertex_list.draw(GL_QUADS)
		self.set_enable_texture(True)
			
	def end(self):
		self._shader.unbind()
		self._texture = None
		self._color_stack.clear()