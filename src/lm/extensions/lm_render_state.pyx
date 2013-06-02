cimport c_opengl as gl
from libcpp.vector cimport vector
from libcpp.stack cimport stack
from libc.stdlib cimport malloc, free
from memory cimport memset
	
cdef struct CVertexData:
	float x, y
	float u, v
	unsigned color
	unsigned secondary_color
	float padding[2]
cdef struct CRect:
	float xmin, ymin, xmax, ymax
cdef struct CMat:
	float t0, t1, s0, s1, r0, r1
cdef struct CColor:
	float r, g, b, a
cdef struct CPos:
	float x, y
cdef struct CCoords:
	float x0, y0, x1, y1, x2, y2, x3, y3
cdef void color_add(CColor *out, CColor *a, CColor *b):
	out.r = a.r + b.r
	out.g = a.g + b.g
	out.b = a.b + b.b
	out.a = a.a + b.a
cdef void color_mul(CColor *out, CColor *a, CColor *b):
	out.r = a.r * b.r
	out.g = a.g * b.g
	out.b = a.b * b.b
	out.a = a.a * b.a
cdef void mat_mul(CMat *out, CMat *a, CMat *b):
	out.s0 = a.s0 * b.s0 + a.r1 * b.r0
	out.s1 = a.r0 * b.r1 + a.s1 * b.s1
	out.t0 = a.s0 * b.t0 + a.r1 * b.t1 + a.t0
	out.t1 = a.r0 * b.t0 + a.s1 * b.t1 + a.t1
	out.r0 = a.r0 * b.s0 + a.s1 * b.r0
	out.r1 = a.s0 * b.r1 + a.r1 * b.s1
cdef void transform_coords(CCoords *out, CCoords *a, CMat *m):
	out.x0 = a.x0 * m.s0 + a.y0 * m.r1 + m.t0
	out.y0 = a.x0 + m.r0 + a.y0 * m.s1 + m.t1
	out.x1 = a.x1 * m.s0 + a.y1 * m.r1 + m.t0
	out.y1 = a.x1 + m.r0 + a.y1 * m.s1 + m.t1
	out.x2 = a.x2 * m.s0 + a.y2 * m.r1 + m.t0
	out.y2 = a.x2 + m.r0 + a.y2 * m.s1 + m.t1
	out.x3 = a.x3 * m.s0 + a.y3 * m.r1 + m.t0
	out.y3 = a.x3 + m.r0 + a.y3 * m.s1 + m.t1	
cdef unsigned pack_color(CColor *color):
	cdef unsigned ret = (max(0, min(int(color.r * 255), 255)) << 24) |(max(0, min(int(color.g * 255), 255)) << 16) |(max(0, min(int(color.b * 255), 255)) << 8) | max(0, min(int(color.a * 255), 255))
	return ret

