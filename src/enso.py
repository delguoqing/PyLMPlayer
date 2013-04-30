# -*- coding: gbk -*-

import sys
import os
import cProfile
import pyglet
import gc
import random

from pyglet.gl import *
from ctypes import *

from lm import lm_loader
from lm import lm_glb

from lm.type import lm_type_color
from lm.type import lm_type_mat

from lm.drawable import lm_sprite
from lm.drawable import lm_render_state

# standard resolution for wii? May be I should start with pspdx, which has simpler actionscript
window = pyglet.window.Window(480, 272)
fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))
# one frame movieclip can be drawn as a display_list

###################################
# Game Logic
###################################
cur_combo = 0	# current combo
cur_score = 0	# current score
cur_dancer = -1	# current dancer
first_unsync_dancer = -1 # current unsync_dancer
last_unsync_dancer = -1 # last unsync_dancer

def set_combo(combo):

	global movieclips, cur_combo
	if combo < 10:
		movieclips[COMBO].enso_combo.gotoAndPlay("combo0-9")
	elif combo < 100:
		num10 = combo // 10
		num1 = combo - num10 * 10
		movieclips[COMBO].enso_combo.gotoAndPlay("combo10-99")		
		movieclips[COMBO].enso_combo.num1.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].enso_combo.num10.gotoAndPlay("number_%d" % num10)
		
	elif combo < 1000:
		num100 = combo // 100
		num10 = (combo - num100 * 100) // 10
		num1 = combo - num100 * 100 - num10 * 10
		
		movieclips[COMBO].enso_combo.gotoAndPlay("combo100-999color")
		movieclips[COMBO].enso_combo.num1color.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].enso_combo.num10color.gotoAndPlay("number_%d" % num10)
		movieclips[COMBO].enso_combo.num100color.gotoAndPlay("number_%d" % num100)		
		
		_num100 = cur_combo // 100
		if _num100 != num100:
			movieclips[COMBO].enso_combo.cherry.gotoAndPlay("in")
	elif combo < 10000:
		num1000 = combo // 1000
		num100 = (combo - num1000 * 1000) // 100
		num10 = (combo - num1000 * 1000 - num100 * 100) // 10
		num1 = combo - num1000 * 1000 - num100 * 100 - num10 * 10
		
		movieclips[COMBO].enso_combo.gotoAndPlay("combo1000-9999color")
		movieclips[COMBO].enso_combo.num1color.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].enso_combo.num10color.gotoAndPlay("number_%d" % num10)
		movieclips[COMBO].enso_combo.num100color.gotoAndPlay("number_%d" % num100)
		movieclips[COMBO].enso_combo.num1000color.gotoAndPlay("number_%d" % num1000)

		_num1000 = cur_combo // 1000
		_num100 = (cur_combo - _num1000 * 1000) // 100

		if _num100 != num100:
			movieclips[COMBO].enso_combo.cherry.gotoAndPlay("in")
					
	cur_combo = combo
	
def add_score(score):
	set_score(cur_score + score)
	_s = score
	num_10000 = _s // 10000
	_s -= num_10000 * 10000	
	num_1000 = _s // 1000
	_s -= num_1000 * 1000
	num_100 = _s // 100
	_s -= num_100 * 100	
	num_10 = _s // 10
	_s -= num_10 * 10	
	num_1 = _s // 1
	_s -= num_1 * 1	
	mc = movieclips[SCORE_ADD]
	mc.gotoAndPlay(0)
	
	score >= 0 and mc.num_1.gotoAndPlay("number_%d" % num_1)
	score >= 10 and mc.num_10.gotoAndPlay("number_%d" % num_10)
	score >= 100 and mc.num_100.gotoAndPlay("number_%d" % num_100)
	score >= 1000 and mc.num_1000.gotoAndPlay("number_%d" % num_1000)
	score >= 10000 and mc.num_10000.gotoAndPlay("number_%d" % num_10000)

