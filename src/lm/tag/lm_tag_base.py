import lm_tag_reader
import lm_consts

class CTag(object):

	def __init__(self, ctx, tag):
		pass
				
	@classmethod
	def parse_tag(cls, ctx, tag):
		fmt = ctx.format[cls.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		return d
		
	@classmethod
	def get_id(cls):
		raise NotImplementedError