from lm.util import lm_tag_reader
from lm import lm_consts

class CTag(object):
	
	def __init__(self, ctx, tag):
		
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		
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