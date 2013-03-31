# -*- coding: gbk -*-

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
window = pyglet.window.Window(480*2, 272*2)
fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 480, 272, 0, -1, 1)
	
#	glClearColor(1, 1, 0, 1)
	window.clear()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	global movieclip
	movieclip.draw()

	fps_display.draw()
	
def update(dt):
	global movieclip
	movieclip.advance()
pyglet.clock.schedule_interval(update, 0.01666666666)

# --------- experiment cases ------------------

ctx = lm_loader.load("../../LMDumper/lm/pspdx/DANCE_IDOL_HIBIKI.LM", "C:/png", "pspdx")
movieclip = ctx.get_character(40).instantiate(parent=None)
movieclip.set_matrix(lm_type_mat.CType((100, 200)))
	
pyglet.app.run()