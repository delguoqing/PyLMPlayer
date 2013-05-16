# -*- coding: gbk -*-

import sys
import os
import cProfile
import pyglet
import gc
import random
import enso_cfg

from tja import tja_onp_mgr, tja_fumen, tja_reader
from enso_layout import *
from pyglet.gl import *
from ctypes import *

from lm import lm_loader
from lm import lm_glb

from lm.type import lm_type_color
from lm.type import lm_type_mat

from lm.drawable import lm_render_state

# standard resolution for psp
window = pyglet.window.Window(480, 272)
fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.0, 1.0, 1.0))

###################################
# Game Logic
###################################
scr_shot_id = 0
cur_combo = 0	# current combo
cur_renda = 0	# current renda
cur_score = 0	# current score
max_balloon = -1 # hits needed to break to balloon
cur_balloon = 0 # current balloon
max_imo = -1
cur_imo = 0
cur_dancer = -1	# current dancer
cur_renda_effect = 1 # current renda_effect id
first_unsync_dancer = -1 # current unsync_dancer
last_unsync_dancer = -1 # last unsync_dancer
donchan_free = True


# Dancer Pos
DANCER1_POS = (240, 270)
DANCER2_POS = (150, 270)
DANCER3_POS = (330, 270)
DANCER4_POS = (60, 270)
DANCER5_POS = (420, 270)

RENDA_EFFECT_POS_BASE = (-30, 200)

def set_combo(combo):

	global movieclips, cur_combo
	
	num1000 = combo // 1000
	num100 = (combo - num1000 * 1000) // 100
	num10 = (combo - num1000 * 1000 - num100 * 100) // 10
	num1 = combo - num1000 * 1000 - num100 * 100 - num10 * 10	

	_num1000 = cur_combo // 1000
	_num100 = (cur_combo - _num1000 * 1000) // 100
	_num10 = (cur_combo - _num1000 * 1000 - _num100 * 100) // 10
			
	if combo < 10:
		movieclips[COMBO].enso_combo.gotoAndPlay("combo0-9")
	elif combo < 100:
		movieclips[COMBO].enso_combo.gotoAndPlay("combo10-99")		
		movieclips[COMBO].enso_combo.num1.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].enso_combo.num10.gotoAndPlay("number_%d" % num10)
		
	elif combo < 1000:
		movieclips[COMBO].enso_combo.gotoAndPlay("combo100-999color")
		movieclips[COMBO].enso_combo.num1color.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].enso_combo.num10color.gotoAndPlay("number_%d" % num10)
		movieclips[COMBO].enso_combo.num100color.gotoAndPlay("number_%d" % num100)		
			
	elif combo < 10000:
		
		movieclips[COMBO].enso_combo.gotoAndPlay("combo1000-9999color")
		movieclips[COMBO].enso_combo.num1color.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].enso_combo.num10color.gotoAndPlay("number_%d" % num10)
		movieclips[COMBO].enso_combo.num100color.gotoAndPlay("number_%d" % num100)
		movieclips[COMBO].enso_combo.num1000color.gotoAndPlay("number_%d" % num1000)

	if _num100 != num100 and num100 != 0:
		movieclips[COMBO].enso_combo.cherry.gotoAndPlay("in")
		set_fukidashi_combo(num1000, num100, num10)
	elif (_num10 != num10 and num10 != 0) or (_num1000 != num1000 and num1000 != 0):
		set_fukidashi_combo(num1000, num100, num10)	
		
	cur_combo = combo
	
def set_fukidashi_combo(num1000, num100, num10):
	global movieclips
	
	num1 = 0
	
	mc = movieclips[FUKIDASHI]
	mc.gotoAndPlay("combo")
	
	first = False

	if num1000 != 0:	
		mc.combo_num_1000.gotoAndStop("number_%d" % num1000)
		first = True
	else:
		mc.combo_num_1000.gotoAndStop("start_number")

	if num100 != 0 or first:	
		mc.combo_num_100.gotoAndStop("number_%d" % num100)
		first = True
	else:
		mc.combo_num_100.gotoAndStop("start_number")
		
	if num10 != 0 or first:	
		mc.combo_num_10.gotoAndStop("number_%d" % num10)
		first = True
	else:
		mc.combo_num_10.gotoAndStop("start_number")
		
	mc.combo_num_1.gotoAndStop("number_%d" % num1)
		
