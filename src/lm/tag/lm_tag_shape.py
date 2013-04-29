import pyglet
import lm_tag_base

from lm import lm_consts
from lm.type import lm_type_pos
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
		
		self._rect = lm_type_rect.CType(x_min, y_min, x_max, y_max)
				
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
			_ty_base - max(0.0, min(1.0, d["v3"])) * _ty_len, ]
			
		elif self.fill_style == lm_consts.FILL_STYLE_TILED_IMAGE:
			_vertices = []
			_tex_coords = []
			count = 0
			for _y in xrange(_r.ymin, _r.ymax, self.texture.height):
				for _x in xrange(_r.xmin, _r.xmax, self.texture.width):
	
					_xmin = _x
					_xmax = _x + self.texture.width
					_ymin = _y
					_ymax = _y + self.texture.height
									
					_vertices += (_xmin, _ymax, _xmax, _ymax, _xmax, 
					_ymin, _xmin, _ymin)

					_tex_coords2 = list(self.base_tex_coords)
					if _xmax > _r.xmax:
						scale_tx = (_r.xmax - _xmin) * 1.0 / self.texture.width
						_vertices[-4] = _vertices[-6] = _r.xmax
					else:
						scale_tx = 1
					_tx_len = _tex_coords2[-9] - _tex_coords2[-3]
					_tex_coords2[-6] = _tex_coords2[-9] = _tex_coords2[-3] + _tx_len * scale_tx					
					if _ymax > _r.ymax:
						scale_ty = (_r.ymax - _ymin) * 1.0 / self.texture.height
						_vertices[-5] = _vertices[-7] = _r.ymax	
					else:
						scale_ty = 1
					_ty_len = _tex_coords2[-5] - _tex_coords2[-8]
					_tex_coords2[-5] = _tex_coords2[-2] = _tex_coords2[-8] + _ty_len * scale_ty

					for i, v in enumerate(_tex_coords2):
						if i % 3 != 2:
							_tex_coords.append(v)
							
					count += 1	
			self.vertices = _vertices
			self.tex_coords = _tex_coords					
		else:
			assert False, "not supported fill type! 0x%02x" % self.fill_style

#		self._parsed_data = None
				
		return self.vertices, self.tex_coords, self.texture
		
	def get_id(cls):
		return lm_consts.TAG_SHAPE
