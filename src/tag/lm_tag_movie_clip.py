import lm_tag_base
import lm_consts

class CTag(lm_tag_base.CTag):
	
	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = CTag.parse_tag(ctx, tag)
		
		self.character_id = d["character_id"]
		self.max_depth = d["max_depth"]
		self.class_name = d["class_name"]

		self._frame_label_tags = []
		self._key_frame_tags = []
		self._frame_tags = []
	
	def add_ctrl_tag(self, tag):
		id = tag.get_id()
		if id == lm_consts.TAG_FRAME_LABEL:
			self._add_frame_label_tag(tag)
		elif id == lm_consts.TAG_FRAME:
			self._add_frame_tag(tag)
		elif id == lm_consts.TAG_KEY_FRAME:
			self._add_key_frame_tag(tag)
		else:
			assert False, "Can't add tag 0x%x to MovieClip!"
		
	def _add_frame_label_tag(self, tag):
		self._frame_label_tags.append(tag)
		
	def _add_frame_tag(self, tag):
		self._frame_tags.append(tag)
		
	def _add_key_frame_tag(self, tag):
		self._key_frame_tags.append(tag)