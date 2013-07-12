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
		self.star = min(10, star)
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
		self._textures = collections.deque([(None, None)] * num_slot)
		self.tex_coords = -1
		self.coords = -1
		
	def set_texture(self, slot, image_file):
		old_image, old_image_file = self._textures[slot]
		if image_file == "":
			self._textures[slot] = (None, None)
		elif image_file != old_image_file:
			self._textures[slot] = (pyglet.image.load(image_file), image_file)
	
	def get_texture(self, slot):
		ret, file_path = self._textures[slot]
		if ret is not None:
			ret = ret.get_texture()
			if self.tex_coords < 0:
				global renderer
				self.coords = renderer.reg_coords(-0.5*ret.width, -0.5*ret.height, 0.5*ret.width, -0.5*ret.height, 0.5*ret.width, 0.5*ret.height, -0.5*ret.width, 0.5*ret.height)
				self.tex_coords = renderer.reg_coords(0.0, ret.tex_coords[7], ret.tex_coords[3], ret.tex_coords[7], ret.tex_coords[3], 0.0, 0.0, 0.0)
		return ret
	
	def shift_left(self):
		self._textures.popleft()
		self._textures.append((None, None))
		
	def shift_right(self):
		self._textures.pop()
		self._textures.appendleft((None, None))
	
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
		if self.is_paused: return
		self.is_paused = True
		if self.player.playing:
			self.player.pause()
			
	def resume(self):
		if not self.is_paused: return
		self.is_paused = False
		self.accu_t = 0
	
	def set_audio(self, wave, preview_off):
		if wave == self.now_playing_wave:
			return
			
		if self.player.playing:
			self.player.pause()
				
		print "preview off = %f" % preview_off
		if wave:
			self.preview_off = preview_off
			source = pyglet.media.load(wave)
			self.player.queue(source)
			if self.now_playing_wave:
				self.player.next()
			self.player.seek(self.preview_off)
			self.player.play()
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
				renderer.push_state(-1, -1, self.matrix_index, 0)
				renderer.draw_image(texture.target, texture.id, self.texture_set.coords, self.texture_set.tex_coords)
				renderer.pop_state()				

SONG_ROOT = r"../song"
ALL_GENRE_NAME = ["j-pop", "animation", "variety", "classic", "namco", "doyo", "game", "random"]
ALL_DIFF_NAME = ["easy", "normal", "hard", "mania"]
GENRE_NAME_2_ID = dict([(genre_name, genre_name_idx) for genre_name_idx, genre_name in enumerate(ALL_GENRE_NAME)])
MAX_BOARD = 11
BOARD_CENTER = 0
BOARD_ID_2_TEX_ID = [5, 6, 7, 8, 9, 10, 0, 1, 2, 3, 4]

# Mapping course select cursor pos to movieclip label
COURSE_SELECT_CURSOR_POS_BACK = 0
COURSE_SELECT_CURSOR_POS_RECORD = 1
COURSE_SELECT_CURSOR_POS_TONE = 2
COURSE_SELECT_CURSOR_POS_OPTION = 3
COURSE_SELECT_CURSOR_POS_ONI = 4
COURSE_SELECT_CURSOR_POS_HARD = 5
COURSE_SELECT_CURSOR_POS_NORMAL = 6
COURSE_SELECT_CURSOR_POS_EASY = 7
COURSE_SELECT_CURSOR_POS_2_NAME = ["pos0", "pos1", "pos2", "pos3", "pos4oni", "pos5oni", "pos6oni", "pos7oni"]

# How large has the menu been opened up
# Used to recover from open to close
menu_open_up_count = 0
cur_genre = 0
enable_move = False
enable_to_course_select = False
enable_course_select = False
menu_move_direction = ""

#ALL_GENRE_NAME = ["debug"]

NO_RENDER_DEBUG = False
inited = False

renderer = None
loader = None

mc_song_select = None
mc_song_select_submenu = None

song_lst = []
cursor_pos = 6
course_cursor_pos = 0

