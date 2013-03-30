from lm import lm_consts
from lm.util import lm_tag_reader
from lm.drawable import lm_sprite

import lm_tag_base

class CTag(lm_tag_base.CTag):

	# The difference between Sprite and MovieClip.
	# basically, there're the same thing.(In Flash, they use Movieclip, and in # SDK and swf spec, they use Sprite).
	# In this project:
	# Sprite is a single-frame Movieclip contains only shapes, Also, Sprite do # not support action script.

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		
		rect_idx = d["size_idx"]
		
		self._shape_tags = []
		self._rect = ctx.rect_list.get_val(rect_idx)
		self._sub_tag_cnt = d["f023_cnt"]
		if d["f024_cnt"]:
			self._sub_tag_cnt += d["f024_cnt"]
		self.char_id = d["character_id"]
		
	def add_sub_tag(self, tag):
		self._shape_tags.append(tag)
		
	def get_sub_tag_cnt(self):
		return self._sub_tag_cnt
		
	def get_character_id(self):
		return self.char_id
		
	def instantiate(self, parent=None):
		sprite = lm_sprite.CDrawable(len(self._shape_tags), parent=parent)
		for i, shape_tag in enumerate(self._shape_tags):
			shape = shape_tag.instantiate(parent=self)
			sprite.add_drawable(shape, i)
		
		return sprite
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_SPRITE