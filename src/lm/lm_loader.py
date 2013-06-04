import os
import sys
import random
import pyglet
import lm_consts

from lm.util import lm_tag_reader
from lm.format import lm_format_map
from lm.as_object import as_movieclip_pool
from lm.type import lm_type_mat

class CLoader(object):
	
	def __init__(self, platform, lm_root, renderer):
		self.texture_bin = pyglet.image.atlas.TextureBin(4096, 4096)
		self.platform = platform
		self.lm_root = lm_root
		self.renderer = renderer
		
	def load_movie_cos(self, name, cos, cos_id, translate=(0, 0)):
		filename = os.path.join(self.lm_root, name)
		img_root = os.path.split(filename)[0]
		
		cos_filename = os.path.join(self.lm_root, cos)
		cos_img_root = os.path.split(cos_filename)[0]
		
		ctx = load(filename, img_root, self.platform, self.texture_bin, self.renderer)
		ctx_cos = load(cos_filename, cos_img_root, self.platform, self.texture_bin, self.renderer)
		ctx.set_character(cos_id, ctx_cos.get_character(ctx_cos.stage_info.start_character_id))
		
		char_id = ctx.stage_info.start_character_id
		char_tag = ctx.get_character(char_id)
		
		movieclip = char_tag.instantiate(0, 0, parent=None)
		movieclip.init()
		movieclip.set_matrix_index(
			self.renderer.reg_mat(translate[0], translate[1], 1.0, 1.0, 0.0, 0.0))
		movieclip.ctx = ctx
		return movieclip
	
	def load_movie(self, name, translate=(0, 0)):
		
		filename = os.path.join(self.lm_root, name)
		img_root = os.path.split(filename)[0]
		
		ctx = load(filename, img_root, self.platform, self.texture_bin, self.renderer)
		char_id = ctx.stage_info.start_character_id
		char_tag = ctx.get_character(char_id)
		movieclip = char_tag.instantiate(0, 0, parent=None)
		movieclip.init()
		movieclip.set_matrix_index(
			self.renderer.reg_mat(translate[0], translate[1], 1.0, 1.0, 0.0, 0.0))
		movieclip.ctx = ctx
		return movieclip
		
	# Load several movieclips sharing the same contex file.
	def load_multi_movie(self, name, count, translate=(0, 0)):			
		mcs = []
		
		filename = os.path.join(self.lm_root, name)
		img_root = os.path.split(filename)[0]
	
		ctx = load(filename, img_root, self.platform, self.texture_bin, self.renderer)
		char_id = ctx.stage_info.start_character_id
		char_tag = ctx.get_character(char_id)
		
		for i in xrange(count):
			movieclip = char_tag.instantiate(0, 0, parent=None)
			movieclip.init()
			movieclip.set_matrix(
				self.renderer.reg_mat(translate[0], translate[1], 1.0, 1.0, 0.0, 0.0))
			movieclip.ctx = ctx
			mcs.append(movieclip)
			
		return mcs		
			
	def load_movie_pool(self, defs):
		pool = as_movieclip_pool.CDrawable(0, 0, parent=None)
		for _def in defs:
			mcs = []
			for tuple in _def:
				if len(tuple) == 2: 
					name, count = tuple
					translate = None
				elif len(tuple) == 3: 
					name, count, translate = tuple
				mcs += self.load_multi_movie(name, count, translate)
			if len(_def) > 1: random.shuffle(mcs)
			pool.register(mcs)
		return pool
	
class CContex(object):
	
	def __init__(self):
		self.format = None
		self.img_root = None
		self.str_list = None
		self.color_list = None
		self.pos_list = None
		self.mat_list = None
		self.as_list = None
		self.img_list = None
		self.rect_list = None
		self.char_dict = {}
		self.texture_bin = None
		self.renderer = None
	
		self.shape_tags = []
		
		self._super_tag_stack = []
		
		self._global = {}
		
	def set_img_root(self, root):
		self.img_root = root
		
	def set_platform(self, platform):
		self.format = __import__("lm.format.lm_format_%s" % platform, fromlist=["lm", "format"])
				
	def set_str_list(self, tag):
		self.str_list = tag
	def set_color_list(self, tag):
		self.color_list = tag
	def set_pos_list(self, tag):
		self.pos_list = tag
	def set_mat_list(self, tag):
		self.mat_list = tag
	def set_as_list(self, tag):
		self.as_list = tag
	def set_img_list(self, tag):
		self.img_list = tag
	def set_rect_list(self, tag):
		self.rect_list = tag

	def add_sprite(self, tag):
		self.char_dict[tag.get_character_id()] = tag
		
	def add_movieclip(self, tag):
		self.char_dict[tag.get_character_id()] = tag
		
	def add_shape_tag(self, tag):
		self.shape_tags.append(tag)
		self.add_sub_tag(tag)
		
	def get_character(self, character_id):
		return self.char_dict.get(character_id)
		
	# Used by costume change?
	def set_character(self, character_id, tag):
		self.char_dict[character_id] = tag
	
	def add_super_tag(self, tag, sub_cnt, callback):
		self._super_tag_stack.append((tag, sub_cnt, callback))
	
	def add_sub_tag(self, tag):
		if not self._super_tag_stack:
			raise Exception("No super tag to add to!")
		super_tag, sub_cnt, callback = self._super_tag_stack.pop(-1)
		super_tag.add_sub_tag(tag)
		sub_cnt -= 1
		if sub_cnt <= 0:
			callback(super_tag)
		else:
			self._super_tag_stack.append((super_tag, sub_cnt, callback))
		
	def set_global(self, name, val):
		self._global[name] = val
		
	def replace_texture(self, idx, filename):
		texture = self.img_list.replace_texture(idx, filename, self.texture_bin)
		for shape_tag in self.shape_tags:
			if shape_tag.fill_idx == idx and shape_tag.origin_fill_style == lm_consts.FILL_STYLE_CLIPPED_IMAGE:
				shape_tag.set_texture(texture)
				
