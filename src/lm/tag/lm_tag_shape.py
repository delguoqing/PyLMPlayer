import math
import pyglet
import lm_tag_base

from lm import lm_consts
from lm.type import lm_type_rect

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		self._parsed_data = d
		
		x_min = min(d["x0"], d["x1"], d["x2"], d["x3"])
		x_max = max(d["x0"], d["x1"], d["x2"], d["x3"])
		y_min = min(d["y0"], d["y1"], d["y2"], d["y3"])
		y_max = max(d["y0"], d["y1"], d["y2"], d["y3"])
		
		# Prepare for 
		_is_replace = True
		for i in xrange(4):
			if d["u%d" % i] != -1.0: _is_replace = False; break
			if d["u%d" % i] != -1.0: _is_replace = False; break
		if _is_replace:
			d["u0"], d["v0"], d["u1"], d["v1"], d["u2"], d["v2"], d["u3"], d["v3"] = 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0
						
		self._rect = lm_type_rect.CType(x_min, y_min, x_max, y_max)
				
		self.origin_fill_style = d["fill_style"]
		self.fill_style = d["fill_style"]
		self.fill_idx = d["fill_idx"]
		
		self.texture = None
		if self.fill_style == lm_consts.FILL_STYLE_SOLID_COLOR:
			self.fill_style = lm_consts.FILL_STYLE_CLIPPED_IMAGE
			color = self.ctx.color_list.get_val(self.fill_idx)
			self.texture = self._get_faked_texture(color)
		else:
			self.texture = self.ctx.img_list.get_val(self.fill_idx)
			
		self.base_tex_coords = self.texture.tex_coords
			
		# Python level data
		self.tex_coords = None
		self.vertices = None
		self.create_vertex_list()
		# C level data
		self.coords_index = []
		self.tex_coords_index = []
		self.register_all()
		
	def set_texture(self, texture):
		self.texture = texture
		self.base_tex_coords = texture.tex_coords
		
		self.tex_coords = None
		self.vertices = None
		self.create_vertex_list()
		
	# fake a solid color texture
	# simplify the problem a lot!
	def _get_faked_texture(self, color):
		img = pyglet.image.SolidColorImagePattern((color.rB, color.gB, color.bB, color.aB)).create_image(1, 1)
		return self.ctx.texture_bin.add(img)
		
	def create_vertex_list(self):
		if self.tex_coords:
			return self.vertices, self.tex_coords, self.texture
		
		_r = self._rect
		if self.fill_style == lm_consts.FILL_STYLE_CLIPPED_IMAGE:
			_tx_len = self.base_tex_coords[-9] - self.base_tex_coords[-3]
			_ty_len = self.base_tex_coords[-5] - self.base_tex_coords[-8]
			_tx_base = self.base_tex_coords[-3]
			_ty_base = self.base_tex_coords[-5] 
			
			d = self._parsed_data
			self.vertices = [d["x0"], d["y0"], d["x1"], d["y1"], d["x2"], d["y2"], d["x3"], d["y3"]]
			self.tex_coords = [
			_tx_base + max(0.0, min(1.0, d["u0"])) * _tx_len, 
			_ty_base - max(0.0, min(1.0, d["v0"])) * _ty_len,
			_tx_base + max(0.0, min(1.0, d["u1"])) * _tx_len, 
			_ty_base - max(0.0, min(1.0, d["v1"])) * _ty_len,
			_tx_base + max(0.0, min(1.0, d["u2"])) * _tx_len,
			_ty_base - max(0.0, min(1.0, d["v2"])) * _ty_len,
			_tx_base + max(0.0, min(1.0, d["u3"])) * _tx_len, 
			_ty_base - max(0.0, min(1.0, d["v3"])) * _ty_len]
			
