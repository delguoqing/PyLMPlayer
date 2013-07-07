import os
import glob
import random
import pyglet
import collections
from pyglet.gl import *
from tja import tja_header, tja_reader
import game_state

from lm import lm_consts
from lm import lm_loader
from lm.extensions import lm_render_state
from lm.drawable import lm_drawable

import config

class CDiffInfo(object):
	def __init__(self, idx, course, star, has_bunki):
		self.idx = idx
		self.star = star
		self.has_bunki = has_bunki
		self.course = course
		
	def __repr__(self):
		return "course:%d\nstar: %d\n has_bunki: %d\n"  % (self.course, self.star, self.has_bunki)
	
	
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
	
class CPreviewPlayer(object):
	def __init__(self, max_preview, interval=5):
		self.max_preview = max_preview
		self.now_playing_wave = None
		self.player = pyglet.media.Player()
		self.preview_off = None
		self.accu_t = 0
		self.interval = interval
		self.is_paused = True
	
	def pause(self):
		self.is_paused = True
		if self.player.playing:
			self.player.pause()
	
	def set_audio(self, wave, preview_off):
		if self.player.playing:
			self.player.pause()
				
		if wave:
			self.preview_off = preview_off
			source = pyglet.media.load(wave)
			self.player.queue(source)
			if self.now_playing_wave:
				self.player.next()
			else:
				self.player.play()
			self.player.seek(self.preview_off)
			self.accu_t = 0
			self.now_playing_wave = wave
			self.is_paused = False
			
	def update(self, dt):
		if self.is_paused: return
		self.accu_t += dt
		if self.player.playing and self.accu_t > self.max_preview:
			self.player.pause()
		elif self.accu_t > self.max_preview + self.interval:
			self.player.seek(self.preview_off)
			self.player.play()
			self.accu_t = 0

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
ALL_GENRE_NAME = ["j-pop", "animation", "variety", "classic", "namco", "game"]
GENRE_NAME_2_ID = dict([(genre_name, genre_name_idx) for genre_name_idx, genre_name in enumerate(ALL_GENRE_NAME)])
MAX_BOARD = 11
BOARD_CENTER = 5

# How large has the menu been opened up
# Used to recover from open to close
menu_open_up_count = 15
cur_genre = 0
enable_input = False


#ALL_GENRE_NAME = ["debug"]

NO_RENDER_DEBUG = False
inited = False

renderer = None
loader = None

mc_song_select = None
mc_song_select_submenu = None

song_lst = []
cursor_pos = BOARD_CENTER + 1

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
	

def set_genre(genre, dir=""):
	global cur_genre
	
	# set bg
	bg = mc_song_select.main_movie.bg
	bg.lower.gotoAndPlay("genre%d" % cur_genre)
	bg.upper.gotoAndPlay("genre%d" % genre)
	
	board_move = mc_song_select.main_movie.board_move
	# set genre text
	mc_genre = board_move.genre
	mc_genre.gotoAndPlay(dir+ALL_GENRE_NAME[genre])
	# set menu title
	board_move.menu_title.gotoAndPlay("genre%d" % genre)
	
	# update cur_genre
	cur_genre = genre
	

def on_update(dt):
	if NO_RENDER_DEBUG: return
	
	preview_player.update(dt)
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glOrtho(left, right, bottom, top, -1, 1)
			
	renderer.begin()
	mc_song_select.update(renderer)			
	renderer.end()

def get_cur_song_idx(board_id):
	return (cursor_pos + board_id - BOARD_CENTER) % (len(song_lst) + 1)
	
def update_board(mc, board_id):
	song_idx = get_cur_song_idx(board_id)
	
	if song_idx > len(song_lst):
		print "update board %d: back_board" % board_id
		mc.gotoAndPlay("back_board")
		song_texture_set.set_texture(board_id, "")
	elif song_idx == len(song_lst):
		print "update board %d: random_board" % board_id
		mc.gotoAndPlay("random_board")
		song_texture_set.set_texture(board_id, "")
	else:
		song_info = song_lst[song_idx]
		
		print "update board %d: song_board" % board_id
		mc.gotoAndPlay("song_board")
		mc.crown.active = False
		mc.board.gotoAndPlay("genre%d" % GENRE_NAME_2_ID[song_info.genre])
		
		song_texture_set.set_texture(board_id, os.path.join(song_info.folder, "sn_non_select.png"))
		
		if board_id == BOARD_CENTER:
			set_genre(GENRE_NAME_2_ID[song_info.genre])
			select_song_texture_set.set_texture(0, os.path.join(song_info.folder, "sn_select_short.png"))
			select_song_texture_set.set_texture(1, os.path.join(song_info.folder, "sn_select_full.png"))			

