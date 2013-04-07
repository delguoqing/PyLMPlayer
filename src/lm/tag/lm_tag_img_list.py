from lm import lm_consts

import os.path
import pyglet
import lm_tag_base

class CTag(lm_tag_base.CTag):

	def __init__(self, ctx, tag):
		super(CTag, self).__init__(ctx, tag)
		d = self.parse_tag(ctx, tag)
		self._data = []
		self._bin = None
		self._make_atalas(d)
			
	def get_val(self, idx):
		return self._data[idx]

	@classmethod	
	def get_id(self):
		return lm_consts.TAG_IMG_LIST
		
	def _make_atalas(self, d):
		self._bin = pyglet.image.atlas.TextureBin(2048, 2048)
		self._data = []
		
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
				
			texture = self._bin.add(image_data)
			self._data.append(texture)