def build_song_lst_by_genre(genre_name):
	genre_folder = os.path.join(SONG_ROOT, genre_name)
	glob_pattern = os.path.join(genre_folder, "*/*.tja")
	reader = tja_reader.CReader()
	header = tja_header.CData()
	genre_song_lst = []
	print glob_pattern
	for file_path in glob.glob(glob_pattern):
		print "doing %s" % file_path
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
	
	if cur_genre == genre: return
	# set bg
	bg = mc_song_select.main_movie.bg
	bg.lower.gotoAndPlay("genre%d" % cur_genre)
	bg.upper.gotoAndPlay("genre%d" % genre)
	
	board_move = mc_song_select.main_movie.board_move
	# set genre text
	mc_genre = board_move.genre
	genre_name = ALL_GENRE_NAME[genre]
	
	mc_genre.gotoAndStop(genre_name)
	# set menu title
	board_move.menu_title.gotoAndStop("genre%d" % genre)
	
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
	if board_id <= 5:
		return (cursor_pos + board_id) % ((len(song_lst) + 1))
	else:
		return (cursor_pos + board_id - 11) % (len(song_lst) + 1)
	
def update_board(mc, board_id):
	song_idx = get_cur_song_idx(board_id)
	
	if song_idx > len(song_lst):
		#print "update board %d: back_board" % board_id
		mc.gotoAndPlay("back_board")
	elif song_idx == len(song_lst):
		#print "update board %d: random_board" % board_id
		mc.gotoAndPlay("random_board")
	else:
		song_info = song_lst[song_idx]
		
		#print "update board %d: song_board => %s" % (board_id, song_info.folder)
		mc.gotoAndPlay("song_board")
		mc.crown.active = False
		mc.board.gotoAndPlay("genre%d" % GENRE_NAME_2_ID[song_info.genre])
		
		non_select_texture.set_texture(BOARD_ID_2_TEX_ID[board_id], os.path.join(song_info.folder, "sn_non_select.png"))
		
def update_out_board(mc, board_id):
	song_idx = get_cur_song_idx(board_id)
	
	if song_idx > len(song_lst):
		#print "update out board %d: back_board" % board_id
		mc.gotoAndPlay("back_board")
	elif song_idx == len(song_lst):
		#print "update out board %d: random_board" % board_id
		mc.gotoAndPlay("random_board")
	else:
		song_info = song_lst[song_idx]
		
		#print "update out board %d: song_board => %s" % (board_id, song_info.folder)
		mc.gotoAndPlay("song_board")
		#mc.board.gotoAndPlay("genre%d" % GENRE_NAME_2_ID[song_info.genre])
		out_title.texture_idx = BOARD_ID_2_TEX_ID[board_id]		
		
def update_open_board(mc):
	song_idx = get_cur_song_idx(BOARD_CENTER)
	
	if song_idx > len(song_lst):
		mc.gotoAndPlay("back_board")
		#print "update open board: back_board"
	elif song_idx == len(song_lst):
		mc.gotoAndPlay("random_board")
		#print "update open board: random_board"
	else:
		song_info = song_lst[song_idx]
		#print "update open board: song_board => %s" % song_info.folder
		#set_genre(GENRE_NAME_2_ID[song_info.genre])
		select_short_texture.set_texture(0, os.path.join(song_info.folder, "sn_select_short.png"))
		select_full_texture.set_texture(0, os.path.join(song_info.folder, "sn_select_full.png"))			

def update_course(mc, song_info):
	mc.gotoAndPlay("oni")
	for diff_idx, diff_info in enumerate(song_info.diff_lst):
		mc_course_wise = mc.get_drawable(3 - diff_idx)
		if mc_course_wise is None: continue
		mc_star = mc_course_wise.star
		if diff_info is None:
			mc_course_wise._visible = False
		else:
			mc_course_wise._visible = True
			mc_star.gotoAndStop("star%d" % diff_info.star)
			