def add_score(score):
	global SCORE_ADD_INDEX
	
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
	
	mc = movieclips[SCORE_ADD].alloc(INDEX_SCORE_ADD)
	if mc is not None: mc.gotoAndPlay("score")
	
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

def dancer_log(i, str):
	print "[DANCER%d] %s" % (5 - i + DANCER5, str)

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
	# DANCER1 will never be removed
	if cur_dancer != -1 and cur_dancer < DANCER1:
		# remove `cur_dancer`
		movieclips[cur_dancer].gotoAndPlay("out")
		cur_dancer += 1
		
def on_dancer_in_end(mc, dancer):
	global movieclips, first_unsync_dancer, last_unsync_dancer
	if dancer == DANCER1:	# if it is the first dancer, then start dance at once
		movieclips[dancer].gotoAndPlay("dance")
	elif dancer >= cur_dancer:
		if first_unsync_dancer == -1:
			first_unsync_dancer = dancer
		last_unsync_dancer = dancer

def on_dancer_sync(mc, dancer):
	global first_unsync_dancer, last_unsync_dancer, movieclips
	if first_unsync_dancer != -1:
		sync_to = movieclips[dancer].dancer._play_head
		a, b = first_unsync_dancer, last_unsync_dancer
		first_unsync_dancer = -1
		for dancer in xrange(b, a + 1):
			movieclips[dancer].gotoAndPlay("dance")
			movieclips[dancer].dancer.gotoAndPlay(sync_to)
			
def set_renda(renda):
	global movieclips, cur_renda
	mc = movieclips[RENDA_NUM]
	
	if renda == cur_renda: return
	if renda == 0: mc.gotoAndPlay("renda_out"); return
	if cur_renda == 0: mc.gotoAndPlay("renda_hit")
	
	num100 = renda // 100
	num10 = (renda - num100 * 100) // 10
	num1 = renda - num100 * 100 - num10 * 10
	
	if num100 != 0:
		mc.renda_hukidashi.gotoAndPlay("renda_hit_100")
		mc.renda_hukidashi.geki_num_00.gotoAndStop("number_%d" % num1)
		mc.renda_hukidashi.geki_num_10.gotoAndStop("number_%d" % num10)
		mc.renda_hukidashi.geki_num_100.gotoAndStop("number_%d" % num100)
	elif num10 != 0:
		mc.renda_hukidashi.gotoAndPlay("renda_hit_10")
		mc.renda_hukidashi.geki_num_00.gotoAndStop("number_%d" % num1)
		mc.renda_hukidashi.geki_num_10.gotoAndStop("number_%d" % num10)
	else:
		mc.renda_hukidashi.gotoAndPlay("renda_hit_00")
		mc.renda_hukidashi.geki_num_00.gotoAndStop("number_%d" % num1)
	cur_renda = renda
	
def swap_depth(depth1, depth2):
	global movieclips
	movieclips[depth1], movieclips[depth2] = movieclips[depth2], movieclips[depth1]
		
def set_max_balloon(balloon):
	global max_balloon, cur_balloon, donchan_free

	# if donchan is busy	
	if not donchan_free: return
	# max balloon hit can't be zero
	if balloon == 0: return

	donchan_free = False
	# This goes first
	mc = movieclips[BALLOON]
	mc._visible = True	
	mc.gotoAndPlay("geki_hit")
	
	swap_depth(DON, DON2)
	movieclips[DON2].matrix.translate = enso_cfg.DON_POS_BALLOON
		
	max_balloon = balloon
	set_balloon(balloon)
	