def load(filename, root, platform, texture_bin, renderer):
	# uniform resource root
	res_root = root
	
	# read LM file data
	f = open(filename, "rb")
	data = f.read()
	
	# build initial contex
	ctx = CContex()
	ctx.set_img_root(root)
	ctx.set_platform(platform)
	ctx.texture_bin = texture_bin
	ctx.renderer = renderer
	
	# start parsing
	f.seek(0x40)
	while True:
		data = f.read(ctx.format.HEADER_SIZE)
		if not data:
			break
		header = lm_tag_reader.read_tag(ctx.format.DATA[0xFF00], data)
		tag_type, tag_size = header["tag_type"], header["tag_size"]
		tag_name = lm_format_map.MAP.get(tag_type)
		data = data + f.read(tag_size * 4)
		
		# This tag is not handled a.t.m
		if not tag_name:
			assert tag_type != 0x0027
			continue
			
		# try find a handler module
		try:
			module = __import__("lm.tag.lm_tag_%s" % tag_name, fromlist=["lm", "tag"])
		except ImportError:
			assert tag_type != 0x0027, tag_name
			continue
		
		# handle different tags	
		_t = module.CTag(ctx, data)
		# ---------- LOOKUP TABLES -------------
		if tag_type == lm_consts.TAG_STR_LIST:
			ctx.set_str_list(_t)
		elif tag_type == lm_consts.TAG_COLOR_LIST:
			ctx.set_color_list(_t)
		elif tag_type == lm_consts.TAG_POS_LIST:
			ctx.set_pos_list(_t)
		elif tag_type == lm_consts.TAG_MAT_LIST:
			ctx.set_mat_list(_t)
		elif tag_type == lm_consts.TAG_AS_LIST:
			if _t.as_cnt > 0:
				sys.path.append(res_root)
				patch_module = __import__(os.path.splitext(os.path.split(filename)[1])[0])
				sys.path.pop()
				_t.patch_py_actionscript(patch_module.DATA)
			ctx.set_as_list(_t)
		elif tag_type == lm_consts.TAG_IMG_LIST:
			_t.load_textures(texture_bin)
			ctx.set_img_list(_t)
		elif tag_type == lm_consts.TAG_RECT_LIST:
			ctx.set_rect_list(_t)
		elif tag_type == lm_consts.TAG_STAGE_INFO:
			ctx.stage_info = _t
			
		# ---------- DRAWABLES ---------
		elif tag_type == lm_consts.TAG_MOVIECLIP:
			ctx.add_super_tag(_t, _t.get_sub_tag_cnt(), ctx.add_movieclip)
		elif tag_type == lm_consts.TAG_SPRITE:
			ctx.add_super_tag(_t, _t.get_sub_tag_cnt(), ctx.add_sprite)
		elif tag_type in (lm_consts.TAG_SHAPE, lm_consts.TAG_SHAPE2):
			ctx.add_shape_tag(_t)
		elif tag_type == lm_consts.TAG_PLACE_OBJ:
			if _t.get_sub_tag_cnt() == 0:	# any clip action follows?
				ctx.add_sub_tag(_t)
			else:
				ctx.add_super_tag(_t, _t.get_sub_tag_cnt(), ctx.add_sub_tag)
		elif tag_type == lm_consts.TAG_REMOVE_OBJ:
			ctx.add_sub_tag(_t)				
		elif tag_type == lm_consts.TAG_CLIP_ACTION:
			ctx.add_sub_tag(_t)
		elif tag_type == lm_consts.TAG_DO_ACTION:
			ctx.add_sub_tag(_t)
		elif tag_type in (lm_consts.TAG_FRAME, lm_consts.TAG_KEY_FRAME):
			if _t.get_sub_tag_cnt() == 0:
				ctx.add_sub_tag(_t)
			else:
				ctx.add_super_tag(_t, _t.get_sub_tag_cnt(), ctx.add_sub_tag)
		elif tag_type == lm_consts.TAG_FRAME_LABEL:
			ctx.add_sub_tag(_t)
		
	f.close()
	return ctx