def set_score(score):
	global cur_score
	_s = score
	num_10000000 = _s // 10000000
	_s -= num_10000000 * 10000000
	num_1000000 = _s // 1000000
	_s -= num_1000000 * 1000000
	num_100000 = _s // 100000
	_s -= num_100000 * 100000
	num_10000 = _s // 10000
	_s -= num_10000 * 10000	
	num_1000 = _s // 1000
	_s -= num_1000 * 1000
	num_100 = _s // 100
	_s -= num_100 * 100	
	num_10 = _s // 10
	_s -= num_10 * 10	
	num_1 = _s // 1
	_s -= num_1 * 1	
	mc = movieclips[SCORE_MAIN]
	
	score >= 0 and mc.num_1.gotoAndPlay("number_%d" % num_1)
	score >= 10 and mc.num_10.gotoAndPlay("number_%d" % num_10)
	score >= 100 and mc.num_100.gotoAndPlay("number_%d" % num_100)
	score >= 1000 and mc.num_1000.gotoAndPlay("number_%d" % num_1000)
	score >= 10000 and mc.num_10000.gotoAndPlay("number_%d" % num_10000)
	score >= 100000 and mc.num_100000.gotoAndPlay("number_%d" % num_100000)
	score >= 1000000 and mc.num_1000000.gotoAndPlay("number_%d" % num_1000000)
	score >= 10000000 and mc.num_10000000.gotoAndPlay("number_%d" % num_10000000)
	
	cur_score = score

def add_dancer():
	global cur_dancer, movieclips
	if cur_dancer == -1:
		cur_dancer = DANCER1
	elif cur_dancer > DANCER5:
		cur_dancer -= 1
	else:
		return
	
	# add `cur_dancer`
	movieclips[cur_dancer].gotoAndPlay("in")
	
def remove_dancer():
	global cur_dancer
	if cur_dancer <= DANCER1:
		# remove `cur_dancer`
		movieclips[cur_dancer].gotoAndPlay("out")
		cur_dancer += 1

def on_dancer_in_end(dancer):
	global first_unsync_dancer, last_unsync_dancer, movieclips
	if dancer == DANCER1:	# if it is the first dancer, then start dance at once
		movieclips[dancer].gotoAndPlay("dance")
	else:
		if first_unsync_dancer == -1:
			first_unsync_dancer = dancer
		last_unsync_dancer = dancer

def on_dancer_sync(dancer):
	global first_unsync_dancer, last_unsync_dancer, movieclips
	if first_unsync_dancer != -1:
		sync_to = movieclips[dancer].dancer._play_head
		a, b = first_unsync_dancer, last_unsync_dancer
		first_unsync_dancer = -1
		for dancer in xrange(b, a + 1):
			movieclips[dancer].gotoAndPlay("dance")
			movieclips[dancer].dancer.gotoAndPlay(sync_to)
			
@window.event
def on_key_press(symbol, modifiers):
	global movieclips, render_state
	if symbol == pyglet.window.key.F:
		movieclips[LEFT_DON].gotoAndPlay("left_don")
		movieclips[MATO].gotoAndPlay("hit_ryo")
		movieclips[HITJUDGE].gotoAndPlay("hit_ryo")
		movieclips[HITEFFECTS].gotoAndPlay("don_s")
	elif symbol == pyglet.window.key.J:
		movieclips[RIGHT_DON].gotoAndPlay("right_don")
		movieclips[MATO].gotoAndPlay("hit_ka")		
		movieclips[HITJUDGE].gotoAndPlay("hit_ka")
		movieclips[HITEFFECTS].gotoAndPlay("don_b")
	elif symbol == pyglet.window.key.R:
		movieclips[LEFT_KATS].gotoAndPlay("left_kats")
		movieclips[MATO].gotoAndPlay("hit_dai_ryo")		
		movieclips[HITEFFECTS].gotoAndPlay("katsu_s")
		movieclips[HITJUDGE].gotoAndPlay("hit_ryo_big")
	elif symbol == pyglet.window.key.U:
		movieclips[RIGHT_KATS].gotoAndPlay("right_kats")
		movieclips[MATO].gotoAndPlay("hit_dai_ka")
		movieclips[HITJUDGE].gotoAndPlay("hit_ka_big")
		movieclips[HITEFFECTS].gotoAndPlay("katsu_b")		
	elif symbol == pyglet.window.key.BRACKETLEFT:
		movieclips[MATO_GOGO].gotoAndPlay("sabi_in")
		movieclips[GAUGE].gotoAndPlay("gage_50")
		movieclips[DANCE_BG].gotoAndPlay("normal_fever")
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_start")
		movieclips[FEVER].fever.gotoAndPlay("fever_start")
	elif symbol == pyglet.window.key.BRACKETRIGHT:
		movieclips[MATO_GOGO].gotoAndPlay("sabi_out")
		movieclips[GAUGE].gotoAndPlay("gage_47")
		movieclips[DANCE_BG].gotoAndPlay("fever_normal")
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_end")
		movieclips[FEVER].fever.gotoAndPlay("fever_end")		
	elif symbol == pyglet.window.key.ENTER:		
		movieclips[FULLCOMBO].gotoAndPlay("run")

		
	elif symbol == pyglet.window.key.UP:
		movieclips[BUNKI].play()
		movieclips[BUNKI_MOJI].play()
		add_dancer()		
		
	elif symbol == pyglet.window.key.DOWN:
		movieclips[DON].play()
		remove_dancer()
		
	elif symbol == pyglet.window.key.NUM_ADD:
		set_combo(cur_combo + 1)
		add_score(random.randint(500, 2000))
		
	elif symbol == pyglet.window.key._1:
		render_state.enable_statistic(1)
		
	elif symbol == pyglet.window.key._0:
		render_state.enable_statistic(2000)		
		
	elif symbol == pyglet.window.key.ESCAPE:
		pyglet.clock.unschedule(on_draw)
	
