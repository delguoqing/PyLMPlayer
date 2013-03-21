import lm_tag_base
import lm_consts
import lm_type_pos

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)
		
		self.uv = []
		self.xy = []
		for i in xrange(4):
			u = d["u%d" % i]
			v = d["v%d" % i]
			x = d["x%d" % i]
			y = d["y%d" % i]
			self.uv.append(lm_type_pos.CType(u, v))
			self.xy.append(lm_type_pos.CType(x, y))
			
		self.uv = tuple(self.uv)
		self.xy = tuple(self.xy)
		
		self.fill_style = d["fill_style"]
		self.fill_idx = d["fill_idx"]
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_SHAPE