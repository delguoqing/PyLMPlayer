# -*- coding: gbk -*-

import sys
import os
import cProfile
import pyglet
import gc

from pyglet.gl import *
from ctypes import *

from lm import lm_loader
from lm import lm_glb

from lm.type import lm_type_color
from lm.type import lm_type_mat

from lm.drawable import lm_sprite
from lm.drawable import lm_render_state

# standard resolution for wii? May be I should start with pspdx, which has simpler actionscript
window = pyglet.window.Window(480, 272)
fps_display = pyglet.clock.ClockDisplay()

# one frame movieclip can be drawn as a display_list

MENU_UME = 1
MENU_TAKE = 2
MENU_MATSU = 3
MENU_ONI = 4


cur_menu = MENU_UME
@window.event
def on_key_press(symbol, modifiers):
	global movieclips, cur_menu, render_state
	if symbol == pyglet.window.key.UP:
		movieclips[BG].mc_bg_000.gotoAndPlay("up_%d_in_oni" % cur_menu)
		movieclips[TOP].diff.gotoAndPlay("up_%d_in_oni" % cur_menu)
				
		movieclips[cur_menu].gotoAndPlay("up_1")
		cur_menu = cur_menu % 4 + 1
		movieclips[cur_menu].gotoAndPlay("up_2")		


	elif symbol == pyglet.window.key.DOWN:
		movieclips[BG].mc_bg_000.gotoAndPlay("down_%d_in_oni" % (6-cur_menu))
		movieclips[TOP].diff.gotoAndPlay("down_%d_in_oni" % (6-cur_menu))
		
		movieclips[cur_menu].gotoAndPlay("down_1")
		cur_menu = cur_menu - 1
		if cur_menu < 1: cur_menu = 4
		movieclips[cur_menu].gotoAndPlay("down_2")

	elif symbol == pyglet.window.key.LEFT:
		movieclips[cur_menu].menu_top.gotoAndPlay("right_move")
		
	elif symbol == pyglet.window.key.RIGHT:
		movieclips[cur_menu].menu_top.gotoAndPlay("left_move")
		
	elif symbol == pyglet.window.key.ENTER:		
		movieclips[cur_menu].menu_top.gotoAndPlay("play")	
		
	elif symbol == pyglet.window.key._1:
		render_state.enable_statistic(1)
		
def fscommand(event, data):
	global cur_menu
	print event, data
	if event == "callback":
		if data == "update_menu_matsu_sbopen_l_b":
			movieclips[cur_menu].menu_top.gotoAndPlay("open")
		elif data == "update_menu_matsu_sbopen_r_b":
			movieclips[cur_menu].menu_top.gotoAndPlay("open")
	
def on_draw(dt):
	global movieclips
	# switch off some expensive operation
	glShadeModel(GL_FLAT)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_DITHER)
	
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 480, 272, 0, -1, 1)
	
	# turn off clear screen, because we will redraw the whole screen
	# every frame.
	# how about blend ?
	#glClearColor(1, 1, 0, 1)
	#window.clear()
	
	glMatrixMode(GL_MODELVIEW)
	
	render_state.begin()
	
	for movieclip in movieclips:
		glLoadIdentity()
		movieclip.update(render_state)

	render_state.end()
		
	# Draw fps
	glScalef(1.0, -1.0, 1.0)
	glTranslatef(0.0, -64.0, 1.0)
	fps_display.draw()
		
pyglet.clock.schedule(on_draw)


# --------- experiment cases ------------------

img_root = "C:/png"
platform = "pspdx"
lm_root = "../../LMDumper/lm/pspdx/"
inst_id = 999
depth = 0

def load_movie(filename, translate=(0, 0)):
	global texture_bin
	
	filename = os.path.join(lm_root, filename)
	ctx = lm_loader.load(filename, img_root, platform, texture_bin)
	ctx.fscommand = fscommand
	char_id = ctx.stage_info.start_character_id
	char_tag = ctx.get_character(char_id)
	movieclip = char_tag.instantiate(inst_id, depth, parent=None)
	movieclip.char_id = char_id
	movieclip.init()
	movieclip.set_matrix(lm_type_mat.CType(translate))
	movieclip.ctx = ctx
	return movieclip

# global render state control
render_state = lm_render_state.CObj()

# global texture bin
texture_bin = pyglet.image.atlas.TextureBin(2048, 2048)

NUM_MOVIECLIP = 6
(
BG,
MENU_UME, 
MENU_TAKE,
MENU_MATSU,
MENU_ONI,
TOP,
) = range(NUM_MOVIECLIP)

# Build up scene
movieclips = [None] * NUM_MOVIECLIP

movieclips[BG] = load_movie("SONG_SELECT_BG.LM")
movieclips[MENU_UME] = load_movie("SONG_SELECT_EASY.LM")
movieclips[MENU_TAKE] = load_movie("SONG_SELECT_NORMAL.LM")
movieclips[MENU_MATSU] = load_movie("SONG_SELECT_HARD.LM")
movieclips[MENU_ONI] = load_movie("SONG_SELECT_ONI.LM")
movieclips[TOP] = load_movie("SONG_SELECT_TOP.LM")

# Thus we use shader to do cxform, this is not needed
#glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

glEnable(GL_BLEND)

# Turn off texture filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

gc.disable()	
pyglet.app.run()