def on_initial_animation_end(root, data):
	global enable_move, enable_to_course_select
	global menu_open_up_count
	
	menu_open_up_count = 15
	enable_move = True
	enable_to_course_select = True
	
	song_idx = get_cur_song_idx(BOARD_CENTER)
	
	mc = data
	
	if song_idx > len(song_lst):	# invalid board
		mc.gotoAndPlay("close%d" % menu_open_up_count)
		mc.open_board.gotoAndPlay("close%d" % menu_open_up_count)
	elif song_idx == len(song_lst):
		mc.gotoAndPlay("close%d" % menu_open_up_count)
		mc.open_board.gotoAndPlay("r_close%d" % menu_open_up_count)
	else:
		song_info = song_lst[song_idx]
		mc.gotoAndPlay("select")
		mc.hiscore.active = False

def on_menu_open_up_count(root, data):
	global menu_open_up_count
	global enable_to_course_select
	menu_open_up_count += 1
	if menu_open_up_count >= 15:
		enable_to_course_select = True

def on_board_expanding_out(root, data):
	
	mc = data
	
	song_idx = get_cur_song_idx(BOARD_CENTER)
	if song_idx >= 0 and song_idx < len(song_lst):
		song_info = song_lst[song_idx]
		
		# Play Preview here
		preview_player.set_audio(os.path.join(song_info.folder, song_info.wave), song_info.preview_off)
		mc.use_lyric.active = False
		
		update_course(mc.course, song_info)

def move_board(d):
	global enable_move, enable_to_course_select
	global menu_move_direction
	
	menu_move_direction = d
	enable_move = False
	enable_to_course_select = False

	board_move = mc_song_select.main_movie.board_move
	song_idx = get_cur_song_idx(cursor_pos)
	
	if song_idx == len(song_lst):
		on_song_menu_close_end(mc_song_select, board_move)
	else:
		label_close = "close%d" % menu_open_up_count
	
		open_board = board_move.open_board
		open_board.gotoAndPlay(label_close)
	
		preview_player.set_audio(None, -1)
	
		board_move.gotoAndPlay(label_close)
	
def on_song_menu_close_end(root, data):
	global cursor_pos
	global menu_open_up_count
	global enable_move	
	
	mc_board_move = data
	dir_prefix = ""
	if menu_move_direction == "R":
		non_select_texture.shift_left()
		cursor_pos = (cursor_pos + 1) % (len(song_lst) + 1)
		for i in xrange(MAX_BOARD):
			update_board(getattr(mc_board_move, "song_board_%d" % i), i)
		update_out_board(mc_board_move.out_board, 10)
		update_open_board(mc_board_move.open_board)
		mc_board_move.gotoAndPlay("right_move")
		dir_prefix = "L_"
	elif menu_move_direction == "L":
		non_select_texture.shift_right()
		cursor_pos = (cursor_pos - 1) % (len(song_lst) + 1)
		for i in xrange(MAX_BOARD):
			update_board(getattr(mc_board_move, "song_board_%d" % i), i)
		update_out_board(mc_board_move.out_board, 1)
		update_open_board(mc_board_move.open_board)		
		mc_board_move.gotoAndPlay("left_move")
		dir_prefix = "R_"
	
	menu_open_up_count = 0
	enable_move = True
	
	# Update genre
	song_idx = get_cur_song_idx(BOARD_CENTER)
	
	if song_idx >= 0 and song_idx < len(song_lst):
		song_info = song_lst[song_idx]
		set_genre(GENRE_NAME_2_ID[song_info.genre], dir_prefix)
	else:
		set_genre(GENRE_NAME_2_ID["random"], dir_prefix)
	
# init select pos
def on_course_menu_start(root, data):
	global enable_course_select
	enable_course_select = True
	mc_course_menu = mc_song_select.main_movie.board_move.open_board.course_select
	mc_course_cursor = mc_course_menu.cursor1p
	mc_course_cursor.gotoAndStop(COURSE_SELECT_CURSOR_POS_2_NAME[course_cursor_pos])
	mc_course_cursor.move_cursor.cursor.gotoAndStop("cur_1000")
	
