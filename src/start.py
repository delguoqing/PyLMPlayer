import sys
import pyglet
import gcrandom
from pyglet.gl import *

import scn_song_select
import scn_enso
import scn_dummy

WINDOW_WIDTH = 856
WINDOW_HEIGHT = 480

GAME_STATE_NULL = 0
GAME_STATE_SONG_SELECT = 1
GAME_STATE_ENSO = 2
GAME_STATE_RESULT = 3

STATE_MODULES = {
	GAME_STATE_NULL: scn_dummy,
	GAME_STATE_SONG_SELECT: scn_song_select,
	GAME_STATE_ENSO: scn_enso,
	GAME_STATE_RESULT: scn_dummy,
}

window = None
fps_display = None
cur_state = None
active_m = None

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
	active_m.on_key_press(symbol, modifiers)
	
def on_update(dt):
	# switch off some expensive operation
	glShadeModel(GL_FLAT)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_DITHER)
	
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-108, enso_scene_wii.WIDTH-108, enso_scene_wii.HEIGHT, 0, -1, 1)

	# update working module
	active_m.on_update(dt)

###################################
# Setup code
###################################
def set_game_state(state):
	global cur_state
	global active_m
	
	if state == cur_state: return
	
	m_old = STATE_MODULES[cur_state]
	m_new = STATE_MODULES[state]
	
	if m_old is not None:
		m_old.on_exit()	
	m_new.on_enter()

	cur_state = state
	active_m = m_new
	
def logic_setup():
	set_game_state(GAME_STATE_SONG_SELECT)
	
	# Disable some global python setting
	gc.disable()
	sys.setcheckinterval(1000000)
	
	# set up timer
	pyglet.clock.schedule(on_update)
	
def graphic_setup():
	global window
	global fps_display
	
	window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
	fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))
	
	# Texture env
	glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

	# Turn off texture filter
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

def startup():
	graphic_setup()
	logic_setup()
	pyglet.app.run()