import collections
import pyglet

from lm.util import lm_shader
from lm.type import lm_type_color
from lm.type import lm_type_blend_mode
from lm.type import lm_type_mat
from lm import lm_glb
from lm import lm_consts

from pyglet.gl import *


class CObj(object):

	def __init__(self):
		self._shader = lm_shader.cxform_shader
		
		self._color_stack = collections.deque()
		self._color_stack.append((lm_glb.null_cadd, lm_glb.null_cmul))		
		self._color_pool = collections.deque()
				
		self._matrix_stack = collections.deque()
		self._mat_pool = collections.deque()

		self._empty_blend_mode_cnt = []
		self._blend_mode_stack = collections.deque()

		###########################
		# Current Rendering Contex
		###########################			
		self._texture = None # active texture
		self._color_add = lm_type_color.CType(0.0, 0.0, 0.0, 0.0) # active color add
		self._blend_mode = lm_type_blend_mode.null_blend
		self._use_shader = False
		
		self._is_color_add_dirty = False
		self._is_blend_mode_dirty = False
		self._is_texture_dirty = False
		
		# vbo
		self._vertex_count = 100
		self._vertex_list = pyglet.graphics.vertex_list(self._vertex_count, 
			"v2f", "t3f", "c4f")
		self._vertex_idx = 0
		
		# statistic
		self._draw_count = 0
		self._max_depth = 0
		self._node_count = 0
		
		self._peak_draw_count = 0
		self._peak_max_depth = 0
		self._peak_node_count = 0
		
		self._is_enable_statistic = False
		self._to_enable_statistic = None
		
	def _get_cached_color(self):
		if self._color_pool:
			return self._color_pool.pop()
		return lm_type_color.CType(0.0, 0.0, 0.0, 0.0)
		
	def _get_cached_mat(self):
		if self._mat_pool:
			return self._mat_pool.pop()
		return lm_type_mat.CType()
		
	def begin(self):

		self._texture = None
		self._blend_mode = None
		self._use_shader = False
		self._color_add.zero()
		
		if self._to_enable_statistic:
			self._is_enable_statistic = self._to_enable_statistic
			self._to_enable_statistic = None
			
		if self._is_enable_statistic:
			# clear up statistic
			self._draw_count = 0
			self._max_depth = 0
			self._node_count = 0
