# -*- coding: gbk -*-

import sys
import os
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
	global movieclip
	
	if symbol == pyglet.window.key.SPACE:	
		movieclip.play()
	elif symbol == pyglet.window.key.F:
		on_draw(1)

#@window.event
#def on_draw2():
#	pass

def on_draw(dt):
	global movieclip, ctx
	global debug_advance
	
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
	
	
	
	# Bind The overall Texture
	# TODO:
	#	what if more than one texture atlas are used?
	tex = ctx.img_list.get_val(0)
	glEnable(tex.target)
	glBindTexture(tex.target, tex.id)
	
	render_state = movieclip._render_state
	render_state.begin()

#	if movieclip._play_head < 171:
	movieclip.advance()
	
	# Draw movieclip	
	movieclip.draw(render_state)
	
	render_state.end()
	# Draw fps counter
	fps_display.draw()
	
pyglet.clock.schedule(on_draw)


# --------- experiment cases ------------------

img_root = "C:/png"
platform = "pspdx"
filename = os.path.join("../../LMDumper/lm/pspdx/", sys.argv[1])
inst_id = 999
depth = 0

ctx = lm_loader.load(filename, img_root, platform)
char_id = ctx.stage_info.start_character_id


movieclip = ctx.get_character(char_id).instantiate(inst_id, depth, parent=None)
movieclip.char_id = char_id
movieclip.init()
#movieclip.set_matrix(lm_type_mat.CType((256, 64)))

glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

	
#import cProfile
#pyglet.app.run()

#print
#on_draw(1)

pyglet.app.run()

# TODO:
# 1. BLEND MODE
# 2. mask!
# 3. fscommand(used everywhere for callback)
# 4. DANCE_BG_10.LM bubble flashs.
# 5. dance bg 04 mushroom looks better in game???
# 6. Sprite not complete matching together. metedai?dancebg05
# 7. optimization.