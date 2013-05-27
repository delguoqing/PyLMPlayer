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
		self._blend_mode = lm_type_blend_mode.null_blend
		
		self._is_blend_mode_dirty = False
		self._is_texture_dirty = False
		
		# vbo
		self._vertex_count = 100
		self._vertex_list = pyglet.graphics.vertex_list(self._vertex_count, 
			"v2f", "t2f", "c4f", "s3f")
		self._vertex_idx = 0

		# mask
		self._mask_rect = None
		self.time = 0
		
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

		glEnable(GL_COLOR_SUM)
		self._texture = None
		self._blend_mode = None
		
		if self._to_enable_statistic:
			self._is_enable_statistic = self._to_enable_statistic
			self._to_enable_statistic = None
			
		if self._is_enable_statistic:
			# clear up statistic
			self._draw_count = 0
			self._max_depth = 0
			self._node_count = 0
			
#		self.log("==== render BEG ====")

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

	def _append(self, vertices, colors, tex_coords, secondary_colors):
		m = self._matrix_stack[-1]
		i = self._vertex_idx
		v = self._vertex_list
		n = len(vertices) / 2
		
#		self.log("New vertices data:")
				
		# append colors
		s = i * 4
		t = s + n * 4
		v.colors[s : t] = colors
		
#		self.log("\tcolor = (%.2f, %.2f, %.2f, %.2f)" % tuple(v.colors[s:s+4]))
		
		# append secondary colors
		s = i * 3
		t = s + n * 3
		v.secondary_colors[s : t] = secondary_colors
		
		mask = self._mask_rect
		if not mask:
			# append tex_coords
			s = i * 2
			t = s + n * 2
			v.tex_coords[s : t] = tex_coords

			# transform and append vertices
			for j in xrange(s, t, 2):
				x, y = vertices[j - s], vertices[j - s + 1]
				x1, y1 = m.transform_point((x, y))
				v.vertices[j], v.vertices[j + 1] = x1, y1
				
		else:
			s = i * 2
			t = s + n * 2
			for j in xrange(s, t, 8):
				x0, y0, x1, y1, x2, y2, x3, y3 = vertices[j - s: j - s + 8]
				u0, v0, u1, v1, u2, v2, u3, v3 = tex_coords[j - s: j - s + 8]
				
				x0, y0 = m.transform_point((x0, y0))
				x1, y1 = m.transform_point((x1, y1))
				x2, y2 = m.transform_point((x2, y2))
				x3, y3 = m.transform_point((x3, y3))
				
				stride_u = abs(u0 - u1 or u1 - u2)
				stride_v = abs(v0 - v1 or v1 - v2)
				stride_x = abs(x0 - x1 or x1 - x2)
				stride_y = abs(y0 - y1 or y1 - y2)
				
				_fix_x = stride_u / stride_x
				_fix_y = stride_v / stride_y
				
				if x0 < mask[0]: u0 += (mask[0] - x0) * _fix_x; x0 = mask[0]
				elif x0 > mask[1]: u0 -= (x0 - mask[1]) * _fix_x; x0 = mask[1]
				if y0 < mask[2]: v0 -= (mask[2] - y0) * _fix_y; y0 = mask[2]
				elif y0 > mask[3]: v0 += (y0 - mask[3]) * _fix_y; y0 = mask[3]

				if x1 < mask[0]: u1 += (mask[0] - x1) * _fix_x; x1 = mask[0]
				elif x1 > mask[1]: u1 -= (x1 - mask[1]) * _fix_x; x1 = mask[1]
				if y1 < mask[2]: v1 -= (mask[2] - y1) * _fix_y; y1 = mask[2]
				elif y1 > mask[3]: v1 += (y1 - mask[3]) * _fix_y; y1 = mask[3]
				
				if x2 < mask[0]: u2 += (mask[0] - x2) * _fix_x; x2 = mask[0]
				elif x2 > mask[1]: u2 -= (x2 - mask[1]) * _fix_x; x2 = mask[1]
				if y2 < mask[2]: v2 -= (mask[2] - y2) * _fix_y; y2 = mask[2]
				elif y2 > mask[3]: v2 += (y2 - mask[3]) * _fix_y; y2 = mask[3]
				
				if x3 < mask[0]: u3 += (mask[0] - x3) * _fix_x; x3 = mask[0]
				elif x3 > mask[1]: u3 -= (x3 - mask[1]) * _fix_x; x3 = mask[1]
				if y3 < mask[2]: v3 -= (mask[2] - y3) * _fix_y; y3 = mask[2]
				elif y3 > mask[3]: v3 += (y3 - mask[3]) * _fix_y; y3 = mask[3]
				
				v.vertices[j: j+8] = (x0, y0, x1, y1, x2, y2, x3, y3)
				v.tex_coords[j: j+8] = (u0, v0, u1, v1, u2, v2, u3, v3)
				
		# n vertices added
		self._vertex_idx += n
		
	def log(self, str):
		if self._is_enable_statistic:
			print str
			
	def _update_contex(self):
		
		if self._is_texture_dirty:
			texture = self._texture
			glEnable(texture.target)
			glBindTexture(texture.target, texture.id)

			self._is_texture_dirty = False
			
			# Debug
