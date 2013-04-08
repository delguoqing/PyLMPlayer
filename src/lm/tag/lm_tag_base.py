from lm.util import lm_tag_reader
from lm import lm_consts

class CTag(object):

	def __init__(self, ctx, tag):
		self.ctx = ctx
				
	
	def parse_tag(cls, ctx, tag):
		fmt = ctx.format.DATA[cls.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		return d
		
	
	def get_id(cls):
		raise NotImplementedError
		
	def add_sub_tag(self, tag):
		raise NotImplementedError
		
	def get_sub_tag_cnt(self):
		raise NotImplementedError