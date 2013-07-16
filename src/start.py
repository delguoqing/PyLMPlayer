import sys
import gc
import random

import pyglet
from pyglet.gl import *

import config
import game_state
from game_state import *

window = None
fps_display = None

def graphic_setup():
	global window
	global fps_display

	cfg = config.DATA

	if cfg["fullscreen"]:
		window = pyglet.window.Window(fullscreen=True)
		cfg["real_wnd_width"], cfg["real_wnd_height"] = window.get_size()
		
		# auto detect widescreen
		ratio = 1.0 * cfg["real_wnd_width"] / cfg["real_wnd_height"]
		_width = ratio * cfg["wnd_height"]
		if _width < cfg["wnd_width"] + 2 * cfg["widescreen_padding"]:
			cfg["widescreen"] = False
	else:
		width = cfg["wnd_width"]
		height = cfg["wnd_height"]
		if cfg["widescreen"]:
			width += cfg["widescreen_padding"] * 2
		
		window = pyglet.window.Window(int(cfg["wnd_scale"]*width), int(cfg["wnd_scale"]*height))
		window.set_location(0, 20)
		cfg["real_wnd_width"], cfg["real_wnd_height"] = int(cfg["wnd_scale"]*width), int(cfg["wnd_scale"]*height)
		
	fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))
	
	# Texture env
	glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

	# Turn off texture filter
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
graphic_setup()

scr_shot_id = 0

###################################
# Game Logic
###################################
def gen_screen_shot():
	global scr_shot_id
	pyglet.image.get_buffer_manager().get_color_buffer().save('scr%d.jpg' % scr_shot_id)
	scr_shot_id += 1

@window.event
def on_key_press(symbol, modifiers):
	if symbol == pyglet.window.key.F10:
		gen_screen_shot()

	# pass to active module
	game_state.active_m.on_key_press(symbol, modifiers)
	
# May be customize here!
def on_resize(width, height):
	pass

def on_update(dt):
	# switch off some expensive operation
	glShadeModel(GL_FLAT)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_DITHER)
	
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	#glClearColor(0, 0, 0, 0)
	#window.clear()
	# update working module
	game_state.active_m.on_update(dt)

	# Draw fps
	#glScalef(1.0, -1.0, 1.0)
	#glTranslatef(80.0, -224.0, 1.0)
	#fps_display.draw()
	
###################################
# Setup code
###################################	
def logic_setup():
	# Disable some global python setting
	gc.disable()
	sys.setcheckinterval(1000000)
	
	# set up timer
	pyglet.clock.schedule(on_update)
	
	# add resource path
	pyglet.font.add_directory("../font")
	pyglet.resource.path.append("../snd")
	pyglet.resource.path.append("../song")
	pyglet.resource.reindex()	
	
	# set begin state
	game_state.set_game_state(config.DATA["start_state"])
	

def startup():
	logic_setup()
	pyglet.app.run()
	
startup()
