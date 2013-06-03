# -*- coding: gbk -*-

import sys
import os
import cProfile
import pyglet
import gc
import random

from pyglet.gl import *
from ctypes import *

sys.path.append("..")
sys.path.append("../..")
import lm_loader
import lm_render_state


# standard resolution for psp
window = pyglet.window.Window(480, 272, vsync=True)
fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))

###################################
# Game Logic
###################################
scr_shot_id = 0

@window.event
def on_key_press(symbol, modifiers):
	global mc
	if symbol == pyglet.window.key.ESCAPE:
		pyglet.clock.unschedule(on_draw)
			
	elif symbol == pyglet.window.key.F10:
		global scr_shot_id
		pyglet.image.get_buffer_manager().get_color_buffer().save('enso%d.jpg' % scr_shot_id)
		scr_shot_id += 1
		
	elif symbol == pyglet.window.key.Q:
		mc.gotoAndPlay("normal_fever")
	elif symbol == pyglet.window.key.W:
		mc.gotoAndPlay("fever_normal")
###################################
# Rendering
###################################
def on_draw(dt):
	# switch off some expensive operation
	glShadeModel(GL_FLAT)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_DITHER)
	
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 480, 272, 0, -1, 1)
	
	glClearColor(0, 0, 0, 1)
	window.clear()
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	render_state.begin()
	mc.update(render_state)
	render_state.end()
			
	# Draw fps
	glScalef(1.0, -1.0, 1.0)
	glTranslatef(0.0, -64.0, 1.0)
	fps_display.draw()
	
pyglet.clock.schedule(on_draw)

###################################
# Setup code
###################################

# global render state control
render_state = lm_render_state.CRenderer()
render_state.init()
#render_state.reg_mat(10.0, 10.0, 1.0, 1.0, 0.0, 0.0)
#render_state.reg_color(1.0, 1.0, 1.0, 1.0)
#render_state.reg_color(0.0, 0.0, 0.0, 0.0)
#render_state.reg_coords(0.0, 16.0, 128.0, 16.0, 128.0, 0.0, 0.0, 0.0)
#render_state.reg_coords(0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0)

loader = lm_loader.CLoader("pspdx", "../../../packages", render_state)
mc = loader.load_movie(r"pack121/DANCE_BG_IDOL.LM")

# Texture env
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

# Turn off texture filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

pyglet.app.run()