import os
import glob
import random
import pyglet
from pyglet.gl import *
from tja import tja_header, tja_reader

from lm import lm_consts
from lm import lm_loader
from lm.extensions import lm_render_state

import config

class CDiffInfo(object):
	def __init__(self, idx, rank, has_bunki):
		self.idx = idx
		self.rank = rank
		self.has_bunki = has_bunki
	
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

SONG_ROOT = r"../song"
ALL_GENRE_NAME = ["anime", "classic", "j-pop", "game", "namco", "variety"]

inited = False

renderer = None
loader = None

mc_song_select = None
mc_song_select_submenu = None

song_lst = []

def build_song_lst_by_genre(genre_name):
	genre_folder = os.path.join(SONG_ROOT, genre_name)
	glob_pattern = os.path.join(SONG_ROOT, "*/*.tja")
	reader = tja_reader.CReader()
	header = tja_header.CData()
	genre_song_lst = []
	for file_path in glob.glob(glob_pattern):
		reader.set_file(file_path)
		header.reset()
		
		diff_lst = [None, None, None, None]
		folder, tja = os.path.split(file_path)
		
		diff_idx = 0
		while not reader.is_eof():
			header.ex_read(reader)
			header.refresh()
			if not header["HAS_FUMEN"]: break
			diff_lst[header["COURSE"]] = CDiffInfo(diff_idx, header["LEVEL"], header["HAS_BUNKI"])
			diff_idx += 1
				
		if diff_idx == 0: continue
		
		wave = header["WAVE"]
		song_vol = header["SONG_VOL"]
		se_vol = header["SE_VOL"]
		preview_off = header["DEMOSTART"]
		
		info = CSongInfo(folder, genre, song_vol, se_vol, wave, preview_off, tja, diff_lst)
		genre_song_lst.append(info)
	reader.close()
	
	return genre_song_lst

def build_song_lst():
	global song_lst
	
	song_lst = []
	for genre_name in ALL_GENRE_NAME:
		song_lst.extend(build_song_lst_by_genre())
	

def set_genre(genre):
	pass

def on_update(dt):
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
			
	renderer.begin()
	mc_song_select.update(renderer)			
	renderer.end()
	
def on_enter(this):
	global renderer, loader
	global mc_song_select, mc_song_select_submenu
	
	if not inited:
		renderer = lm_render_state.CRenderer()
		renderer.init()
		
		loader = lm_loader.CLoader("wii", config.DATA["lm_root"], renderer)
	
		mc_song_select = loader.load_movie("song_select/song_select/song_select.lm")

def on_exit():
	pass

def on_key_press(symbol, modifiers):
	pass