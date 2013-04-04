import collections
from lm.util import lm_shader
from lm.type import lm_type_color


class CObj(object):

	def __init__(self):
		self._texture = None
		self._shader = lm_shader.cxform_shader
		self._color_stack = collections.deque()
		
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
		
	def end(self):
		self._shader.unbind()
		self._texture = None
		self._color_stack.clear()