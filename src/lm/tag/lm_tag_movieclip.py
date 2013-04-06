import lm_tag_base
from lm import lm_consts
from lm.as_object import as_movieclip

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)
		
		self.character_id = d["character_id"]
		self.max_depth = d["max_depth"]
		self.class_name = self.ctx.str_list.get_val(d["class_name_idx"])

		self._key_frame_cnt = d["key_frame_cnt"]
		self._frame_cnt = d["0001_cnt"]
		self._frame_label_cnt = d["frame_label_cnt"]
		
		self._frame_tags = []
		self._frame_label_tags = []
		self._key_frame_tags = []
		self._label_dict = {}
		
	def add_sub_tag(self, tag):
		id = tag.get_id()
		if id == lm_consts.TAG_FRAME_LABEL:
			self._add_frame_label_tag(tag)
		elif id == lm_consts.TAG_FRAME:
			self._add_frame_tag(tag)
		elif id == lm_consts.TAG_KEY_FRAME:
			self._add_key_frame_tag(tag)
		else:
			assert False, "Can't add tag 0x%x to MovieClip!"

	def get_character_id(self):
		return self.character_id
				
	def get_sub_tag_cnt(self):
		return self._key_frame_cnt + self._frame_cnt + self._frame_label_cnt
		
	def _add_frame_label_tag(self, tag):
		self._frame_label_tags.append(tag)
		self._label_dict[tag.name] = tag.frame_id
		
	def _add_frame_tag(self, tag):
		self._frame_tags.append(tag)
		
	def _add_key_frame_tag(self, tag):
		self._key_frame_tags.append(tag)
		
	@classmethod
	def get_id(cls):
		return lm_consts.TAG_MOVIECLIP
		
	def instantiate(self, inst_id, depth, parent=None):
		inst = as_movieclip.CObj(self._frame_tags, self._key_frame_tags, self._label_dict, self.max_depth, inst_id, depth, parent=parent)
		inst.init()
		return inst
		