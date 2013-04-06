import collections
from lm.util import lm_shader
from lm.type import lm_type_color

from pyglet.gl import *

class CObj(object):

	def __init__(self):
		self._texture = None
		self._shader = lm_shader.cxform_shader
		self._color_stack = collections.deque()
		self._matrix_stack = collections.deque()
		
	def begin(self):
		self._shader.bind()
		self._shader.uniformi("sampler", 0)
		self._shader.uniformi("use_texture", 1)
		self._use_texture = True
		self._color_stack.append((lm_type_color.null_cadd, lm_type_color.null_cmul))
		self._is_color_dirty = True		
		
	def set_enable_texture(self, flag):
		if flag != self._use_texture:
			self._use_texture = flag
			self._shader.uniformi("use_texture", int(flag))
		
	def push_cxform(self, cadd, cmul):
		cadd = cadd or lm_type_color.null_cadd
		cmul = cmul or lm_type_color.null_cmul
		oadd, omul = self._color_stack[-1]
		self._color_stack.append((cadd*omul+oadd, cmul*omul))
		self._is_color_dirty = True
#
#		nadd, nmul = self._color_stack[-1]		
#		print "Push Cxform:"
#		print "Old\n\t", oadd, omul
#		print "New\n\t", cadd, cmul
#		print "Mix\n\t", nadd, nmul
#		print
		
	def pop_cxform(self):
		self._color_stack.pop()
		self._is_color_dirty = True
		
	def update_cxform(self):
		if not self._color_stack \
			or not self._is_color_dirty:
			return
			
		cadd, cmul = self._color_stack[-1]
		self._shader.uniformf("color_add", cadd.r, cadd.g, cadd.b, cadd.a)
		self._shader.uniformf("color_mul", cmul.r, cmul.g, cmul.b, cmul.a)
		self._is_color_dirty = False
		
#		print "cxform updated!"
#		print cadd
#		print cmul
		
	def push_matrix(self, matrix):
		self._matrix_stack.append(matrix)
		if matrix:
			matrix.set()
		
	def pop_matrix(self):
		matrix = self._matrix_stack.pop()
		if matrix:
			matrix.unset()
		
	def draw_image(self, vertex_list):
		self.update_cxform()
		vertex_list.draw(GL_QUADS)
		
	def draw_solid(self, vertex_list):
		self.update_cxform()
		self.set_enable_texture(False)
		vertex_list.draw(GL_QUADS)
		self.set_enable_texture(True)
			
	def end(self):
		self._shader.unbind()
		self._texture = None
		self._color_stack.clear()