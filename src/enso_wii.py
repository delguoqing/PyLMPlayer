# -*- coding: gbk -*-

import sys
import os
import cProfile
import pyglet
import gc
import random
import enso_scene_wii
from enso_layout_wii import *

from pyglet.gl import *
from ctypes import *

from lm import lm_loader
from lm.extensions import lm_render_state

# standard resolution for psp
window = pyglet.window.Window()
window.maximize()
window.set_size(window.width, window.width * enso_scene_wii.HEIGHT / enso_scene_wii.WIDTH)
fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))

# setting up config
if len(sys.argv) > 2:
	cfg = __import__(sys.argv[2])
else:
	cfg = __import__("enso_cfg_wii")

###################################
# Game Logic
###################################
scr_shot_id = 0
fumen_started = False

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
	global movieclips, fumen_mgr
	global music_player
	global fumen_started
	
	# Music startup
	fumen_off = fumen_mgr._state.offset
	if not music_player.playing:
		if fumen_off < 0:
			fumen_started = True
		if fumen_off >= 0:
			music_player.seek(fumen_off / 1000.0)
			music_player.play()
	elif not fumen_started and music_player.time * 1000.0 >= fumen_off:
		fumen_started = True
		fumen_mgr._state.offset = music_player.time * 1000.0
		
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
		#if movieclip not in (movieclips[SONG_NAME], ): continue
		movieclip.update(render_state)
			
	render_state.end()
	
	# Fumen advance
	if fumen_started:
		fumen_mgr._state.offset += dt * 1000.0
		
	glScalef(1.0, -1.0, 1.0)		
	# Draw song name
	song_name_label.draw()
	
	# Draw fps
	#glTranslatef(80.0, -224.0, 1.0)
	#fps_display.draw()
	
pyglet.clock.schedule(on_draw)

###################################
# Setup code
###################################

# global render state control
render_state = lm_render_state.CRenderer()
render_state.init()

loader = lm_loader.CLoader("wii", cfg.LM_PACK_ROOT, render_state)

movieclips = enso_scene_wii.build_scene(cfg, loader, sys.argv[1])
fumen_mgr = movieclips[ONPS]
fumen_mgr.reset(enso_scene_wii)
song_name = fumen_mgr.get_song_name()
pyglet.font.add_directory("../font")
pyglet.resource.path.append(os.path.split(sys.argv[1])[0])
pyglet.resource.path.append("../snd")
pyglet.resource.reindex()

song_name_label = pyglet.text.Label(song_name, "DFKanTeiRyu-W11", color=(255, 255, 255, 255),
	x=630, y=-240, width=640, height=35, anchor_x="right", anchor_y="center", halign="right",
	font_size=20)

# Load WAVE
audio_file = fumen_mgr.get_audio_file()
music = pyglet.resource.media(audio_file, streaming=False)
music_player = music.play()
music_player.pause()
music_player.volume = fumen_mgr._fumen.header["SONGVOL"] / 100.0

# Load SE
enso_scene_wii.dong = pyglet.resource.media("dong.wav", streaming=False)
enso_scene_wii.ka = pyglet.resource.media("ka.wav", streaming=False)
	
# Texture env
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

# Turn off texture filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

pyglet.app.run()
