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
fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))
# one frame movieclip can be drawn as a display_list

@window.event
def on_key_press(symbol, modifiers):
	global movieclips, render_state
	if symbol == pyglet.window.key.F:
		movieclips[LEFT_DON].gotoAndPlay("left_don")
		movieclips[MATO].gotoAndPlay("hit_ryo")
		movieclips[HITJUDGE].gotoAndPlay("hit_ryo")
		movieclips[HITEFFECTS].gotoAndPlay("don_s")
	elif symbol == pyglet.window.key.J:
		movieclips[RIGHT_DON].gotoAndPlay("right_don")
		movieclips[MATO].gotoAndPlay("hit_ka")		
		movieclips[HITJUDGE].gotoAndPlay("hit_ka")
		movieclips[HITEFFECTS].gotoAndPlay("don_b")
	elif symbol == pyglet.window.key.R:
		movieclips[LEFT_KATS].gotoAndPlay("left_kats")
		movieclips[MATO].gotoAndPlay("hit_dai_ryo")		
		movieclips[HITEFFECTS].gotoAndPlay("katsu_s")
		movieclips[HITJUDGE].gotoAndPlay("hit_ryo_big")
	elif symbol == pyglet.window.key.U:
		movieclips[RIGHT_KATS].gotoAndPlay("right_kats")
		movieclips[MATO].gotoAndPlay("hit_dai_ka")
		movieclips[HITJUDGE].gotoAndPlay("hit_ka_big")
		movieclips[HITEFFECTS].gotoAndPlay("katsu_b")		
	elif symbol == pyglet.window.key.BRACKETLEFT:
		movieclips[MATO_GOGO].gotoAndPlay("sabi_in")
		movieclips[GAUGE].gotoAndPlay("gage_50")
		movieclips[DANCE_BG].gotoAndPlay("normal_fever")
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_start")
	elif symbol == pyglet.window.key.BRACKETRIGHT:
		movieclips[MATO_GOGO].gotoAndPlay("sabi_out")
		movieclips[GAUGE].gotoAndPlay("gage_47")
		movieclips[DANCE_BG].gotoAndPlay("fever_normal")
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_end")
	elif symbol == pyglet.window.key.ENTER:		
		movieclips[FULLCOMBO].gotoAndPlay("run")
			
	elif symbol == pyglet.window.key.UP:
		movieclips[BUNKI].play()
		movieclips[BUNKI_MOJI].play()
		
	elif symbol == pyglet.window.key.DOWN:
		movieclips[DON].play()
		
	elif symbol == pyglet.window.key._1:
		render_state.enable_statistic(1)
		
	elif symbol == pyglet.window.key._0:
		render_state.enable_statistic(2000)		
		
	elif symbol == pyglet.window.key.ESCAPE:
		pyglet.clock.unschedule(on_draw)
		
def fscommand(event, data):
	print "fscommand(%s, %s)" % (event, data)
	
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
	
	#glClearColor(1, 1, 0, 1)
	#window.clear()
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	render_state.begin()
	
	for movieclip in movieclips:
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

NUM_MOVIECLIP = 20
(
DANCE_BG, 
ENSO_UP_BG, 
BG_SAB_EFFECTI,
COURSE, 
DON,
LANE, 
HITEFFECTS, 
BUNKI,
MATO_GOGO, 
BUNKI_MOJI, 
MATO, 
FULLCOMBO,
TAIKO, 
COMBO,
HITJUDGE, 
LEFT_DON, 
LEFT_KATS, 
RIGHT_DON, 
RIGHT_KATS, 
GAUGE
) = range(NUM_MOVIECLIP)

# Build up scene
movieclips = [None] * NUM_MOVIECLIP

movieclips[DANCE_BG] = load_movie("DANCE_BG_MIKU.LM")
movieclips[ENSO_UP_BG] = load_movie("ENSO_UP_BG_01.LM")
movieclips[COURSE] = load_movie("COURSE_ONI.LM")
movieclips[LANE] = load_movie("ENSO_LANE.LM")
movieclips[HITEFFECTS] = load_movie("ENSO_HITEFFECTS.LM")
movieclips[TAIKO] = load_movie("ENSO_TAIKO.LM")
movieclips[COMBO] = load_movie("ENSO_COMBO.LM")
movieclips[MATO_GOGO] = load_movie("ENSO_MATO_GOGO.LM")
movieclips[MATO] = load_movie("ENSO_MATO.LM")
movieclips[HITJUDGE] = load_movie("ENSO_HITJUDGE.LM")
movieclips[LEFT_DON] = load_movie("ENSO_LEFT_DON.LM")
movieclips[LEFT_KATS] = load_movie("ENSO_LEFT_KATS.LM")
movieclips[RIGHT_DON] = load_movie("ENSO_RIGHT_DON.LM")
movieclips[RIGHT_KATS] = load_movie("ENSO_RIGHT_KATS.LM")
movieclips[GAUGE] = load_movie("GAUGE_DON_E.LM")
movieclips[BUNKI] = load_movie("ENSO_BUNKI.LM")
movieclips[BUNKI_MOJI] = load_movie("ENSO_BUNKI_MOJI.LM")
movieclips[FULLCOMBO] = load_movie("ENSO_FULLCOMBO.LM")
movieclips[BG_SAB_EFFECTI] = load_movie("BG_SAB_EFFECTI.LM")
movieclips[DON] = load_movie("DON_COS00_DIET.LM", (64, 42))

# Thus we use shader to do cxform, this is not needed
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

glEnable(GL_BLEND)

# Turn off texture filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

gc.disable()	
pyglet.app.run()