def update_course(mc, song_info):
	for diff_idx, diff_info in enumerate(song_info.diff_lst):
		mc_course_wise = mc.get_drawable(3 - diff_idx)
		if mc_course_wise is None: continue
		mc_star = mc_course_wise.star
		if diff_info is None:
			mc_star.gotoAndPlay("star0")
		else:
			mc_star.gotoAndPlay("star%d" % diff_info.star)
			
def on_initial_animation_end(root, data):
	song_idx = get_cur_song_idx(BOARD_CENTER)
	
	mc = data
	
	if song_idx > len(song_lst):	# invalid board
		mc.gotoAndPlay("close%d" % menu_open_up_count)
		mc.open_board.gotoAndPlay("close%d" % menu_open_up_count)
	elif song_idx == len(song_lst):
		mc.gotoAndPlay("close%d" % menu_open_up_count)
		mc.open_board.gotoAndPlay("r_close%d" % menu_open_up_count)
	else:
		mc.gotoAndPlay("select")
		mc.hiscore.active = False

def on_menu_open_up_count(root, data):
	global menu_open_up_count
	menu_open_up_count += 1

def on_board_expanding_out(root, data):
	global enable_input
	
	mc = data
	
	song_idx = get_cur_song_idx(BOARD_CENTER)
	if song_idx >= 0 and song_idx < len(song_lst):
		song_info = song_lst[song_idx]
		
		# Play Preview here
		preview_player.set_audio(os.path.join(song_info.folder, song_info.wave), song_info.preview_off)
		mc.use_lyric.active = False
		mc.course.gotoAndPlay("oni")
		enable_input = True
		
		update_course(mc.course, song_info)

def on_enter(this):
	global renderer, loader
	global mc_song_select, mc_song_select_submenu
	global song_texture_set, select_song_texture_set
	global SONG_TEX_COORDS_INDEX, SONG_COORDS_INDEX
	global preview_player, inited
	
	if not inited:
		if not NO_RENDER_DEBUG:
			renderer = lm_render_state.CRenderer()
			renderer.init()
			
			loader = lm_loader.CLoader("wii", config.DATA["lm_root"], renderer)
	
			mc_song_select = loader.load_movie("song_select/song_select/song_select.lm")
			mc_song_select.register_callback("initial_animation_end", on_initial_animation_end, mc_song_select.main_movie.board_move)
			mc_song_select.register_callback("menu_open_up_count", on_menu_open_up_count, None)
			mc_song_select.register_callback("board_expanding_out", on_board_expanding_out, mc_song_select.main_movie.board_move.open_board)
		
			song_texture_set = CSongTexture(MAX_BOARD)
			select_song_texture_set = CSongTexture(2)
			
			board_move = mc_song_select.main_movie.board_move
			board_move.don_left_1.active = False
			board_move.don_left_2.active = False
			board_move.don_right_1.active = False
			board_move.don_right_2.active = False
			
			for i in xrange(MAX_BOARD):
				board = getattr(board_move, "song_board_%d" % i)
				board.title.add_drawable(CSongTitleRenderer(song_texture_set, i), 0)
				
			open_board = board_move.open_board
			open_board.title.add_drawable(CSongTitleRenderer(select_song_texture_set, 0), 0)
			open_board.full_title.add_drawable(CSongTitleRenderer(select_song_texture_set, 1), 0)
				
			setup_viewport()
			
			preview_player = CPreviewPlayer(30)
		
		build_song_lst()
		inited = True
	
	preview_player.is_paused = False
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
	preview_player.pause()
	mc_song_select.main_movie.board_move.open_board.gotoAndPlay("wait")

def on_key_press(symbol, modifiers):
	if not enable_input: return
	if symbol == pyglet.window.key.J:
		song_idx = get_cur_song_idx(BOARD_CENTER)
		if song_idx >= 0 and song_idx < len(song_lst):
			config.DATA["fumen_file"] = os.path.join(song_lst[song_idx].folder, song_lst[song_idx].tja)
			game_state.set_game_state(game_state.GAME_STATE_ENSO)
	elif symbol == pyglet.window.key.U:
		global cursor_pos
		cursor_pos = (cursor_pos + 1) % (len(song_lst))
		game_state.set_game_state(game_state.GAME_STATE_SONG_SELECT)
	elif symbol == pyglet.window.key.R:
		global cursor_pos
		cursor_pos = (cursor_pos - 1) % (len(song_lst))
		game_state.set_game_state(game_state.GAME_STATE_SONG_SELECT)