###################################
# Rendering
###################################
def on_draw(dt):
	global movieclips
	# switch off some expensive operation
	glShadeModel(GL_FLAT)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_DITHER)
	
	# change default pyglet setting, for a origin at left top corner
	# do this wheneVer redraw event is triggered!
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 480, 272, 0, -1, 1)
	
#	glClearColor(0, 0, 0, 1)
#	window.clear()
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	render_state.begin()
	
	for movieclip in movieclips:
		movieclip.update(render_state)
	
	render_state.end()
			
	# Draw fps
#	glScalef(1.0, -1.0, 1.0)
#	glTranslatef(0.0, -64.0, 1.0)
#	fps_display.draw()
	
pyglet.clock.schedule(on_draw)

###################################
# Setup code
###################################

img_root = "C:/png"
platform = "pspdx"
lm_root = "../../LMDumper/lm/pspdx/"
inst_id = 999
depth = 0

def load_movie(filename, translate=(0, 0)):
	global texture_bin
	
	filename = os.path.join(lm_root, filename)
	ctx = lm_loader.load(filename, img_root, platform, texture_bin)
	char_id = ctx.stage_info.start_character_id
	char_tag = ctx.get_character(char_id)
	movieclip = char_tag.instantiate(inst_id, depth, parent=None)
	movieclip.char_id = char_id
	movieclip.init()
	movieclip.set_matrix(lm_type_mat.CType(translate))
	movieclip.ctx = ctx
	return movieclip

# global render state control
render_state = lm_render_state.CObj()

# global texture bin
texture_bin = pyglet.image.atlas.TextureBin(4096, 4096)

NUM_MOVIECLIP = 28
(
#######################
# BG Part!
# Some dance bg is such made that its elements can move event to the top,
# which should be hidden by the enso up bg.
#######################
# Dance BG
DANCE_BG, 
# Enso up bg. Scrolling from left to right.
ENSO_UP_BG, 
# sabi effect. When game enters gogotime. This is drawn on top of up bg.
BG_SAB_EFFECTI,

# ===========> renda effects <==============
# Dancers: (Appear in the  following order)
# 4    2    1    3    5
DANCER5,
DANCER4,
DANCER3,
DANCER2,
DANCER1,
# Fever(Appear when tamashii gauge is full.)
FEVER,

# Course icon. not affected by sabi effect.
COURSE, 
# Character don.
DON,
# The tamashi gauge
GAUGE,

# ====> Chibis <======

########################
# Enso Part!
# Enso parts rules.hit judge effect can be the most top.
# The onp_fly animation is on top of the gauge and something else
########################
LANE, 
HITEFFECTS, 
BUNKI,
MATO_GOGO, 
BUNKI_MOJI, 
MATO, 
FULLCOMBO,

# =========> onps <====================

# The taiko.
TAIKO, 
# Left/Right Don/Kats.
LEFT_DON, LEFT_KATS, RIGHT_DON, RIGHT_KATS, 
# Combo number and Cherry(every 100 combo).
COMBO,

# =========> onp_fly <===============
# =========> hit judges <============
# Hit judge text and effect(which covers part of the taiko).
HITJUDGE, 



#######################
# HUD Part!
#######################
# Scores.
# Score Add: How many score is added in the last hit
# Score Main: The total score.
# Renda Num: The current hit of the renda onp
# Combo Num: The current combo(every 10 combo)
#RENDA_NUM, COMBO_NUM,
SCORE_ADD, SCORE_MAIN,

# =========> score add <==================

# To be layout correctly
#SYOUSETSU,
#FEVER,
#RENDA_EFFECT,
#RENDA_NUM,
#CHIBI1,
#CHIBI2,
#CHIBI3,
#CHIBI4,
#CHIBI5,
#CHIBI6,
#CHIBI_MISS,
#DANDER1,
#DANDER2,
#DANDER3,
#DANDER4,
#DANDER5,
#ONP_DON,
#ONP_KATS,
#ONP_DON_DAI,
#ONP_KATS_DAI,
#ONP_RENDA1,
#ONP_RENDA2,
#ONP_RENDA3,
#ONP_RENDA1_DAI,
#ONP_RENDA2_DAI,
#ONP_RENDA3_DAI,
#ONP_IMO,
#ONP_BALLOON,
#ONP_FLY_DON,
#ONP_FLY_DON_DAI,
#ONP_FLY_KATS,
#ONP_FLY_KATS_DAI,
#ONP_FLY_BALLOON,
#IMO,
) = range(NUM_MOVIECLIP)

