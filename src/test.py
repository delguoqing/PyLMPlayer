# -*- coding: gbk -*-

import cProfile
import pyglet
from pyglet.gl import *
from ctypes import *

from lm import lm_loader

from lm.type import lm_type_color
from lm.type import lm_type_mat

from lm.drawable import lm_shape_solid_color
from lm.drawable import lm_shape_clipped_image
from lm.drawable import lm_shape_tiled_image
from lm.drawable import lm_sprite

# standard resolution for wii? May be I should start with pspdx, which has simpler actionscript
window = pyglet.window.Window(480, 272)
fps_display = pyglet.clock.ClockDisplay()

# one frame movieclip can be drawn as a display_list

@window.event
def on_key_press(symbol, modifiers):
	if symbol == pyglet.window.key.SPACE:
		global movieclip
		movieclip.play()


def on_draw2():
	window.clear()
	fps_display.draw()

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
	
#	glClearColor(1, 1, 0, 1)
	window.clear()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	global movieclip, ctx
	
	# Bind The overall Texture
	tex = ctx.img_list.get_val(0)
	glEnable(tex.target)
	glBindTexture(tex.target, tex.id)
	
	# Draw movieclip
	movieclip.advance()				
	movieclip.draw(movieclip._render_state)

	fps_display.draw()
	
pyglet.clock.schedule(on_draw)

# --------- experiment cases ------------------
ctx = lm_loader.load("../../LMDumper/lm/pspdx/DANCE_BG_14.LM", "C:/png", "pspdx")

movieclip = ctx.get_character(29).instantiate(999, 0, parent=None)
#movieclip.set_matrix(lm_type_mat.CType((256, 64)))
	
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	
#import cProfile
pyglet.app.run()


#pyglet.app.run()