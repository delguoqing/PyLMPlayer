from lm import lm_consts
import os
import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		self._data = []
		self._parsed_data = d
			
	def get_val(self, idx):
		return self._data[idx]
		
	def get_id(self):
		return lm_consts.TAG_IMG_LIST
		
	def load_textures(self):
		self._data = []
		d = self._parsed_data
		self._parsed_data = None
		
		for info in d["img_list"]:
			filename = self.ctx.str_list.get_val(info["name_idx"])

			def_filename = "noname_%d.png" % info["img_idx"]
			if filename == "":
				filename = def_filename
			elif not filename.endswith(".png"):
				filename = os.path.splitext(filename)[0] + ".png"
				
			contex = self.ctx
			try:
				texture = contex.load_texture(filename)
			except IOError:
				texture = contex.load_texture(def_filename)

			self._data.append(texture)