# Build up scene
movieclips = [None] * NUM_MOVIECLIP

movieclips[DANCE_BG] = load_movie("DANCE_BG_IDOL.LM")
movieclips[ENSO_UP_BG] = load_movie("ENSO_UP_BG_04.LM")
movieclips[COURSE] = load_movie("COURSE_ONI.LM")
movieclips[LANE] = load_movie("ENSO_LANE.LM")
movieclips[HITEFFECTS] = load_movie("ENSO_HITEFFECTS.LM")
movieclips[TAIKO] = load_movie("ENSO_TAIKO.LM")
movieclips[COMBO] = load_movie("ENSO_COMBO.LM")
movieclips[MATO_GOGO] = load_movie("ENSO_MATO_GOGO.LM")
movieclips[MATO] = load_movie("ENSO_MATO.LM")
movieclips[HITJUDGE] = load_movie("ENSO_HITJUDGE.LM")
movieclips[LEFT_DON] = load_movie("ENSO_LEFT_DON.LM")
movieclips[LEFT_KATS] = load_movie("ENSO_LEFT_KATS.LM")
movieclips[RIGHT_DON] = load_movie("ENSO_RIGHT_DON.LM")
movieclips[RIGHT_KATS] = load_movie("ENSO_RIGHT_KATS.LM")
movieclips[GAUGE] = load_movie("GAUGE_DON_E.LM")
movieclips[BUNKI] = load_movie("ENSO_BUNKI.LM")
movieclips[BUNKI_MOJI] = load_movie("ENSO_BUNKI_MOJI.LM")
movieclips[FULLCOMBO] = load_movie("ENSO_FULLCOMBO.LM")
movieclips[BG_SAB_EFFECTI] = load_movie("BG_SAB_EFFECTI.LM")
movieclips[DON] = load_movie("DON_COS00_DIET.LM", (64, 42))
movieclips[SCORE_MAIN] = load_movie("ENSO_SCORE_MAIN.LM")
movieclips[SCORE_ADD] = load_movie("ENSO_SCORE_ADD.LM")
movieclips[FEVER] = load_movie("FEVER_IDOL.LM")
movieclips[DANCER1] = load_movie("DANCE_IDOL_HARUKA.LM", (240, 270))
movieclips[DANCER2] = load_movie("DANCE_IDOL_HIBIKI.LM", (150, 270))
movieclips[DANCER3] = load_movie("DANCE_IDOL_TAKANE.LM", (330, 270))
movieclips[DANCER4] = load_movie("DANCE_IDOL_MIKI.LM", (60, 270))
movieclips[DANCER5] = load_movie("DANCE_IDOL_MAMI.LM", (420, 270))

for dancer in xrange(DANCER1, DANCER1 - 5, -1):
	mc = movieclips[dancer]
	mc.ctx.register_callback("in_end", on_dancer_in_end, dancer)
	mc.ctx.register_callback("dance_sync", on_dancer_sync, dancer)
	
# Texture env
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

# Turn off texture filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

pyglet.app.run()