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
window = pyglet.window.Window(480 * 2, 272 * 2)
# A texture for test
texture = pyglet.resource.texture('tmp/player_select_bg_001.png')

@window.event
def on_draw():
	global x, root, sprite, sprites
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 480, 272, 0, -1, 1)
	
#	glClearColor(1, 1, 0, 1)
	window.clear()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

#	glTranslatef(x, 0, 0)	
#	sprite.draw()
	
	for _s in sprites:
		_s.draw()
	root.draw()
	

def update(dt):
	global x
	x = x - 50.0 * dt
	if x <= -480.0:
		x += 480.0
pyglet.clock.schedule(update)

# --------- experiment cases ------------------
	
def create_sprite():
	
	asprite = lm_sprite.CDrawable(10)
	matrix = lm_type_mat.CType((-24, 0))
	asprite.set_matrix(matrix)
	
	for i in xrange(10):
		coords = [96*i, 0, 0, 0, 96*i+128, 0, 1, 0, 96*i+128, 256, 1, 1	, 96*i, 256, 0, 1]
		shape = lm_shape_clipped_image.CDrawable(texture, coords)
		asprite.add_drawable(shape, i)
	
	return asprite

def create_tamashii_gauge_E():
	_load = pyglet.resource.texture
	_ctor = lm_shape_clipped_image.CDrawable
	_ctor2 = lm_sprite.CDrawable
	_mat = lm_type_mat.CType
	_col = lm_type_color.CType
	
	root = _ctor2(4)
	
	p0 = _load("tmp/gauge_DropShadow_E.png")
	t0 = [
		0, 0, 0, 0,
		512, 0, 1, 0,
		512, 64, 1, 1,
		0, 64, 0, 1
	]
	s0 = _ctor(p0, t0)
	spr0 = _ctor2(1)
	spr0.add_drawable(s0, 0)
	spr0.set_cxform(None, _col(1, 1, 1, 0.5))
	
	p1 = _load("tmp/gauge_base_E.png")
	t1 = [
		0, 0, 0, 0,
		256, 0, 1, 0,
		256, 32, 1, 1,
		0, 32, 0, 1
	]
	s1 = _ctor(p1, t1)
	spr1 = _ctor2(1)
	spr1.add_drawable(s1, 0)
	spr1.set_matrix(_mat((183, 6)))
	
	p2 = _load("tmp/gauge_frame_E.png")
	t2 = [
		0, 0, 0, 0,
		256, 0, 1, 0,
		256, 32, 1, 1,
		0, 32, 0, 1
	]
	s2 = _ctor(p2, t2)
	spr2 = _ctor2(1)
	spr2.add_drawable(s2, 0)
	spr2.set_matrix(_mat((183, 6)))
	
	p3 = _load("tmp/gauge_tamashii.png")
	t3 = [
		-32, -32, 0, 0,
		32, -32, 1, 0,
		32, 32, 1, 1,
		-32, 32, 0, 1
	]
	s3 = _ctor(p3, t3)
	spr3 = _ctor2(1)
	spr3.add_drawable(s3, 0)
	spr3.set_matrix(_mat((447, 32)))
	
	root.add_drawable(spr0, 0)
	root.add_drawable(spr1, 1)
	root.add_drawable(spr2, 2)
	root.add_drawable(spr3, 3)
	
	return root
	
sprite = create_sprite()
root = create_tamashii_gauge_E()
x = 0

ctx = lm_loader.load("../../LMDumper/lm/pspdx/PLAYER_SELECT_BG.LM", "C:/png", "pspdx")
ctx2 = lm_loader.load("../../LMDumper/lm/pspdx/DANCE_TORA_01.LM", "C:/png", "pspdx")
sprites = [
	ctx.get_character(i).instantiate() for i in (1, 3, 6, 8)
] + [
	ctx2.get_character(i).instantiate() for i in (1, 3, 5, 7, 9)
]
	

pyglet.app.run()