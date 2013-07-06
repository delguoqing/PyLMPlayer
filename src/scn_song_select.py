import os
import glob
import random
import pyglet
import collections
from pyglet.gl import *
from tja import tja_header, tja_reader

from lm import lm_consts
from lm import lm_loader
from lm.extensions import lm_render_state
from lm.drawable import lm_drawable

import config

class CDiffInfo(object):
	def __init__(self, idx, course, rank, has_bunki):
		self.idx = idx
		self.rank = rank
		self.has_bunki = has_bunki
		self.course = course
		
	def __repr__(self):
		return "course:%d\nstar: %d\n has_bunki: %d\n"  % (self.course, self.rank, self.has_bunki)
	
	
class CSongInfo(object):
	def __init__(self, folder, genre, song_vol, se_vol, wave, preview_off, tja, diff_lst):
		self.genre = genre
		self.folder = folder
		self.song_vol = song_vol
		self.se_vol = se_vol
		self.wave = wave
		self.preview_off = preview_off
		self.tja = tja
		self.diff_lst = diff_lst

	def __repr__(self):
		msg = "\n".join([
			"genre: %s" % self.genre,
			"tja: %s" % self.tja,
			"wave: %s" % self.wave,
			"num_of_diff: %d" % (len(self.diff_lst) - self.diff_lst.count(None)),
		])
		msg += "\n" + "\n".join(map(repr, filter(None, self.diff_lst)))
		
		return msg
	
class CSongTexture(object):
	def __init__(self, num_slot):
		self._textures = collections.deque([None] * num_slot)
		self.tex_coords = -1
		self.coords = -1
		
	def set_texture(self, slot, image_file):
		if image_file == "":
			self._textures[slot] = None
		else:
			self._textures[slot] = pyglet.image.load(image_file)
	
	def get_texture(self, slot):
		ret = self._textures[slot]
		if ret is not None:
			ret = ret.get_texture()
			if self.tex_coords < 0:
				global renderer
				self.coords = renderer.reg_coords(-0.5*ret.width, -0.5*ret.height, 0.5*ret.width, -0.5*ret.height, 0.5*ret.width, 0.5*ret.height, -0.5*ret.width, 0.5*ret.height)
				self.tex_coords = renderer.reg_coords(0.0, ret.tex_coords[7], ret.tex_coords[3], ret.tex_coords[7], ret.tex_coords[3], 0.0, 0.0, 0.0)
		return ret
	
	def shift_left(self):
		self._textures.popleft()
		self._textures.append(None)
		
	def shift_right(self):
		self._textures.pop()
		self._textures.appendleft(None)
	
class CSongTitleRenderer(lm_drawable.CDrawable):
	def __init__(self, texture_set, texture_idx):
		super(CSongTitleRenderer, self).__init__(0, 0, None)
		self.texture_set = texture_set
		self.texture_idx = texture_idx
		self._as_tween_only = True
	
	def update(self, renderer, operation=lm_consts.MASK_ALL):
		if operation & lm_consts.MASK_DRAW:
			texture = self.texture_set.get_texture(self.texture_idx)
			if texture is not None:
				renderer.draw_image(texture.target, texture.id, self.texture_set.coords, self.texture_set.tex_coords)
	
SONG_ROOT = r"../song"
ALL_GENRE_NAME = ["anime", "classic", "j-pop", "game", "namco", "variety"]
MAX_BOARD = 11
BOARD_CENTER = 5

#ALL_GENRE_NAME = ["debug"]

NO_RENDER_DEBUG = False
inited = False

renderer = None
loader = None

mc_song_select = None
mc_song_select_submenu = None

song_lst = []
cursor_pos = 0