#		print "start"

	def enable_statistic(self, loop=1):
		self._to_enable_statistic = loop
		
	def disable_statistic(self):
		self._is_enable_statistic = 0
		self._to_enable_statistic = None
		print "<====================>"
		self.print_statistic()		
		self.print_overall_statistic()
		print
		
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
#		print "push cxform %r" % new_cadd

		# do statistic A
		if self._is_enable_statistic:
			self._node_count += 1
			self._max_depth = max(self._max_depth, len(self._color_stack))
				
	def pop_cxform(self):
		cadd, cmul = self._color_stack.pop()
		self._color_pool.append(cadd)
		self._color_pool.append(cmul)

	def push_matrix(self, matrix):
		_matrix = self._get_cached_mat()
		if not self._matrix_stack:
			_matrix.copy_from(matrix)
		else:
			_matrix2 = self._matrix_stack[-1]
			_matrix.mul(_matrix2, matrix)
		self._matrix_stack.append(_matrix)
		
	def pop_matrix(self):
		mat = self._matrix_stack.pop()
		self._mat_pool.append(mat)
		
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

	def _append(self, vertices, colors, tex_coords):
		m = self._matrix_stack[-1]
		i = self._vertex_idx
		v = self._vertex_list
		n = len(vertices) / 2
		
		# append colors
		s = i * 4
		t = s + n * 4
		v.colors[s : t] = colors
		
		# append tex_coords
		s = i * 3
		t = s + n * 3
		v.tex_coords[s : t] = tex_coords
		
		# transform and append vertices
		s = i * 2
		t = s + n * 2
		for j in xrange(s, t, 2):
			x, y = vertices[j - s], vertices[j - s + 1]
			x1, y1 = m.transform_point((x, y))
			v.vertices[j], v.vertices[j + 1] = x1, y1
		
		# n vertices added
		self._vertex_idx += n
		
	def log(self, str):
		if self._is_enable_statistic:
			print str
			
	def _update_contex(self):
		if self._is_color_add_dirty:
			use_shader = (self._color_add != lm_glb.null_cadd)
			if self._use_shader != use_shader:
				if use_shader:
					self._shader.bind()
				else:
					self._shader.unbind()
				self._use_shader = use_shader
			if self._use_shader:
				self._shader.uniformf("color_add", self._color_add.r, self._color_add.g, self._color_add.b, self._color_add.a)
			self._is_color_add_dirty = False
			
			# Debug
			self.log("update color add (%.2f, %.2f, %.2f, %.2f)" % (self._color_add.r, self._color_add.g, self._color_add.b, self._color_add.a))
		
		if self._is_texture_dirty:
			texture = self._texture
			glEnable(texture.target)
			glBindTexture(texture.target, texture.id)
			
			if self._use_shader:
				self._shader.uniformi("sampler", 0)
			self._is_texture_dirty = False
			
			# Debug
			self.log("update texture")
				
		if self._is_blend_mode_dirty:	
			self._blend_mode.set()
			self._is_blend_mode_dirty = False
			
			self.log("update blend mode")
				
	def _flush(self):
				
		if self._vertex_idx > 0:
			
			self._update_contex()
			
			self.log("batch draw %d" % ((self._vertex_idx + 1) / 4))
			empty_cnt = (self._vertex_count - self._vertex_idx)
			if empty_cnt:
				self._vertex_list.vertices[self._vertex_idx*2: ] = [0.0] * (empty_cnt * 2)
			self._vertex_list.draw(GL_QUADS)
			self._vertex_idx = 0
		
	def draw_image(self, texture, vertex_list, tex_coords):
		texture = texture
		blend_mode = self._blend_mode_stack[-1]
		color_add, color_mul = self._color_stack[-1]
		matrix = self._matrix_stack[-1]

		_is_texture_dirty = self._texture is None or (self._texture.id != self._texture.id)
		_is_blend_mode_dirty = (blend_mode != self._blend_mode)
		_is_color_add_dirty = (self._color_add != color_add)
					
		# if render contex changes, flush buffer, and set up new contex
		n = len(vertex_list) / 2
		if _is_texture_dirty\
			or _is_blend_mode_dirty \
			or _is_color_add_dirty \
			or self._vertex_idx + n > self._vertex_count:
			
			self._flush()
			
			self._is_texture_dirty = _is_texture_dirty
			self._is_color_add_dirty = _is_color_add_dirty
			self._is_blend_mode_dirty = _is_blend_mode_dirty

			self._texture = texture
			self._blend_mode = blend_mode
			self._color_add.copy_from(color_add)
			
		# any way, append vertex data
		colors = [color_mul.r, color_mul.g, color_mul.b, color_mul.a] * n
		self._append(vertex_list, colors, tex_coords)	
		
		# do statistic B
		if self._is_enable_statistic:
			self._draw_count += 1
					
	def end(self):

		# flush buffer anyway
		self._flush()
				
		# do statistic D
		# compare peak statistc
		if self._is_enable_statistic:
			self._peak_node_count = max(self._peak_node_count,self._node_count)
			self._peak_draw_count = max(self._peak_draw_count,self._draw_count)
			self._peak_max_depth = max(self._peak_max_depth, self._max_depth)
			self._is_enable_statistic -= 1
			
			if not self._is_enable_statistic:
				self.disable_statistic()
		
		if self._use_shader:
			self._shader.unbind()
#		print "end"
		
	def print_statistic(self):
		print "Render Statistic:"
		print "\t%d nodes visited" % self._node_count
		print "\t%d primitives draw" % self._draw_count
		print "\tmax recursive depth: %d" % self._max_depth
		
	def print_overall_statistic(self):
		print "Render Statistic Peak:"
		print "\t%d nodes visited" % self._peak_node_count
		print "\t%d primitives draw" % self._peak_draw_count
		print "\tmax recursive depth: %d" % self._peak_max_depth		