def set_balloon(balloon):
	global cur_balloon, movieclips, max_balloon
	
	if balloon < 0: return
	if balloon == cur_balloon: return
	
	mc = movieclips[BALLOON]
	
	if balloon == 0:
		movieclips[DON2].gotoAndPlay("balloon_succsess")
		mc.gotoAndPlay("geki_break")
		return
		
	# in case of overflow	
	if balloon >= 1000: balloon = 999

	num100 = balloon // 100
	num10 = (balloon - num100 * 100) // 10
	num1 = balloon - num100 * 100 - num10 * 10
	
	mc_geki_num = mc.geki_num
	if balloon < 10:
		mc_geki_num.gotoAndPlay("num_0")
		mc_geki_num.geki_num_00.gotoAndPlay("number_%d" % num1)
	elif balloon < 100:
		mc.geki_num.gotoAndPlay("num_00")
		mc_geki_num.geki_num_00.gotoAndPlay("number_%d" % num1)
		mc_geki_num.geki_num_10.gotoAndPlay("number_%d" % num10)
	elif balloon < 1000:
		mc.geki_num.gotoAndPlay("num_000")	
		mc_geki_num.geki_num_00.gotoAndPlay("number_%d" % num1)
		mc_geki_num.geki_num_10.gotoAndPlay("number_%d" % num10)		
		mc_geki_num.geki_num_100.gotoAndPlay("number_%d" % num100)		
	
	# 6 level in total
	progress = (max_balloon - balloon) * 6 / max_balloon + 1
	mc.geki_don.gotoAndPlay("geki_0%d" % progress)
	
	if progress == 6:
		movieclips[DON2].gotoAndPlay("balloon_6")
	else:
		movieclips[DON2].gotoAndPlay("balloon_1")
	movieclips[DON2].don.gotoAndPlay(0)
		
	cur_balloon = balloon

def on_balloon_success_end(mc, data):
	global max_balloon, cur_balloon, donchan_free
	swap_depth(DON, DON2)
	# should gotoAndPlay old animation
	max_balloon = -1
	cur_balloon = 0
	donchan_free = True
	movieclips[DON].gotoAndPlay("normal")
	movieclips[DON].matrix.translate = enso_cfg.DON_POS_NORMAL
		
def set_max_imo(imo):
	global max_imo, cur_imo, donchan_free
	
	if not donchan_free: return
	if imo <= 0: return
	
	donchan_free = False
	
	mc = movieclips[IMO]
	mc.gotoAndPlay("imo_start")
	
	swap_depth(DON, DON2)
	movieclips[DON2].matrix.translate = enso_cfg.DON_POS_IMO
	movieclips[DON2].gotoAndPlay("imo_in")
	
	max_imo = imo
	set_imo(imo)
	
def set_imo(imo):
	global cur_imo, movieclips, max_imo
	
	if imo < 0: return
	if imo == cur_imo: return
	
	mc = movieclips[IMO]
	
	if imo == 0:
		movieclips[DON2].gotoAndPlay("imo_break_high")
		mc.gotoAndPlay("imo_break_high")
		return
		
	# in case of overflow	
	if imo >= 1000: imo = 999

	num100 = imo // 100
	num10 = (imo - num100 * 100) // 10
	num1 = imo - num100 * 100 - num10 * 10
	
	if imo == max_imo: # not event begin to eat
		cur_imo = imo
		return
	elif cur_imo == max_imo: # the first bite
		mc.gotoAndPlay("imo_hit")
		movieclips[DON2].gotoAndPlay("imo_eat")
	
	cur_imo = imo
	
	mc_geki_num = mc.imo_num_100
	if imo < 10:
		mc_geki_num.gotoAndPlay("1digit")
		mc_geki_num.num_Layer2_num_1.gotoAndPlay("number_%d" % num1)
	elif imo < 100:
		mc_geki_num.gotoAndPlay("2digit")
		mc_geki_num.num_Layer2_num_1.gotoAndPlay("number_%d" % num1)
		mc_geki_num.num_Layer2_num_2.gotoAndPlay("number_%d" % num10)
	elif imo < 1000:
		mc_geki_num.gotoAndPlay("3digit")	
		mc_geki_num.num_Layer2_num_1.gotoAndPlay("number_%d" % num1)
		mc_geki_num.num_Layer2_num_2.gotoAndPlay("number_%d" % num10)		
		mc_geki_num.num_Layer2_num_3.gotoAndPlay("number_%d" % num100)		
	
	# 6 level in total
	progress = (max_imo - imo) * 6 / max_imo + 1
	mc.imo_don.gotoAndPlay("geki_0%d" % progress)
	
	movieclips[DON2].don.gotoAndPlay(0)
	
