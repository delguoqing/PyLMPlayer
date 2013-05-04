from lm import lm_consts

import os.path
import pyglet
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
		
	def load_textures(self, bin):
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
				
			fullpath = os.path.join(self.ctx.img_root, filename)

			image_data = None
			try:
				image_data = pyglet.image.load(fullpath)
			except IOError:
				fullpath = os.path.join(self.ctx.img_root, def_filename)
				image_data = pyglet.image.load(fullpath)
			texture = bin.add(image_data)
			self._data.append(texture)
			
	# memory leak!!!!
	def replace_texture(self, idx, filename, bin):
		image_data = pyglet.image.load(filename)
		self._data[idx] = bin.add(image_data)
		return self._data[idx]