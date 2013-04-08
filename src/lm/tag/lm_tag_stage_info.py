from lm.util import lm_tag_reader
from lm import lm_consts

import lm_tag_base

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		self.max_character_id = d["max_character_id"]
		self.start_character_id = d["start_character_id"]
		self.fps = d["fps"]
		self.width = d["width"]
		self.height = d["height"]
		self.x = d["x"]
		self.y = d["y"]
		self.ctx = ctx
	
			
	def get_id(self):
		return lm_consts.TAG_STAGE_INFO