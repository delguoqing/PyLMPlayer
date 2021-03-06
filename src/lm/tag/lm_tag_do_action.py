import lm_tag_base
from lm import lm_consts

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self.as_idx = d["as_idx"]
		self.script = ctx.as_list.get_val(self.as_idx)
		
	
	def get_id(cls):
		return lm_consts.TAG_DO_ACTION
		
	def execute(self, target=None):
		if not target: return
		self.script(target, self.ctx._global)
		