def on_imo_break_end(mc, data):
	global max_imo, cur_imo, donchan_free
	swap_depth(DON, DON2)
	# should gotoAndPlay old animation
	max_imo = -1
	cur_imo = 0
	donchan_free = True
	movieclips[DON].gotoAndPlay("normal")
	movieclips[DON].matrix.translate = enso_cfg.DON_POS_NORMAL
	
def on_imo_in_end(mc, data):
	global movieclips
	
	movieclips[DON2].gotoAndPlay("imo_eat")
		
@window.event
def on_key_press(symbol, modifiers):
	global movieclips, render_state
	if symbol == pyglet.window.key.F:
		movieclips[LEFT_DON].gotoAndPlay("left_don")
		movieclips[MATO].gotoAndPlay("hit_ryo")
		movieclips[HITJUDGE].gotoAndPlay("hit_ryo")
		movieclips[HITEFFECTS].gotoAndPlay("don_s")
		
		chibi = movieclips[CHIBI].alloc(INDEX_CHIBI_HIT)
		if chibi is not None: chibi.gotoAndPlay(0)

		onp_fly_don = movieclips[ONP_FLY].alloc(INDEX_ONP_FLY_DON)
		onp_fly_don.gotoAndPlay("don_hit")
		
		global cur_renda_effect
		renda_effect = movieclips[RENDA_EFFECT].alloc(INDEX_RENDA_EFFECT)
		if renda_effect: 
			x_range = enso_cfg.RENDA_EFFECT_X_RANGE
			y_range = enso_cfg.RENDA_EFFECT_Y_RANGE
			x = random.randint(x_range[0], x_range[1])
			y = random.randint(y_range[0], y_range[1])
			renda_effect.matrix.translate = (x, y)
			enso_cfg.RENDA_EFFECT_FUNC(renda_effect, random.randint(1, enso_cfg.RENDA_EFFECT_NUM))
			
	elif symbol == pyglet.window.key.J:
		movieclips[RIGHT_DON].gotoAndPlay("right_don")
		movieclips[MATO].gotoAndPlay("hit_ka")		
		movieclips[HITJUDGE].gotoAndPlay("hit_ka")
		movieclips[HITEFFECTS].gotoAndPlay("don_b")
		movieclips[COURSE].gotoAndPlay("hit")
		
		chibi = movieclips[CHIBI].alloc(INDEX_CHIBI_MISS)
		if chibi is not None: chibi.gotoAndPlay(0)

		onp_fly_kats = movieclips[ONP_FLY].alloc(INDEX_ONP_FLY_KATS)
		onp_fly_kats.gotoAndPlay("katsu_hit")
						
	elif symbol == pyglet.window.key.R:
		movieclips[LEFT_KATS].gotoAndPlay("left_kats")
		movieclips[MATO].gotoAndPlay("hit_dai_ryo")		
		movieclips[HITEFFECTS].gotoAndPlay("katsu_s")
		movieclips[HITJUDGE].gotoAndPlay("hit_ryo_big")
		
		onp_fly_geki = movieclips[ONP_FLY].alloc(INDEX_ONP_FLY_GEKI)
		onp_fly_geki.gotoAndPlay("geki_hit")		
		
	elif symbol == pyglet.window.key.U:
		movieclips[RIGHT_KATS].gotoAndPlay("right_kats")
		movieclips[MATO].gotoAndPlay("hit_dai_ka")
		movieclips[HITJUDGE].gotoAndPlay("hit_ka_big")
		movieclips[HITEFFECTS].gotoAndPlay("katsu_b")		
		
		onp_fly_don_dai = movieclips[ONP_FLY].alloc(INDEX_ONP_FLY_DON_DAI)
		onp_fly_don_dai.gotoAndPlay("don_d_hit")
		
	elif symbol == pyglet.window.key.BRACKETLEFT:
		movieclips[MATO_GOGO].gotoAndPlay("sabi_in")
		movieclips[DANCE_BG].gotoAndPlay("normal_fever")
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_start")
		movieclips[FEVER].fever.gotoAndPlay("fever_start")
		movieclips[GAUGE].gotoAndStop("gage_50")
		
		movieclips[DON].gotoAndPlay("full_sabi")
	elif symbol == pyglet.window.key.BRACKETRIGHT:
		movieclips[MATO_GOGO].gotoAndPlay("sabi_out")
		movieclips[GAUGE].gotoAndStop("gage_47")
		movieclips[DANCE_BG].gotoAndPlay("fever_normal")
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_end")
		movieclips[FEVER].fever.gotoAndPlay("fever_end")		

		movieclips[DON].gotoAndPlay("normal")		
	elif symbol == pyglet.window.key.SPACE:
		movieclips[FULLCOMBO].gotoAndPlay("run")

	elif symbol == pyglet.window.key.UP:
		movieclips[BUNKI].play()
		movieclips[BUNKI_MOJI].play()
		add_dancer()		
		movieclips[FUKIDASHI].gotoAndPlay("level_up")		
		
	elif symbol == pyglet.window.key.DOWN:
		remove_dancer()
		movieclips[FUKIDASHI].gotoAndPlay("level_down")
		
	elif symbol == pyglet.window.key.NUM_ADD:
		set_combo(cur_combo + 1)
		add_score(1500)
		set_renda(cur_renda + 1)
		
	elif symbol == pyglet.window.key._1:
		render_state.enable_statistic(1)
		
	elif symbol == pyglet.window.key._0:
		movieclips[GAUGE].gotoAndStop("gage_50")
		
	elif symbol == pyglet.window.key.ESCAPE:
		pyglet.clock.unschedule(on_draw)
		
	elif symbol == pyglet.window.key.ENTER:
		global cur_balloon, max_balloon
		if max_balloon <= 0:
			set_max_balloon(random.randint(1, 20))
		else:
			set_balloon(cur_balloon - 1)
			
	elif symbol == pyglet.window.key.I: # Imo
		global cur_imo, max_imo
		if max_imo <= 0:
			set_max_imo(random.randint(10, 20))
		else:
			set_imo(cur_imo - 1)
			
	elif symbol == pyglet.window.key.F10:
		global scr_shot_id
		pyglet.image.get_buffer_manager().get_color_buffer().save('enso%d.jpg' % scr_shot_id)
		scr_shot_id += 1
		
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
	
	#glClearColor(1, 1, 1, 1)
	#window.clear()
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	render_state.begin()
	
	for movieclip in movieclips:
		if movieclip is None: continue
		#if movieclip not in (movieclips[MATO_GOGO], ): continue
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