def on_course_menu_init(root, data):
	global course_cursor_pos
	mc_course_menu = mc_song_select.main_movie.board_move.open_board.course_select
	mc_boards = mc_course_menu.menu
	song_idx = get_cur_song_idx(BOARD_CENTER)
	song_info = song_lst[song_idx]
	
	course_cursor_pos = None
	for diff_idx, diff_info in enumerate(song_info.diff_lst):
		course_board = getattr(mc_boards, "board_%s" % ALL_DIFF_NAME[diff_idx])
		if diff_info is not None:
			course_cursor_pos = 7 - diff_idx			
			course_board._visible = True
		else:
			course_board._visible = False

def on_song_menu_select_start(root, data):
	global menu_move_direction

	mc_board_move = data
	if cursor_pos >= 0 and cursor_pos < len(song_lst):
		mc_board_move.gotoAndPlay("open")
		
def on_course_menu_to_song_select(root, data):
	global enable_course_select
	
	mc_board_move = root.main_movie.board_move
	mc_board_move.gotoAndPlay("restart")
	
	enable_course_select = False

def on_course_select_decide():
	if course_cursor_pos == COURSE_SELECT_CURSOR_POS_BACK:
		on_course_menu_to_song_select(mc_song_select, None)
	elif course_cursor_pos == COURSE_SELECT_CURSOR_POS_RECORD:
		pass
	elif course_cursor_pos == COURSE_SELECT_CURSOR_POS_TONE:
		pass
	elif course_cursor_pos == COURSE_SELECT_CURSOR_POS_OPTION:
		pass
	else:
		song_idx = get_cur_song_idx(BOARD_CENTER)
		if song_idx >= 0 and song_idx < len(song_lst):
			song_info = song_lst[song_idx]
			config.DATA["fumen_file"] = os.path.join(song_info.folder, song_lst[song_idx].tja)
			config.DATA["course_idx"] = song_info.diff_lst[7 - course_cursor_pos].idx
			game_state.set_game_state(game_state.GAME_STATE_ENSO)
			
def move_course_cursor(dir):
	global course_cursor_pos
	
	if not enable_course_select:
		return
	delta = ("L", "R").index(dir) * 2 - 1
	next_pos = course_cursor_pos
	while True:
		next_pos = (next_pos + delta) % len(COURSE_SELECT_CURSOR_POS_2_NAME)
		if next_pos >= COURSE_SELECT_CURSOR_POS_ONI and next_pos <= COURSE_SELECT_CURSOR_POS_EASY:
			song_idx = get_cur_song_idx(BOARD_CENTER)
			song_info = song_lst[song_idx]
			if song_info.diff_lst[7 - next_pos] is not None:
				break
		else:
			break
	if next_pos != course_cursor_pos:
		mc_course_menu = mc_song_select.main_movie.board_move.open_board.course_select
		mc_course_cursor = mc_course_menu.cursor1p
		mc_course_cursor.gotoAndStop(COURSE_SELECT_CURSOR_POS_2_NAME[next_pos])
		course_cursor_pos = next_pos
	
def on_enter(this):
	global renderer, loader
	global mc_song_select, mc_song_select_submenu
	global SONG_TEX_COORDS_INDEX, SONG_COORDS_INDEX
	global preview_player, inited
	
	if not inited:
		if not NO_RENDER_DEBUG:
			renderer = lm_render_state.CRenderer()
			renderer.init()
			
			loader = lm_loader.CLoader("wii", config.DATA["lm_root"], renderer)
			
			init_song_select_movie()
				
			setup_viewport()
			
			preview_player = CPreviewPlayer(300)
		
		build_song_lst()
		
		init_song_boards()
		
		inited = True
	
	preview_player.resume()
	
	board_move = mc_song_select.main_movie.board_move
	board_move.gotoAndPlay("start")
	
	# loop start scrolling
	mc_song_select.main_movie.bg.gotoAndPlay("loop")
	