#			self.log("update texture")
				
		if self._is_blend_mode_dirty:	
			self._blend_mode.set()
			self._is_blend_mode_dirty = False
			
#			self.log("update blend mode: %r" % self._blend_mode)
				
	def _flush(self):
				
		if self._vertex_idx > 0:
			
			self._update_contex()
			
#			self.log("%d quads batched!" % (self._vertex_idx / 4))
			
			empty_cnt = (self._vertex_count - self._vertex_idx)
			if empty_cnt:
				self._vertex_list.vertices[self._vertex_idx*2: ] = [0.0] * (empty_cnt * 2)
			self._vertex_list.draw(GL_QUADS)
#			self.log("%r" % self._vertex_list.vertices[:])
			self._vertex_idx = 0
		
	def draw_image(self, texture, vertex_list, tex_coords):
		texture = texture
		blend_mode = self._blend_mode_stack[-1]
		color_add, color_mul = self._color_stack[-1]
		matrix = self._matrix_stack[-1]

		_is_texture_dirty = self._texture is None or (self._texture.id != texture.id)
		_is_blend_mode_dirty = (blend_mode != self._blend_mode)
					
		# if render contex changes, flush buffer, and set up new contex
		n = len(vertex_list) / 2
		if _is_texture_dirty\
			or _is_blend_mode_dirty \
			or self._vertex_idx + n > self._vertex_count:
			
			self._flush()
			
			self._is_texture_dirty = _is_texture_dirty
			self._is_blend_mode_dirty = _is_blend_mode_dirty

			self._texture = texture
			self._blend_mode = blend_mode
			
		# any way, append vertex data
		colors = [color_mul.r, color_mul.g, color_mul.b, color_mul.a] * n
		secondary_colors = [color_add.r, color_add.g, color_add.b] * n
		self._append(vertex_list, colors, tex_coords, secondary_colors)
		
		# do statistic B
		if self._is_enable_statistic:
			self._draw_count += 1
					
	def set_mask(self, drawable):
		if not drawable:
			self._mask_rect = None
		else:

			r = drawable._rect
			m = self._matrix_stack[-1]
			xmin, ymin = m.transform_point((r.xmin, r.ymin))
			xmax, ymax = m.transform_point((r.xmax, r.ymax))
			self._mask_rect = xmin, xmax, ymin, ymax
		
	def end(self):

		# flush buffer anyway
		self._flush()
			
#		self.log("==== render END ====")
		
		# do statistic D
		# compare peak statistc
		if self._is_enable_statistic:
			self._peak_node_count = max(self._peak_node_count,self._node_count)
			self._peak_draw_count = max(self._peak_draw_count,self._draw_count)
			self._peak_max_depth = max(self._peak_max_depth, self._max_depth)
			self._is_enable_statistic -= 1
			
			if not self._is_enable_statistic:
				self.disable_statistic()
						
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