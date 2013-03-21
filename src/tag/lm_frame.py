import lm_tag_base
import lm_consts

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_FRAME