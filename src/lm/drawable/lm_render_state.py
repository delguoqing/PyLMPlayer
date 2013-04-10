import collections
from lm.util import lm_shader
from lm.type import lm_type_color
from lm.type import lm_type_blend_mode
from lm import lm_glb

from pyglet.gl import *

class CObj(object):

	def __init__(self):
		self._texture = None
		self._shader = lm_shader.cxform_shader
		self._color_stack = collections.deque()
		self._matrix_stack = collections.deque()
		self._color_pool = collections.deque()
		
		# statistic
		self._draw_count = 0
		self._max_depth = 0
		self._node_count = 0
		
		self._peak_draw_count = 0
		self._peak_max_depth = 0
		self._peak_node_count = 0
		
	def _get_cached_color(self):
		if self._color_pool:
			return self._color_pool.pop()
		return lm_type_color.CType(0.0, 0.0, 0.0, 0.0)
		
	def begin(self):
		self._shader.bind()
		self._shader.uniformi("sampler", 0)
		self._shader.uniformi("use_texture", 1)
		self._use_texture = True
		self._color_stack.append((lm_glb.null_cadd, lm_glb.null_cmul))
		self._is_color_dirty = True
		self._empty_blend_mode_cnt = []		
		self._blend_mode_stack = collections.deque()		
		self._last_blend_mode = lm_type_blend_mode.null_blend
		
		# clear up statistic
#		self._draw_count = 0
#		self._max_depth = 0
#		self._node_count = 0
		
	def set_enable_texture(self, flag):
		if flag != self._use_texture:
			self._use_texture = flag
			self._shader.uniformi("use_texture", int(flag))
		
	def push_cxform(self, cadd, cmul):
		cadd = cadd or lm_glb.null_cadd
		cmul = cmul or lm_glb.null_cmul
		oadd, omul = self._color_stack[-1]
		
		new_cadd = self._get_cached_color()
		new_cmul = self._get_cached_color()
				
		new_cadd.mul(cadd, omul)
		new_cadd.add(new_cadd, oadd)
		new_cmul.mul(cmul, omul)
		
		self._color_stack.append((new_cadd, new_cmul))
		self._is_color_dirty = True

		# do statistic A
#		self._node_count += 1
#		self._max_depth = max(self._max_depth, len(self._color_stack))
				
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
		
		# do statistic B
#		self._draw_count += 1		
		
	def draw_solid(self, vertex_list):
		self.update_blend_mode()	
		self.update_cxform()
		self.set_enable_texture(False)
		vertex_list.draw(GL_QUADS)
		self.set_enable_texture(True)

		# do statistic C
#		self._draw_count += 1		
					
	def end(self):
		self._shader.unbind()
		self._texture = None
		self._color_stack.clear()
		
		# do statistic D
		# compare peak statistc
#		self._peak_node_count = max(self._peak_node_count, self._node_count)
#		self._peak_draw_count = max(self._peak_draw_count, self._draw_count)
#		self._peak_max_depth = max(self._peak_max_depth, self._max_depth)
						
		
	def print_statistic(self):
		print "Render Statistic:"
		print "\t%d nodes visited" % self._node_count
		print "\t%d primitive draw" % self._draw_count
		print "\tmax recursive depth: %d" % self._max_depth
		
	def print_overall_statistic(self):
		print "Render Statistic Peak:"
		print "\t%d nodes visited" % self._peak_node_count
		print "\t%d primitive draw" % self._peak_draw_count
		print "\tmax recursive depth: %d" % self._peak_max_depth		