#			print "recalc!"
		elif self.fill_style == lm_consts.FILL_STYLE_TILED_IMAGE:
			d = self._parsed_data
			_tx_len = self.base_tex_coords[-9] - self.base_tex_coords[-3]
			_ty_len = self.base_tex_coords[-5] - self.base_tex_coords[-8]
			_tx_base = self.base_tex_coords[-3]
			_ty_base = self.base_tex_coords[-5] 
			
			umin = min(d["u0"], d["u2"])
			umax = max(d["u0"], d["u2"])
			vmin = min(d["v0"], d["v2"])
			vmax = max(d["v0"], d["v2"])
			
			_x_mapping = []
			_y_mapping = []
			# U direction split
			stride_u = umax - umin
			u = max(0, umin)
			while True:
				_u = math.fmod(-u, 1.0) * _tx_len + _tx_base
				_x = _r.xmin + 1.0 * (u - umin) / stride_u * _r.width
				_x_mapping.insert(0, (_x, _u))
				if u == umin:
					break
				u = max(u - 1.0, umin)
			u = min(0, umax)
			while True:
				_u = math.fmod(u, 1.0) * _tx_len + _tx_base
				_x = _r.xmin + 1.0 * (u - umin) / stride_u * _r.width
				_x_mapping.append((_x, _u))
				if u == umax:
					break
				u = min(u + 1.0, umax)
			# V direction split
			stride_v = vmax - vmin
			v = max(0, vmin)
			while True:
				_v = _ty_base - math.fmod(-v, 1.0) * _ty_len
				_y = _r.ymin + 1.0 * (v - vmin) / stride_v * _r.height
				_y_mapping.insert(0, (_y, _v))
				if v == vmin:
					break
				v = max(v - 1.0, vmin)
			v = min(0, vmax)
			while True:
				_v = _ty_base - math.fmod(v, 1.0) * _ty_len
				_y = _r.ymin + 1.0 * (v - vmin) / stride_v * _r.height
				_y_mapping.append((_y, _v))
				if v == vmax:
					break
				v = min(v + 1.0, vmax)
			self.vertices = []
			self.tex_coords = []
			for (_x0, _u0), (_x1, _u1) in zip(_x_mapping[:-1], _x_mapping[1:]):
				for (_y0, _v0), (_y1, _v1) in zip(_y_mapping[:-1], _y_mapping[1:]):
					# Take care of the border
					if _u1 == _tx_base: _u1 += _tx_len
					if _v1 == _ty_base: _v1 -= _ty_len
					self.vertices.extend((_x0, _y0, _x1, _y0, _x1, _y1, _x0, _y1))
					self.tex_coords.extend((_u0, _v0, _u1, _v0, _u1, _v1, _u0, _v1))
		else:
			assert False, "not supported fill type! 0x%02x" % self.fill_style
		
		self._parsed_data = None
				
		return self.vertices, self.tex_coords, self.texture

	def __repr__(self):
		msg = ""
		msg += ",".join(map(str, self.coords_index))
		msg += "\n"
		msg += ",".join(map(str, self.tex_coords_index))
		msg += "\n"
		for i in xrange(0, len(self.vertices), 8):
			msg += ("%f " * 8) %  tuple(self.vertices[i: i + 8])
			msg += "\n"
			msg += ("%f " * 8) %  tuple(self.tex_coords[i: i + 8])
			msg += "\n"
		return msg
			
	def register_all(self):
		renderer = self.ctx.renderer
		for i in xrange(0, len(self.vertices), 8):
			x0, y0, x1, y1, x2, y2, x3, y3 = self.vertices[i: i + 8]
			u0, v0, u1, v1, u2, v2, u3, v3 = self.tex_coords[i: i + 8]
			self.coords_index.append(renderer.reg_coords(x0, y0, x1, y1, x2, y2, x3, y3))
			self.tex_coords_index.append(renderer.reg_coords(u0, v0, u1, v1, u2, v2, u3, v3))

	def get_id(cls):
		return lm_consts.TAG_SHAPE
