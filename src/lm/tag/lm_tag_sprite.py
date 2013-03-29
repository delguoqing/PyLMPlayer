from lm.util import lm_tag_reader
from lm import lm_consts

class CTag(object):

	# The difference between Sprite and MovieClip.
	# basically, there're the same thing.(In Flash, they use Movieclip, and in # SDK and swf spec, they use Sprite).
	# In this project:
	# Sprite is a single-frame Movieclip contains only shapes, Also, Sprite do # not support action script.

	def __init__(self, ctx, tag):
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		rect_idx = d["size_idx"]
		
		self._shape_tags = []
		self._rect = ctx.rect_list[rect_idx]
		
	def add_shape_tag(self, tag):
		self._shape_tags.append(tag)
		
	def instantiate(self, name, inst_id, matrix, cadd, cmul, )