# -*- coding: gbk -*-

import sys
import os
import cProfile
import pyglet
import gc
import random
import enso_cfg_wii
import enso_scene_wii

from enso_layout_wii import *
from pyglet.gl import *
from ctypes import *

from lm import lm_loader

from lm.drawable import lm_render_state

# standard resolution for psp
window = pyglet.window.Window(enso_scene_wii.WIDTH, enso_scene_wii.HEIGHT)
fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))

###################################
# Game Logic
###################################
scr_shot_id = 0

@window.event
def on_key_press(symbol, modifiers):
	global movieclips, render_state
	if symbol == pyglet.window.key.F:
		movieclips[ONPS].add_key(1)
	elif symbol == pyglet.window.key.J:
		movieclips[ONPS].add_key(2)
	elif symbol == pyglet.window.key.R:
		movieclips[ONPS].add_key(4)
	elif symbol == pyglet.window.key.U:
		movieclips[ONPS].add_key(8)
		
	elif symbol == pyglet.window.key._1:
		render_state.enable_statistic(1)
		
	elif symbol == pyglet.window.key.ESCAPE:
		pyglet.clock.unschedule(on_draw)
			
	elif symbol == pyglet.window.key.F10:
		global scr_shot_id
		pyglet.image.get_buffer_manager().get_color_buffer().save('enso%d.jpg' % scr_shot_id)
		scr_shot_id += 1
	
###################################
# Rendering
###################################
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
	glOrtho(-108, enso_scene_wii.WIDTH-108, enso_scene_wii.HEIGHT, 0, -1, 1)
	
	#glClearColor(1, 1, 1, 1)
	window.clear()
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	render_state.begin()
	
	for movieclip in movieclips:
		if movieclip is None: continue
		#if movieclip in (movieclips[ONPS], ): continue
		#if movieclip not in (movieclips[DON], ): continue
		movieclip.update(render_state)
	
	render_state.end()
			
	# Draw fps
	#glScalef(1.0, -1.0, 1.0)
	#glTranslatef(0.0, -64.0, 1.0)
	#fps_display.draw()
	
pyglet.clock.schedule(on_draw)

###################################
# Setup code
###################################

# global render state control
render_state = lm_render_state.CObj()

movieclips = enso_scene_wii.build_scene(enso_cfg_wii, sys.argv[1])
movieclips[ONPS].reset(enso_scene_wii)

# Texture env
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

# Turn off texture filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

pyglet.app.run()