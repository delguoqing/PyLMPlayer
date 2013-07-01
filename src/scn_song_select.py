import os
import random
import pyglet
from pyglet.gl import *

from lm import lm_consts
from lm import lm_loader
from lm.extensions import lm_render_state

import config

inited = False

renderer = None
loader = None

mc_song_select = None
mc_song_select_submenu = None

SONG_NAME_SIZE_NON_SELECT = (48, 296)
SONG_NAME_SIZE_SELECT_FULL = (80, 296)

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