def init_song_select_movie():
	global mc_song_select
	global non_select_texture, select_short_texture, select_full_texture
	global out_title
	
	contex = loader.get_contex("song_select/song_select/song_select.lm")

	non_select_texture = CSongTexture(MAX_BOARD)
	select_short_texture = CSongTexture(1)
	select_full_texture = CSongTexture(1)
	for i in xrange(MAX_BOARD):
		song_title = CSongTitleRenderer(non_select_texture, BOARD_ID_2_TEX_ID[i])
		contex.set_named_instance("song_title_%d" % i, song_title)
	out_title = CSongTitleRenderer(non_select_texture, BOARD_ID_2_TEX_ID[BOARD_CENTER])
	short_title = CSongTitleRenderer(select_short_texture, 0)
	long_title = CSongTitleRenderer(select_full_texture, 0)
	contex.set_named_instance("select_title", short_title)
	contex.set_named_instance("out_title", out_title)
	contex.set_named_instance("select_full_title", long_title)
	
	mc_song_select = contex.create_main_movie()
	mc_song_select.register_callback("initial_animation_end", on_initial_animation_end, mc_song_select.main_movie.board_move)
	mc_song_select.register_callback("menu_open_up_count", on_menu_open_up_count, None)
	mc_song_select.register_callback("board_expanding_out", on_board_expanding_out, mc_song_select.main_movie.board_move.open_board)
	mc_song_select.register_callback("_SongMenu_CloseEnd", on_song_menu_close_end, mc_song_select.main_movie.board_move)
	mc_song_select.register_callback("_SongMenu_SelectStart", on_song_menu_select_start, mc_song_select.main_movie.board_move)
	mc_song_select.register_callback("_CourseMenu_init", on_course_menu_init, None)
	mc_song_select.register_callback("_CourseMenu_start", on_course_menu_start, None)

	board_move = mc_song_select.main_movie.board_move
	board_move.don_left_1.active = False
	board_move.don_left_2.active = False
	board_move.don_right_1.active = False
	board_move.don_right_2.active = False
	for i in xrange(MAX_BOARD):
		getattr(board_move, "song_board_%d" % i).title.gotoAndStop("song_title_%d" % i)
	
def init_song_boards():
	global cur_genre
	global mc_song_select
	
	song_idx = get_cur_song_idx(BOARD_CENTER)
	mc_board_move = mc_song_select.main_movie.board_move
	for i in xrange(MAX_BOARD):
		update_board(getattr(mc_board_move, "song_board_%d" % i), i)
	
	if song_idx >= 0 and song_idx < len(song_lst):
		song_info = song_lst[song_idx]
		mc_board_move.open_board.gotoAndPlay("select")
		on_board_expanding_out(mc_song_select, mc_board_move.open_board)
		genre_name = song_info.genre
	else:
		mc_board_move.gotoAndPlay("close0")
		genre_name = "random"
		
	genre_idx = GENRE_NAME_2_ID[genre_name]
	bg = mc_song_select.main_movie.bg
	bg.lower.gotoAndPlay("genre%d" % genre_idx)			
	# set genre text
	mc_genre = mc_board_move.genre
	mc_genre.gotoAndStop(genre_name)
	# set menu title
	mc_board_move.menu_title.gotoAndStop("genre%d" % genre_idx)
	cur_genre = genre_idx
	
	update_open_board(mc_board_move.open_board)
	
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
	preview_player.set_audio(None, -1)
	mc_song_select.main_movie.board_move.open_board.gotoAndPlay("wait")

def on_key_press(symbol, modifiers):
	global cursor_pos
	global menu_move_direction
	global enable_to_course_select, enable_move
		
	if symbol == pyglet.window.key.J:
		if enable_to_course_select:
			enable_to_course_select = False
			enable_move = False
			mc_song_select.main_movie.board_move.gotoAndPlay("fadeout")
		elif enable_course_select:
			on_course_select_decide()
	elif symbol == pyglet.window.key.U:
		if enable_move:
			move_board("R")
		elif enable_course_select:
			move_course_cursor("R")
	elif symbol == pyglet.window.key.R:
		if enable_move:
			move_board("L")
		elif enable_course_select:
			move_course_cursor("L")