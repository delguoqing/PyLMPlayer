cimport c_opengl as gl
from libcpp.vector cimport vector
from libcpp.stack cimport stack
from libc.stdlib cimport malloc, free
	
cdef struct CMat:
	float t0, t1, s0, s1, r0, r1
cdef struct CColor:
	float r, g, b, a
cdef struct CPos:
	float x, y
cdef struct CCoords:
	float x0, y0, x1, y1, x2, y2, x3, y3
cdef color_add(CColor *out, CColor *a, CColor *b):
	out.r = a.r + b.r
	out.g = a.g + b.g
	out.b = a.b + b.b
	out.a = a.a + b.a
cdef color_mul(CColor *out, CColor *a, CColor *b):
	out.r = a.r * b.r
	out.g = a.g * b.g
	out.b = a.b * b.b
	out.a = a.a * b.a
cdef mat_mul(CMat *out, CMat *a, CMat *b):
	out.s0 = a.s0 * b.s0 + a.r1 * b.r0
	out.s1 = a.r0 * b.r1 + a.s1 * b.s1
	out.t0 = a.s0 * b.t0 + a.r1 * b.t1 + a.t0
	out.t1 = a.r0 * b.t0 + a.s1 * b.t1 + a.t1
	out.r0 = a.r0 * b.s0 + a.s1 * b.r0
	out.r1 = a.s0 * b.r1 + a.r1 * b.s1
cdef transform_coords(CCoords *out, CCoords *a, CMat *m):
	out.x0 = a.x0 * m.s0 + a.y0 * m.r1 + m.t0
	out.y0 = a.x0 + m.r0 + a.y0 * m.s1 + m.t1
	out.x1 = a.x1 * m.s0 + a.y1 * m.r1 + m.t0
	out.y1 = a.x1 + m.r0 + a.y1 * m.s1 + m.t1
	out.x2 = a.x2 * m.s0 + a.y2 * m.r1 + m.t0
	out.y2 = a.x2 + m.r0 + a.y2 * m.s1 + m.t1
	out.x3 = a.x3 * m.s0 + a.y3 * m.r1 + m.t0
	out.y3 = a.x3 + m.r0 + a.y3 * m.s1 + m.t1	

cdef class CRenderer:
	
	cdef vector[CMat*] vec_mat
	cdef vector[CPos*] vec_pos
	cdef vector[CColor*] vec_color
	cdef vector[CCoords*] vec_coords
	
	cdef int _tex_tgt
	cdef int _tex_id
	cdef int _blend_mode
	
	cdef stack[CColor*] stk_cadd
	cdef stack[CColor*] stk_cmul
	cdef stack[CMat *] stk_mat
	
	def __cinit__(self):
		self._tex_tag = -1
		self._tex_id = -1
		self._blend_mode = -1
	
	def begin(self):
		gl.glEnable(gl.GL_COLOR_SUM_EXT)
	
		self._tex_tgt = -1	
		self._tex_id = -1
		self._blend_mode = -1
		
	def push_state(self, int cadd_idx, int cmul_idx, int mat_idx, int blend_mode_idx):
		pass
	
	def pop_state(self):
		pass
	