cdef class CRenderer:
	
	cdef vector[CMat*] vec_mat
	cdef vector[CPos*] vec_pos
	cdef vector[CColor*] vec_color
	cdef vector[CCoords*] vec_coords
	
	cdef int _tex_tgt
	cdef int _tex_id
	cdef int _blend_mode
	cdef int _is_blend_mode_dirty
	cdef int _is_texture_dirty	
	
	cdef stack[CColor*] stk_cadd
	cdef stack[CColor*] stk_cmul
	cdef stack[CMat*] stk_mat
	cdef stack[int] stk_blend_mode
	
	cdef stack[CColor*] cadd_pool
	cdef stack[CColor*] cmul_pool
	cdef stack[CMat*] mat_pool
	
	cdef CVertexData vbuf[1000]
	cdef int vbuf_size
	
	cdef int mask_active
	cdef CRect mask_rect
	
	def __cinit__(self):
		self._tex_tgt = -1
		self._tex_id = -1
		self._blend_mode = -1
		
	cdef void set_blend_mode(self, int idx):
		gl.Enable(gl.GL_BLEND)
		if 0 <= idx <= 2:
			gl.glBlendEquationEXT(gl.GL_FUNC_ADD)
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		elif idx == 8:
			gl.glBlendEquationEXT(gl.GL_FUNC_ADD)
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
		elif idx == 9:
			gl.glBlendEquationEXT(gl.GL_FUNC_REVERSE_SUBTRACT)
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)

	cdef CMat *get_mat(self):
		cdef CMat *mat = self.mat_pool.top()
		self.mat_pool.pop()
		return mat
	
	cdef CColor *get_cadd(self):
		cdef CColor *cadd = self.cadd_pool.top()
		self.cadd_pool.pop()
		return cadd

	cdef CColor *get_cmul(self):
		cdef CColor *cmul = self.cmul_pool.top()
		self.cmul_pool.pop()
		return cmul
	
	cdef void del_mat(self, CMat *mat):
		self.mat_pool.push(mat)
	
	cdef void del_cadd(self, CColor *color):
		self.cadd_pool.push(color)

	cdef void del_cmul(self, CColor *color):
		self.cmul_pool.push(color)
		
	def init(self):
		cdef CMat *mat
		cdef CColor *color
		
		# allocate temperary result for stacking
		cdef int MAX_DEPTH = 20
		for i in xrange(MAX_DEPTH):
			self.cadd_pool.push(<CColor *>malloc(sizeof(CColor)))
			self.cmul_pool.push(<CColor *>malloc(sizeof(CColor)))
			self.mat_pool.push(<CMat *>malloc(sizeof(CMat)))
		
		# Enable secondary color
		gl.glEnable(gl.GL_COLOR_SUM_EXT)
		gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
		gl.glEnableClientState(gl.GL_COLOR_ARRAY)
		gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
		gl.glEnableClientState(gl.GL_SECONDARY_COLOR_ARRAY)
		
		# init state stack
		mat = self.get_mat()
		mat.t0 = mat.t1 = mat.r0 = mat.r1 = 0.0
		mat.s0 = mat.s1 = 1.0
		self.stk_mat.push(mat)
		
		color = self.get_cadd()
		memset(<void *>color, 0, sizeof(CColor))
		self.stk_cadd.push(color)
		
		color = self.get_cmul()
		color.r = color.g = color.b = color.a = 1.0
		self.stk_cmul.push(color)
		
		self.stk_blend_mode.push(0)
		
		self.vbuf_size = 0
		
	def begin(self):
		self._tex_tgt = -1	
		self._tex_id = -1
		self._blend_mode = -1
		self.vbuf_size = 0
		self.mask_active = False
		self._is_texture_dirty = False
		self._is_blend_mode_dirty = False
		
	def push_state(self, int cadd_idx, int cmul_idx, int mat_idx, int blend_mode_idx):
		cdef CColor *color
		cdef CMat *mat
		
		# Pushing cxform	
		if cadd_idx < 0:
			self.stk_cadd.push(self.stk_cadd.top())
		else:
			color = self.get_cadd()
			color_mul(color, self.vec_color[cadd_idx], self.stk_cmul.top())
			color_add(color, color, self.stk_cadd.top())
			self.stk_cadd.push(color)
		if cmul_idx < 0:
			self.stk_cmul.push(self.stk_cmul.top())
		else:
			color = self.get_cmul()
			color_mul(color, self.vec_color[cmul_idx], self.stk_cmul.top())
			self.stk_cmul.push(color)
		
		# Pushing matrix
		if mat_idx < 0:
			self.stk_mat.push(self.stk_mat.top())
		else:
			mat = self.get_mat()
			mat_mul(mat, self.stk_mat.top(), self.vec_mat[mat_idx])

		self.stk_blend_mode.push(blend_mode_idx)
		
	def pop_state(self):
		cdef CColor *cadd, *cmul
		cdef CMat *mat
		cadd = self.stk_cadd.top()
		cmul = self.stk_cmul.top()
		self.stk_cadd.pop()
		self.stk_cmul.pop()
		mat = self.stk_mat.top()
		self.stk_mat.pop()
		self.stk_blend_mode.pop()
		
		if self.stk_cadd.empty() or cadd != self.stk_cadd.top():
			self.del_cadd(cadd)
		if self.stk_cmul.empty() or cmul != self.stk_cmul.top():
			self.del_cmul(cmul)
		if self.stk_mat.empty() or mat != self.stk_mat.top():
			self.del_mat(mat)
	
	def set_mask(self, coord_idx):
		cdef CCoords *coord
		cdef CMat *m
		cdef float xmin, xmax, ymin, ymax
		if coord_idx < 0:
			self.mask_active = False
		else:
			self.mask_active = True
			coord = self.vec_coords[coord_idx]
			m = self.stk_mat.top()
			if coord.x0 < coord.x2:
				xmin = coord.x0; xmax = coord.x2;
			else:
				xmin = coord.x2; xmax = coord.x0;
			if coord.y0 < coord.y2:
				ymin = coord.y0; ymax = coord.y2;
			else:
				ymin = coord.y2; ymax = coord.y0;
			self.mask_rect.xmin = xmin * m.s0 + ymin * m.r1 + m.t0
			self.mask_rect.ymin = xmin * m.r0 + ymin * m.s1 + m.t1
			self.mask_rect.xmax = xmax * m.s0 + ymax * m.r1 + m.t0
			self.mask_rect.ymax = xmax * m.r0 + ymax * m.s1 + m.t1
	
	cdef void _append(self, int coords_idx, int tex_coords_idx):
		cdef CMat *m = self.stk_mat.top()
		cdef CCoords *coord = self.vec_coords[coords_idx]
		cdef CCoords *tex_coords = self.vec_coords[tex_coords_idx]
		cdef int head = self.vbuf_size
		cdef int i
		cdef unsigned cadd = pack_color(self.stk_cadd.top())
		cdef unsigned cmul = pack_color(self.stk_cmul.top())
		cdef CCoords tmp
		cdef float stride_u, stride_v, stride_x, stride_y, _fix_x, _fix_y
		cdef float u0, v0, u1, v1, u2, v2, u3, v3

		transform_coords(&tmp, coord, m)
		u0 = tex_coords.x0
		v0 = tex_coords.y0
		u1 = tex_coords.x1
		v1 = tex_coords.y1
		u2 = tex_coords.x2
		v2 = tex_coords.y2
		u3 = tex_coords.x3
		v3 = tex_coords.y3
		
		# Fix coords if masked
		if self.mask_active:
			stride_u = max(abs(u0 - u1), abs(u1 - u2))
			stride_v = max(abs(v0 - v1), abs(v1 - v2))
			stride_x = max(abs(tmp.x0 - tmp.x1), abs(tmp.x1 - tmp.x2))
			stride_y = max(abs(tmp.y0 - tmp.y1), abs(tmp.y1 - tmp.y2))
				
			_fix_x = stride_u / stride_x
			_fix_y = stride_v / stride_y
			
			if tmp.x0 < self.mask_rect.xmin:
				u0 += (self.mask_rect.xmin - tmp.x0) * _fix_x; tmp.x0 = self.mask_rect.xmin
			elif tmp.x0 > self.mask_rect.xmax:
				u0 -= (tmp.x0 - self.mask_rect.xmax) * _fix_x; tmp.x0 = self.mask_rect.xmax
			if tmp.x1 < self.mask_rect.xmin:
				u1 += (self.mask_rect.xmin - tmp.x1) * _fix_x; tmp.x1 = self.mask_rect.xmin
			elif tmp.x1 > self.mask_rect.xmax:
				u1 -= (tmp.x1 - self.mask_rect.xmax) * _fix_x; tmp.x1 = self.mask_rect.xmax
			if tmp.x2 < self.mask_rect.xmin:
				u2 += (self.mask_rect.xmin - tmp.x2) * _fix_x; tmp.x2 = self.mask_rect.xmin
			elif tmp.x2 > self.mask_rect.xmax:
				u2 -= (tmp.x2 - self.mask_rect.xmax) * _fix_x; tmp.x2 = self.mask_rect.xmax
			if tmp.x3 < self.mask_rect.xmin:
				u3 += (self.mask_rect.xmin - tmp.x3) * _fix_x; tmp.x3 = self.mask_rect.xmin
			elif tmp.x3 > self.mask_rect.xmax:
				u3 -= (tmp.x3 - self.mask_rect.xmax) * _fix_x; tmp.x3 = self.mask_rect.xmax

			if tmp.y0 < self.mask_rect.ymin:
				v0 -= (self.mask_rect.ymin - tmp.y0) * _fix_y; tmp.y0 = self.mask_rect.ymin
			elif tmp.y0 > self.mask_rect.ymax:
				v0 += (tmp.y0 - self.mask_rect.ymax) * _fix_y; tmp.y0 = self.mask_rect.ymax
			if tmp.y1 < self.mask_rect.ymin:
				v1 -= (self.mask_rect.ymin - tmp.y1) * _fix_y; tmp.y1 = self.mask_rect.ymin
			elif tmp.y1 > self.mask_rect.ymax:
				v1 += (tmp.y1 - self.mask_rect.ymax) * _fix_y; tmp.y1 = self.mask_rect.ymax
			if tmp.y2 < self.mask_rect.ymin:
				v2 -= (self.mask_rect.ymin - tmp.y2) * _fix_y; tmp.y2 = self.mask_rect.ymin
			elif tmp.y2 > self.mask_rect.ymax:
				v2 += (tmp.y2 - self.mask_rect.ymax) * _fix_y; tmp.y2 = self.mask_rect.ymax
			if tmp.y3 < self.mask_rect.ymin:
				v3 -= (self.mask_rect.ymin - tmp.y3) * _fix_y; tmp.y3 = self.mask_rect.ymin
			elif tmp.y3 > self.mask_rect.ymax:
				v3 += (tmp.y3 - self.mask_rect.ymax) * _fix_y; tmp.y3 = self.mask_rect.ymax
				
		self.vbuf[head].x = tmp.x0
		self.vbuf[head].y = tmp.y0
		self.vbuf[head].u = u0
		self.vbuf[head].v = v0
		self.vbuf[head].color = cmul
		self.vbuf[head].secondary_color = cadd
		
		head += 1
		self.vbuf[head].x = tmp.x1
		self.vbuf[head].y = tmp.y1
		self.vbuf[head].u = u1
		self.vbuf[head].v = v1		
		self.vbuf[head].color = cmul
		self.vbuf[head].secondary_color = cadd
		
		head += 1
		self.vbuf[head].x = tmp.x2
		self.vbuf[head].y = tmp.y2
		self.vbuf[head].u = u2
		self.vbuf[head].v = v2		
		self.vbuf[head].color = cmul
		self.vbuf[head].secondary_color = cadd
		
		head += 1
		self.vbuf[head].x = tmp.x3
		self.vbuf[head].y = tmp.y3
		self.vbuf[head].u = u3
		self.vbuf[head].v = v3		
		self.vbuf[head].color = cmul
		self.vbuf[head].secondary_color = cadd
			
		self.vbuf_head += 4
		
	cdef void _update_contex(self):
		if self._is_tex_dirty:
			gl.glEnable(self._tex_tgt)
			gl.glBindTexture(self._tex_tgt, self._tex_id)
			self._is_tex_dirty = False
		
		if self._is_blend_mode_dirty:
			self.set_blend_mode(self._blend_mode)
			self._is_blend_mode_dirty = False

	cdef void _flush(self):
		cdef int stride
		if self.vbuf_head > 0:
			self._update_contex()
			stride = sizeof(CVertexData)
			gl.glVertexPointer(2, gl.GL_FLOAT, stride, &self.vbuf[0].x)
			gl.glTexCoordPointer(2, gl.GL_FLOAT, stride, &self.vbuf[0].u)
			gl.glColorPointer(4, gl.GL_UNSIGNED_BYTE, stride, &self.vbuf[0].color)
			gl.glSecondaryColorPointer(3, gl.GL_UNSIGNED_BYTE, stride, &self.vbuf[0].secondary_color)
			gl.glDrawArrays(gl.GL_QUADS, 0, self.vbuf_head)
			self.vbuf_head = 0
			
	def draw_image(self, tex_tgt, tex_id, coord_idx, tex_coord_idx):
		cdef int _is_texture_dirty = self._tex_id != tex_id
		cdef int _is_blend_mode_dirty = self.stk_blend_mode.top() != self._blend_mode
		
		if _is_texture_dirty or _is_blend_mode_dirty or self.vbuf_head >= 1000:
			self._flush()
			self._is_texture_dirty = _is_texture_dirty
			self._is_blend_mode_dirty = _is_blend_mode_dirty
			self._tex_tgt = tex_tgt
			self._tex_id = tex_id
		self._append(coord_idx, tex_coord_idx)
	
	def end(self):
		# flush buffer anyway
		self._flush()
			

	####################################
	# Preloading all rendering data
	####################################
	def reg_pos(self, float x, float y):
		cdef CPos *pos = <CPos *>malloc(sizeof(CPos))
		pos.x = x
		pos.y = y
		self.vec_pos.push_back(pos)
		return self.vec_pos.size() - 1
	
	def reg_color(self, float r, float g, float b, float a):
		cdef CColor *color = <CColor *>malloc(sizeof(CColor))
		color.r = r
		color.g = g
		color.b = b
		color.a = a
		self.vec_color.push_back(color)
		return self.vec_color.size() - 1
	
	def reg_mat(self, float t0, float t1, float s0, float s1, float r0, float r1):
		cdef CMat *mat = <CMat *>malloc(sizeof(CMat))
		mat.t0 = t0
		mat.t1 = t1
		mat.s0 = s0
		mat.s1 = s1
		mat.r0 = r0
		mat.r1 = r1		
		self.vec_mat.push_back(mat)
		return self.vec_mat.size() - 1
	
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
		return self.vec_coords.size() - 1
	