def build_song_lst_by_genre(genre_name):
	genre_folder = os.path.join(SONG_ROOT, genre_name)
	glob_pattern = os.path.join(genre_folder, "*/*.tja")
	reader = tja_reader.CReader()
	header = tja_header.CData()
	genre_song_lst = []
	print glob_pattern
	for file_path in glob.glob(glob_pattern):
		#print "doing %s" % file_path
		reader.set_file(file_path)
		header.reset()
		
		diff_lst = [None, None, None, None]
		folder, tja = os.path.split(file_path)
		
		diff_idx = 0
		while not reader.is_eof():
			header.ex_read(reader)
			header.refresh()
			if not header["HAS_FUMEN"]: break
			diff_lst[header["COURSE"]] = CDiffInfo(diff_idx, header["COURSE"], header["LEVEL"], header["HAS_BUNKI"])
			diff_idx += 1
				
		if diff_idx == 0: continue
		
		wave = header["WAVE"]
		song_vol = header["SONGVOL"]
		se_vol = header["SEVOL"]
		preview_off = header["DEMOSTART"]
		
		info = CSongInfo(folder, genre_name, song_vol, se_vol, wave, preview_off, tja, diff_lst)
		genre_song_lst.append(info)
	reader.close()
	
	return genre_song_lst

def build_song_lst():
	global song_lst
	
	song_lst = []
	for genre_name in ALL_GENRE_NAME:
		song_lst.extend(build_song_lst_by_genre(genre_name))
	

def set_genre(genre):
	pass

def on_update(dt):
	if NO_RENDER_DEBUG: return
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glOrtho(left, right, bottom, top, -1, 1)
			
	renderer.begin()
	mc_song_select.update(renderer)			
	renderer.end()

def update_board(mc, board_id):
	song_idx = (cursor_pos + board_id - BOARD_CENTER) % (len(song_lst) + 1)
	
	if song_idx > len(song_lst):
		print "back_board"
		mc.gotoAndPlay("back_board")
		song_texture_set.set_texture(board_id, "")
	elif song_idx == len(song_lst):
		print "random_board"
		mc.gotoAndPlay("random_board")
		song_texture_set.set_texture(board_id, "")
	else:
		print "song_board"
		mc.gotoAndPlay("song_board")
		song_info = song_lst[song_idx]
		song_texture_set.set_texture(board_id, os.path.join(song_info.folder, "sn_non_select.png"))

def on_enter(this):
	global renderer, loader
	global mc_song_select, mc_song_select_submenu
	global song_texture_set
	global cursor_pos
	global SONG_TEX_COORDS_INDEX, SONG_COORDS_INDEX
	
	if not inited:
		if not NO_RENDER_DEBUG:
			renderer = lm_render_state.CRenderer()
			renderer.init()
			
			loader = lm_loader.CLoader("wii", config.DATA["lm_root"], renderer)
	
			mc_song_select = loader.load_movie("song_select/song_select/song_select.lm")
		
			song_texture_set = CSongTexture(MAX_BOARD)
			
			board_move = mc_song_select.main_movie.board_move
			
			for i in xrange(MAX_BOARD):
				board = getattr(board_move, "song_board_%d" % i)
				board.title.add_drawable(CSongTitleRenderer(song_texture_set, i), 0)
				
			setup_viewport()
		
		build_song_lst()
	
	cursor_pos = BOARD_CENTER + 1
	board_move = mc_song_select.main_movie.board_move
	for i in xrange(MAX_BOARD):
		update_board(getattr(board_move, "song_board_%d" % i), i)
	board_move.gotoAndPlay("start")
	
	# loop start scrolling
	mc_song_select.main_movie.bg.gotoAndPlay("loop")
	
def setup_viewport():
	global left, right, top, bottom	
	cfg = config.DATA
	
	width = cfg["wnd_width"]
	height = cfg["wnd_height"]
	left = top = 0
	right = width
	bottom = height
	if cfg["widescreen"]:
		right += cfg["widescreen_padding"] * 2
	
def on_exit():
	pass

def on_key_press(symbol, modifiers):
	pass