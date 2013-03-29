# -*- coding: gbk -*-

import pyglet
from pyglet.gl import *
from ctypes import *

from lm.type import lm_type_color
from lm.type import lm_type_mat

from lm.drawable import lm_shape_solid_color
from lm.drawable import lm_shape_clipped_image
from lm.drawable import lm_shape_tiled_image
from lm.drawable import lm_sprite

# standard resolution for wii? May be I should start with pspdx, which has simpler actionscript
window = pyglet.window.Window(480 * 2, 272 * 2)
# A texture for test
texture = pyglet.resource.texture('tmp/player_select_bg_001.png')

@window.event
def on_draw():
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 480, 272, 0, -1, 1)
	
	window.clear()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	global x
	x = (x+1) % 480
	glTranslatef(x * 2, 0, 0)	
	create_sprite().draw()

def setup():
	pass
	
# --------- experiment cases ------------------
def create_shape0():
	color = lm_type_color.CType(1.0, 0.0, 0.0, 1.0)
	coords = [0, 0, 0, 0, 100, 0, 1, 0, 100, 100, 1, 1, 0, 100, 0, 1]
	shape = lm_shape_solid_color.CDrawable(color, coords)
	return shape

def create_shape1(texture, coords):
	shape = lm_shape_clipped_image.CDrawable(texture, coords)
	return shape
	
def create_shape2(texture, coords):
	shape = lm_shape_tiled_image.CDrawable(texture, coords)
	return shape
	
def create_sprite():
	
	asprite = lm_sprite.CDrawable(10)
	matrix = lm_type_mat.CType((-360, 0), (1.0, 1.0), (0.0, 0.0))
	asprite.set_matrix(matrix)
	
	for i in xrange(10):
		coords = [96*i, 0, 0, 0, 96*i+128, 0, 1, 0, 96*i+128, 256, 1, 1	, 96*i, 256, 0, 1]
		shape = create_shape1(texture, coords)
		asprite.add_drawable(shape, i)
	
	return asprite

sprite = create_sprite()
x = 0

setup()
pyglet.app.run()