import lm_tag_base
from lm import lm_consts

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		self.name = self.ctx.str_list.get_val(d["name_idx"])
		self.frame_id = d["frame_id"]
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_FRAME_LABEL