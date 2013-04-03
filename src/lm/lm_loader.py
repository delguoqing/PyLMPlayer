import pyglet

from lm.util import lm_tag_reader
from lm.format import lm_format_map
import lm_consts

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
	
		self._super_tag_stack = []
		
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
		
	def get_character(self, character_id):
		return self.char_dict.get(character_id)
		
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
	
def load(filename, root, platform):
	# read LM file data
	f = open(filename, "rb")
	data = f.read()
	
	# build initial contex
	ctx = CContex()
	ctx.set_img_root(root)
	ctx.set_platform(platform)
	
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
			ctx.set_as_list(_t)
		elif tag_type == lm_consts.TAG_IMG_LIST:
			ctx.set_img_list(_t)
		elif tag_type == lm_consts.TAG_RECT_LIST:
			ctx.set_rect_list(_t)
			
		# ---------- DRAWABLES ---------
		elif tag_type == lm_consts.TAG_MOVIECLIP:
			ctx.add_super_tag(_t, _t.get_sub_tag_cnt(), ctx.add_movieclip)
		elif tag_type == lm_consts.TAG_SPRITE:
			ctx.add_super_tag(_t, _t.get_sub_tag_cnt(), ctx.add_sprite)
		elif tag_type in (lm_consts.TAG_SHAPE, lm_consts.TAG_SHAPE2):
			ctx.add_sub_tag(_t)
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