#	
#	def push_cxform(self, cadd, cmul):
#		cadd = cadd or lm_glb.null_cadd
#		cmul = cmul or lm_glb.null_cmul
#		oadd, omul = self._color_stack[-1]
#		
#		new_cadd = self._get_cached_color()
#		new_cmul = self._get_cached_color()
#				
#		new_cadd.mul(cadd, omul)
#		new_cadd.add(new_cadd, oadd)
#		new_cmul.mul(cmul, omul)
#		
#		self._color_stack.append((new_cadd, new_cmul))
#				
#	def pop_cxform(self):
#		cadd, cmul = self._color_stack.pop()
#		self._color_pool.append(cadd)
#		self._color_pool.append(cmul)
#
#	def push_matrix(self, matrix):
#		_matrix = self._get_cached_mat()
#		if not self._matrix_stack:
#			_matrix.copy_from(matrix)
#		else:
#			_matrix2 = self._matrix_stack[-1]
#			_matrix.mul(_matrix2, matrix)
#		self._matrix_stack.append(_matrix)
#		
#	def pop_matrix(self):
#		mat = self._matrix_stack.pop()
#		self._mat_pool.append(mat)
#		
#	def push_blend_mode(self, blend_mode):
#		if blend_mode or not self._blend_mode_stack:
#			if not blend_mode: blend_mode = lm_type_blend_mode.null_blend
#			self._blend_mode_stack.append(blend_mode)
#			self._empty_blend_mode_cnt.append(0)
#		else:
#			self._empty_blend_mode_cnt[-1] += 1
#		
#	# Assume that only one blend mode applies at the same time
#	def pop_blend_mode(self):
#		if self._empty_blend_mode_cnt[-1] == 0:
#			self._empty_blend_mode_cnt.pop(-1)
#			last = self._blend_mode_stack.pop()
#		else:
#			self._empty_blend_mode_cnt[-1] -= 1
#
#	def _append(self, vertices, colors, tex_coords, secondary_colors):
#		m = self._matrix_stack[-1]
#		i = self._vertex_idx
#		v = self._vertex_list
#		n = len(vertices) / 2
#		
##		self.log("New vertices data:")
#				
#		# append colors
#		s = i * 4
#		t = s + n * 4
#		v.colors[s : t] = colors
#		
##		self.log("\tcolor = (%.2f, %.2f, %.2f, %.2f)" % tuple(v.colors[s:s+4]))
#		
#		# append secondary colors
#		s = i * 3
#		t = s + n * 3
#		v.secondary_colors[s : t] = secondary_colors
#		
#		mask = self._mask_rect
#		if not mask:
#			# append tex_coords
#			s = i * 2
#			t = s + n * 2
#			v.tex_coords[s : t] = tex_coords
#
#			# transform and append vertices
#			for j in xrange(s, t, 2):
#				x, y = vertices[j - s], vertices[j - s + 1]
#				x1, y1 = m.transform_point((x, y))
#				v.vertices[j], v.vertices[j + 1] = x1, y1
#				
#		else:
#			s = i * 2
#			t = s + n * 2
#			for j in xrange(s, t, 8):
#				x0, y0, x1, y1, x2, y2, x3, y3 = vertices[j - s: j - s + 8]
#				u0, v0, u1, v1, u2, v2, u3, v3 = tex_coords[j - s: j - s + 8]
#				
#				x0, y0 = m.transform_point((x0, y0))
#				x1, y1 = m.transform_point((x1, y1))
#				x2, y2 = m.transform_point((x2, y2))
#				x3, y3 = m.transform_point((x3, y3))
#				
#				stride_u = abs(u0 - u1 or u1 - u2)
#				stride_v = abs(v0 - v1 or v1 - v2)
#				stride_x = abs(x0 - x1 or x1 - x2)
#				stride_y = abs(y0 - y1 or y1 - y2)
#				
#				_fix_x = stride_u / stride_x
#				_fix_y = stride_v / stride_y
#				
#				if x0 < mask[0]: u0 += (mask[0] - x0) * _fix_x; x0 = mask[0]
#				elif x0 > mask[1]: u0 -= (x0 - mask[1]) * _fix_x; x0 = mask[1]
#				if y0 < mask[2]: v0 -= (mask[2] - y0) * _fix_y; y0 = mask[2]
#				elif y0 > mask[3]: v0 += (y0 - mask[3]) * _fix_y; y0 = mask[3]
#
#				if x1 < mask[0]: u1 += (mask[0] - x1) * _fix_x; x1 = mask[0]
#				elif x1 > mask[1]: u1 -= (x1 - mask[1]) * _fix_x; x1 = mask[1]
#				if y1 < mask[2]: v1 -= (mask[2] - y1) * _fix_y; y1 = mask[2]
#				elif y1 > mask[3]: v1 += (y1 - mask[3]) * _fix_y; y1 = mask[3]
#				
#				if x2 < mask[0]: u2 += (mask[0] - x2) * _fix_x; x2 = mask[0]
#				elif x2 > mask[1]: u2 -= (x2 - mask[1]) * _fix_x; x2 = mask[1]
#				if y2 < mask[2]: v2 -= (mask[2] - y2) * _fix_y; y2 = mask[2]
#				elif y2 > mask[3]: v2 += (y2 - mask[3]) * _fix_y; y2 = mask[3]
#				
#				if x3 < mask[0]: u3 += (mask[0] - x3) * _fix_x; x3 = mask[0]
#				elif x3 > mask[1]: u3 -= (x3 - mask[1]) * _fix_x; x3 = mask[1]
#				if y3 < mask[2]: v3 -= (mask[2] - y3) * _fix_y; y3 = mask[2]
#				elif y3 > mask[3]: v3 += (y3 - mask[3]) * _fix_y; y3 = mask[3]
#				
#				v.vertices[j: j+8] = (x0, y0, x1, y1, x2, y2, x3, y3)
#				v.tex_coords[j: j+8] = (u0, v0, u1, v1, u2, v2, u3, v3)
#				
#		# n vertices added
#		self._vertex_idx += n
#			
#	def _update_contex(self):
#		
#		if self._is_texture_dirty:
#			texture = self._texture
#			glEnable(texture.target)
#			glBindTexture(texture.target, texture.id)
#
#			self._is_texture_dirty = False
#			
#			# Debug
##			self.log("update texture")
#				
#		if self._is_blend_mode_dirty:	
#			self._blend_mode.set()
#			self._is_blend_mode_dirty = False
#			
##			self.log("update blend mode: %r" % self._blend_mode)
#				
#	def _flush(self):
#				
#		if self._vertex_idx > 0:
#			
#			self._update_contex()
#			
##			self.log("%d quads batched!" % (self._vertex_idx / 4))
#			
#			empty_cnt = (self._vertex_count - self._vertex_idx)
#			if empty_cnt:
#				self._vertex_list.vertices[self._vertex_idx*2: ] = [0.0] * (empty_cnt * 2)
#			self._vertex_list.draw(GL_QUADS)
##			self.log("%r" % self._vertex_list.vertices[:])
#			self._vertex_idx = 0
#		
#			# do statistic B
#			if self._is_enable_statistic:
#				self._draw_count += 1
#					
#	def draw_image(self, texture, vertex_list, tex_coords):
#		texture = texture
#		blend_mode = self._blend_mode_stack[-1]
#		color_add, color_mul = self._color_stack[-1]
#		matrix = self._matrix_stack[-1]
#
#		_is_texture_dirty = self._texture is None or (self._texture.id != texture.id)
#		_is_blend_mode_dirty = (blend_mode != self._blend_mode)
#					
#		# if render contex changes, flush buffer, and set up new contex
#		n = len(vertex_list) / 2
#		if _is_texture_dirty\
#			or _is_blend_mode_dirty \
#			or self._vertex_idx + n > self._vertex_count:
#			
#			self._flush()
#			
#			self._is_texture_dirty = _is_texture_dirty
#			self._is_blend_mode_dirty = _is_blend_mode_dirty
#
#			self._texture = texture
#			self._blend_mode = blend_mode
#			
#		# any way, append vertex data
#		colors = [color_mul.r, color_mul.g, color_mul.b, color_mul.a] * n
#		secondary_colors = [color_add.r, color_add.g, color_add.b] * n
#		self._append(vertex_list, colors, tex_coords, secondary_colors)
#					
#	def set_mask(self, drawable):
#		if not drawable:
#			self._mask_rect = None
#		else:
#
#			r = drawable._rect
#			m = self._matrix_stack[-1]
#			xmin, ymin = m.transform_point((r.xmin, r.ymin))
#			xmax, ymax = m.transform_point((r.xmax, r.ymax))
#			self._mask_rect = xmin, xmax, ymin, ymax
#		
#	def end(self):
#
#		# flush buffer anyway
#		self._flush()
#			

	####################################
	# Preloading all rendering data
	####################################
	def reg_pos(self, float x, float y):
		cdef CPos *pos = <CPos *>malloc(sizeof(CPos))
		pos.x = x
		pos.y = y
		self.vec_pos.push_back(pos)
		return self.vec_pos.size()
	
	def reg_color(self, float r, float g, float b, float a):
		cdef CColor *color = <CColor *>malloc(sizeof(CColor))
		color.r = r
		color.g = g
		color.b = b
		color.a = a
		self.vec_color.push_back(color)
		return self.vec_color.size()
	
	def reg_mat(self, float t0, float t1, float s0, float s1, float r0, float r1):
		cdef CMat *mat = <CMat *>malloc(sizeof(CMat))
		mat.t0 = t0
		mat.t1 = t1
		mat.s0 = s0
		mat.s1 = s1
		mat.r0 = r0
		mat.r1 = r1		
		self.vec_mat.push_back(mat)
		return self.vec_mat.size()
	
	def reg_coords(self, float x0, float y0, float x1, float y1, float x2,
						   float y2, float x3, float y3):
		cdef CCoords *coords = <CCoords *>malloc(sizeof(CCoords))
		coords.x0 = x0
		coords.y0 = y0
		coords.x1 = x1
		coords.y1 = y1
		coords.x2 = x2
		coords.y2 = y2
		coords.x3 = x3
		coords.y3 = y3
		self.vec_coords.push_back(coords)
		return self.vec_coords.size()
	