# global render state control
render_state = lm_render_state.CObj()

# Build up scene
def build_scene(cfg):
	global INDEX_CHIBI_HIT, INDEX_CHIBI_MISS
	global INDEX_RENDA_EFFECT
	global INDEX_SCORE_ADD
	global INDEX_ONP_FLY_DON, INDEX_ONP_FLY_DON_DAI
	global INDEX_ONP_FLY_KATS, INDEX_ONP_FLY_KATS_DAI
	global INDEX_ONP_FLY_GEKI
	
	loader = lm_loader.CLoader("pspdx", cfg.LM_PACK_ROOT)
	LMC = loader.load_movie
	LMCS = loader.load_multi_movie
	LMP = loader.load_movie_pool
	
	movieclips = [None] * NUM_MOVIECLIP
	movieclips[DANCE_BG] = LMC(cfg.DANCE_BG)
	movieclips[ENSO_UP_BG] = LMC(cfg.ENSO_UP_BG)
	movieclips[COURSE] = LMC(cfg.COURSE)
	movieclips[LANE] = LMC(cfg.LANE)
	movieclips[HITEFFECTS] = LMC(cfg.HITEFFECTS)
	movieclips[TAIKO] = LMC(cfg.TAIKO)
	movieclips[COMBO] = LMC(cfg.COMBO)
	movieclips[MATO_GOGO] = LMC(cfg.MATO_GOGO)
	movieclips[MATO] = LMC(cfg.MATO)
	movieclips[HITJUDGE] = LMC(cfg.HITJUDGE)
	movieclips[LEFT_DON] = LMC(cfg.LEFT_DON)
	movieclips[LEFT_KATS] = LMC(cfg.LEFT_KATS)
	movieclips[RIGHT_DON] = LMC(cfg.RIGHT_DON)
	movieclips[RIGHT_KATS] = LMC(cfg.RIGHT_KATS)
	movieclips[GAUGE] = LMC(cfg.GAUGE)
	movieclips[BUNKI] = LMC(cfg.BUNKI)
	movieclips[BUNKI_MOJI] = LMC(cfg.BUNKI_MOJI)
	movieclips[FULLCOMBO] = LMC(cfg.FULLCOMBO)
	movieclips[BG_SAB_EFFECTI] = LMC(cfg.BG_SAB_EFFECTI)
	movieclips[DON] = LMC(cfg.DON, cfg.DON_POS_NORMAL)
	movieclips[SCORE_MAIN] = LMC(cfg.SCORE_MAIN)
	movieclips[FEVER] = LMC(cfg.FEVER)
	movieclips[FEVER].speed = 2
	movieclips[DANCER1] = LMC(cfg.DANCER1, DANCER1_POS)
	movieclips[DANCER1].speed = 1.46
	movieclips[DANCER2] = LMC(cfg.DANCER2, DANCER2_POS)
	movieclips[DANCER2].speed = 1.46
	movieclips[DANCER3] = LMC(cfg.DANCER3, DANCER3_POS)
	movieclips[DANCER3].speed = 1.46
	movieclips[DANCER4] = LMC(cfg.DANCER4, DANCER4_POS)
	movieclips[DANCER4].speed = 1.46
	movieclips[DANCER5] = LMC(cfg.DANCER5, DANCER5_POS)
	movieclips[DANCER5].speed = 1.46
	movieclips[RENDA_NUM] = LMC(cfg.RENDA_NUM)
	movieclips[FUKIDASHI] = LMC(cfg.FUKIDASHI)
	movieclips[BALLOON] = LMC(cfg.BALLOON)
	movieclips[IMO] = LMC(cfg.IMO)
	
	# Load score add
	_def = (((cfg.SCORE_ADD, 30),),)
	movieclips[SCORE_ADD] = LMP(_def)
	INDEX_SCORE_ADD, = range(len(_def))
	
	# Load chibi
	_def = ([], ((cfg.CHIBI_MISS, 40),),)
	for chibi_lm in cfg.CHIBI:
		_def[0].append((chibi_lm, 40 / len(cfg.CHIBI)))
	movieclips[CHIBI] = LMP(_def)
	INDEX_CHIBI_HIT, INDEX_CHIBI_MISS = range(len(_def))
	movieclips[CHIBI].speed = 1.46
	
	# Load renda effect
	_def = (((cfg.RENDA_EFFECT, 30),),)
	movieclips[RENDA_EFFECT] = LMP(_def)
	INDEX_RENDA_EFFECT, = range(len(_def))
	
	# Load onp fly
	_def = (((cfg.ONP_FLY[0], 30),), ((cfg.ONP_FLY[1], 30),), ((cfg.ONP_FLY[2], 30),), ((cfg.ONP_FLY[3], 30),), ((cfg.ONP_FLY[4], 10),),)
	movieclips[ONP_FLY] = LMP(_def)
	INDEX_ONP_FLY_DON, INDEX_ONP_FLY_DON_DAI, INDEX_ONP_FLY_KATS, INDEX_ONP_FLY_KATS_DAI, INDEX_ONP_FLY_GEKI = range(len(_def))
	
	# Register callbacks
	for dancer in xrange(DANCER1, DANCER1 - 5, -1):
		mc = movieclips[dancer]
		mc.register_callback("in_end", on_dancer_in_end, dancer)
		mc.register_callback("dance_sync", on_dancer_sync, dancer)
	
	movieclips[DON].register_callback("baloon_success_end", on_balloon_success_end, None)
	movieclips[DON].register_callback("imo_break_end", on_imo_break_end, None)
	movieclips[DON].register_callback("imo_in_end", on_imo_in_end, None)
		
	movieclips[BALLOON].ctx.set_global("don", movieclips[DON])
	movieclips[BALLOON]._visible = False
	
	DON_KARADA_MAPPING = (
		(0, "karada_01b"),
		(3, "karada_01a"),
		(6, "karada_02b"),
		(9, "karada_02a"),
		(13, "karada_03b"),
		(16, "karada_03a"),
		(26, "karada_04b"),
		(29, "karada_04a"),
		(35, "karada_09b"),
		(38, "karada_09a"),

		(44, "karada_06b"),
		(47, "karada_06a"),
		(50, "karada_07b"),
		(53, "karada_07a"),
		
		(55, "karada_05b"),
		(58, "karada_05a"),
		(60, "karada_08b"),
		(63, "karada_08a"),
	)
	DON_ATAMA_MAPPING = (
		(1, "atama_01b"),
		(4, "atama_01a"),
		(7, "atama_02b"),
		(10, "atama_02a"),
		(14, "atama_03b"),
		(17, "atama_03a"),
		(27, "atama_04b"),
		(30, "atama_04a"),
		(36, "atama_09b"),
		(39, "atama_09a"),

		(43, "atama_06b"),
		(46, "atama_06a"),
		(49, "atama_07b"),
		(52, "atama_07a"),
		
		(56, "atama_05b"),
		(59, "atama_05a"),
		(61, "atama_08b"),
		(64, "atama_08a"),
		
		(20, "gum"),
	)
	
	# Don change costume
	if cfg.DON_COS:
		_ctx = movieclips[DON].ctx
		for idx, part in DON_KARADA_MAPPING:
			_ctx.replace_texture(idx, os.path.join(cfg.DON_KARADA[0], "cos_%02d_%s.png" % (cfg.DON_KARADA[1], part)))
		for idx, part in DON_ATAMA_MAPPING:
			_ctx.replace_texture(idx, os.path.join(cfg.DON_ATAMA[0], "cos_%02d_%s.png" % (cfg.DON_ATAMA[1], part)))
	
	# ONPS
	reader = tja_reader.CReader()
	reader.set_file(sys.argv[1])
	fumen = tja_fumen.CFumen()
	fumen.read_header(reader)
	fumen.read_fumen(reader)
	
	onp_lumens = []
	for filename in cfg.ONPS[:-1]:
		onp_lumens.append(LMC(filename))
	onp_lumens.extend(LMCS(cfg.ONPS[-1], 2))
	
	movieclips[ONPS] = tja_onp_mgr.CMgr(fumen, options=0)
	movieclips[ONPS].set_onp_lumens(onp_lumens)
	
	return movieclips

movieclips = build_scene(enso_cfg)

# Texture env
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

# Turn off texture filter
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

pyglet.app.run()