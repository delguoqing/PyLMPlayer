from lm.util import lm_tag_reader
from lm import lm_consts
import lm_type_img

class CTag(object):

	def __init__(self, ctx, tag):
		fmt = ctx.format[self.get_id()]
		d = lm_tag_reader.read_tag(fmt, tag)
		
		_data = []
		for info in d["img_list"]:
			fname = ctx.str_list.get_value(info["name_idx"])
			img = lm_type_img.CType(fname, info["img_idx"], info["width"], info["height"])
			_data.append(img)
		self.ctx = ctx
		self._data = tuple(_data)
			
	def get_value(self, idx):
		return self._data[idx]
	
	def get_id(self):
		return lm_consts.TAG_IMG_LIST