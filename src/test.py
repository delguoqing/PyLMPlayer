# -*- coding: gbk -*-

import pyglet
from pyglet.gl import *
from ctypes import *

# standard resolution for wii?
window = pyglet.window.Window(640, 480)
# A texture for test
texture = pyglet.resource.texture('cos_003_1p/noname_0.png')

@window.event
def on_draw():
	window.clear()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
def setup():
	# change default pyglet setting, for a origin at left top corner
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, window.width, window.height, 0, -1, 1)
	
setup()
pyglet.app.run()

# --------- experiment cases ------------------