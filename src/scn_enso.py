import os
import random
import pyglet
from pyglet.gl import *

from lm import lm_consts
from lm import lm_loader
from lm.extensions import lm_render_state
from tja import tja_onp_mgr
from layout import *
from tja.tja_consts import *
import game_state

import config

EPS = 0.000001

# take care of widescreen
splash_start_label = "splashStartWide"
splash_end_label = ""
fever_start_label = "feverWide_start"
fever_end_label = "feverWide_end"

# enso lane area config
ONP_HIT_X = 145
ONP_Y = 153
ONP_IN_X = 640
ONP_OUT_X = 0
ONP_DIST = 30
DIST_CFG = (ONP_DIST, ONP_IN_X, ONP_HIT_X, ONP_OUT_X, ONP_Y)

# enso display data
cur_combo = 0
cur_renda = 0
cur_score = 0
max_balloon = -1
cur_balloon = 0
max_imo = -1
cur_imo = 0
cur_miss = 0
cur_level = None
cur_dancer = -1
cur_tamashii = 0
max_tamashii = 1
cur_tamashii_grid = 0
max_tamashii_grid = 50
cur_ggt = False
donchan_free = True
def init_enso_data():
	cur_combo = 0
	cur_renda = 0
	cur_score = 0
	max_balloon = -1
	cur_balloon = 0
	max_imo = -1
	cur_imo = 0
	cur_miss = 0
	cur_level = None
	cur_dancer = -1
	cur_tamashii = 0
	max_tamashii = 1
	cur_tamashii_grid = 0
	max_tamashii_grid = 50
	cur_ggt = False	

# movieclips
movieclips = None

def on_config_update():
	#######################
	# Widescreen config
	#######################
	widescreen = config.DATA["widescreen"]
	# SplashStart(Wide)
	global splash_start_label
	splash_start_label = "splashStart"
	if widescreen:
		splash_start_label += "Wide"
		
	# fever(Wide)_start, fever(Wide)_end
	global fever_start_label, fever_end_label
	fever_start_label = "fever%s_start" % (widescreen and "Wide" or "")
	fever_end_label = "fever%s_end" % (widescreen and "Wide" or "")
	
	#######################
	# Onp config
	#######################
	global ONP_HIT_X, ONP_Y, ONP_IN_X, ONP_OUT_X, ONP_DIST, DIST_CFG
	ONP_HIT_X = config.DATA["onp_hit_x"]
	ONP_Y = config.DATA["onp_y"]
	ONP_IN_X = config.DATA["onp_in_x"]
	ONP_OUT_X = config.DATA["onp_out_x"]
	ONP_DIST = config.DATA["onp_dist"]
	DIST_CFG = (ONP_DIST, ONP_IN_X, ONP_HIT_X, ONP_OUT_X, ONP_Y)
	
def set_combo(combo):

	global movieclips, cur_combo, cur_miss, cur_ggt, cur_tamashii, max_tamashii
	
	num1000 = combo // 1000
	num100 = (combo - num1000 * 1000) // 100
	num10 = (combo - num1000 * 1000 - num100 * 100) // 10
	num1 = combo - num1000 * 1000 - num100 * 100 - num10 * 10	

	_num1000 = cur_combo // 1000
	_num100 = (cur_combo - _num1000 * 1000) // 100
	_num10 = (cur_combo - _num1000 * 1000 - _num100 * 100) // 10
			
	if combo < 10:
		movieclips[COMBO].gotoAndPlay("combo0-9")
	elif combo < 100:
		movieclips[COMBO].gotoAndPlay("combo10-99")		
		movieclips[COMBO].num1.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].num10.gotoAndPlay("number_%d" % num10)
		
	elif combo < 1000:
		movieclips[COMBO].gotoAndPlay("combo100-999color")
		movieclips[COMBO].num1color.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].num10color.gotoAndPlay("number_%d" % num10)
		movieclips[COMBO].num100color.gotoAndPlay("number_%d" % num100)		
			
	elif combo < 10000:
		
		movieclips[COMBO].gotoAndPlay("combo1000-9999color")
		movieclips[COMBO].num1color.gotoAndPlay("number_%d" % num1)
		movieclips[COMBO].num10color.gotoAndPlay("number_%d" % num10)
		movieclips[COMBO].num100color.gotoAndPlay("number_%d" % num100)
		movieclips[COMBO].num1000color.gotoAndPlay("number_%d" % num1000)

	if _num100 != num100 and num100 != 0:
		movieclips[COMBO].cherry.gotoAndPlay("in")
		set_fukidashi_combo(num1000, num100, num10)
	elif (_num10 != num10 and num10 != 0) or (_num1000 != num1000 and num1000 != 0):
		set_fukidashi_combo(num1000, num100, num10)

	miss = (combo == 0)
	first_miss = (cur_miss == 0 and miss)
		
	# onp animation speed
	cur_onp_level = min(cur_combo // 50, 3)
	onp_level = min(combo // 50, 3)
	if cur_onp_level != onp_level:
		for onp in xrange(ONP_SHORT[0], ONP_SHORT[1] + 1):
			movieclips[ONPS]._onp_lumens[onp].gotoAndPlay("level0%d" % (onp_level + 1))
		for onp in xrange(ONP_LONG[0], ONP_LONG[1] + 1):
			movieclips[ONPS]._onp_lumens[onp].gotoAndPlay("level0%d" % (onp_level + 1))
			
	# Miss chibi
	if miss:
		mc = movieclips[CHIBI].alloc(INDEX_CHIBI_MISS)
		if mc: mc.gotoAndPlay(0)
	
	# Miss fukidashi
	if first_miss:
		movieclips[FUKIDASHI].gotoAndPlay("miss")
	
	## Miss don animation
	if not cur_ggt:
		if first_miss:
			if cur_tamashii == max_tamashii:
				movieclips[DON].gotoAndPlay("norm_idle")
			else:
				movieclips[DON].gotoAndPlay("miss")
		elif cur_miss == 5 and miss:
			movieclips[DON].gotoAndPlay("miss_6")
		elif cur_miss > 0 and not miss:
			movieclips[DON].gotoAndPlay("miss_normal")
	if first_miss:
		now_gauge_num = int(50.0 * cur_tamashii / max_tamashii + EPS)
		if now_gauge_num < 40:
			movieclips[ENSO_UP_BG].gotoAndPlay("normal_miss")
		else:
			movieclips[ENSO_UP_BG].gotoAndPlay("fever_miss")
	
	# Update data
	cur_combo = combo
	if cur_combo == 0:
		cur_miss += 1
	else:
		cur_miss = 0
	
def play_fullcombo():
	global movieclips
	movieclips[FULLCOMBO].gotoAndPlay("run")

def set_fukidashi_combo(num1000, num100, num10):
	global movieclips, cur_ggt, cur_tamashii, max_tamashii
	
	num1 = 0
	
	mc = movieclips[FUKIDASHI]
	mc.gotoAndPlay("combo")
	
	if not cur_ggt:
		if cur_tamashii != max_tamashii:
			movieclips[DON].gotoAndPlay("combo")
		else:
			movieclips[DON].gotoAndPlay("full_combo")
			
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
	if mc is None: return
	
	mc.gotoAndPlay("score")
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
	movieclips[cur_dancer].active = True
	movieclips[cur_dancer].gotoAndPlay("in")
	
def remove_dancer():
	global cur_dancer
	# DANCER1 will never be removed
	if cur_dancer != -1 and cur_dancer < DANCER1:
		# remove `cur_dancer`
		movieclips[cur_dancer].gotoAndPlay("out")
		cur_dancer += 1
		
def on_dancer_in_end(mc, dancer):
	global movieclips
	
	if dancer != DANCER1:
		mc.dance.gotoAndPlay(movieclips[DANCER1].dance._play_head)
		
def set_balloon_miss():
	global movieclips, max_balloon, cur_balloon
	
	movieclips[DON_GEKI].gotoAndPlay("geki_miss")
	progress = (max_balloon - cur_balloon) * 6 / max_balloon + 1
	if progress != 3:
		movieclips[DON_GEKI].geki_miss.gotoAndPlay("geki0%d_miss" % progress)
	else:
		movieclips[DON_GEKI].geki_miss.gotoAndPlay("geki_03_miss")
		
def set_max_balloon(balloon):
	global max_balloon, cur_balloon, donchan_free

	# if donchan is busy	
	if not donchan_free: return
	# max balloon hit can't be zero
	if balloon == 0: return

	donchan_free = False
	
	movieclips[DON].active = False
	movieclips[DON_GEKI].active = True
	movieclips[DON_GEKI].gotoAndPlay("init")
		
	max_balloon = balloon
	set_balloon(balloon)
	
def set_balloon(balloon):
	global cur_balloon, movieclips, max_balloon
	
	if balloon < 0: return
	if balloon == cur_balloon: return
	
	mc = movieclips[DON_GEKI]

	if balloon == 0:
		mc.gotoAndPlay("geki_break")
		return
	
	mc.gotoAndPlay("geki_hit")
	
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
		
	cur_balloon = balloon

def on_balloon_end(mc, data):
	global max_balloon, cur_balloon, donchan_free
	# should gotoAndPlay old animation
	max_balloon = -1
	cur_balloon = 0
	donchan_free = True
	movieclips[DON].active = True
	reset_don()

def set_max_imo(imo):
	global max_imo, cur_imo, donchan_free
	
	if not donchan_free: return
	if imo <= 0: return
	
	donchan_free = False
	
	mc = movieclips[IMO]
	mc.gotoAndPlay("start")
	
	movieclips[DON].active = False
	movieclips[DON_IMO].active = True
	movieclips[DON_IMO].gotoAndPlay(0)
	
	max_imo = imo
	cur_imo = max_imo
	#set_imo(0, True)
	
def set_imo(imo, high):
	global cur_imo, movieclips, max_imo, cur_ggt
	
	if imo < 0: return
	
	mc = movieclips[IMO]
	
	if imo == 0:
		if high:
			movieclips[DON_IMO].gotoAndPlay("geki_break_high")
			movieclips[DON_IMO].geki_break_high.gotoAndPlay(0)
			mc.gotoAndPlay("geki_break_high")
		else:
			movieclips[DON_IMO].gotoAndPlay("geki_break_low")
			movieclips[DON_IMO].geki_break_low.gotoAndPlay(0)
			mc.gotoAndPlay("geki_break_low")
		if cur_ggt:
			mc.kusudama.score.gotoAndPlay("gogotime")
		else:
			mc.kusudama.score.gotoAndPlay("normal")
		return
		
	# in case of overflow	
	if imo >= 1000: imo = 999
	
	movieclips[DON_IMO].gotoAndPlay("geki_hit")
	mc.gotoAndPlay("geki_hit")
	mc_geki_num = mc.kusudama_counter
	num100 = imo // 100
	num10 = (imo - num100 * 100) // 10
	num1 = imo - num100 * 100 - num10 * 10	
	if imo < 10:
		mc_geki_num.gotoAndPlay("figure1")
		mc_geki_num.digit1.gotoAndPlay("number_%d" % num1)
	elif imo < 100:
		mc_geki_num.gotoAndPlay("figure2")
		mc_geki_num.digit1.gotoAndPlay("number_%d" % num1)
		mc_geki_num.digit2.gotoAndPlay("number_%d" % num10)
	elif imo < 1000:
		mc_geki_num.gotoAndPlay("figure3")	
		mc_geki_num.digit1.gotoAndPlay("number_%d" % num1)
		mc_geki_num.digit2.gotoAndPlay("number_%d" % num10)		
		mc_geki_num.digit3.gotoAndPlay("number_%d" % num100)
	cur_imo = imo
	
	if imo == max_imo: # not event begin to eat
		return
	
	movieclips[DON_IMO].geki_don.play()
	
	# 6 level in total
	progress = (max_imo - imo) * 6 / max_imo + 1
	mc.kusudama.gotoAndPlay("geki_0%d" % progress)
	
def set_imo_miss():
	global movieclips, max_imo, cur_imo
	
	movieclips[DON_IMO].gotoAndPlay("geki_miss")
	movieclips[IMO].gotoAndPlay("geki_miss")
	progress = (max_imo - cur_imo) * 6 / max_imo + 1
	movieclips[IMO].kusudama.gotoAndPlay("geki0%d_miss" % progress)

def on_imo_break_end(mc, data):
	global max_imo, cur_imo, donchan_free
	
	# should gotoAndPlay old animation
	max_imo = -1
	cur_imo = 0
	donchan_free = True
	movieclips[DON].active = True
	reset_don()

def on_imo_in_end(mc, data):
	global cur_imo
	set_imo(cur_imo, True)

def on_trans_animation_end(mc, data):
	reset_don()

def play_onp_fly(onp_fly):
	mc = movieclips[ONP_FLY].alloc(INDEX_ONP_FLY)
	if not mc: return
	if onp_fly == ONP_FLY_DON:
		mc.gotoAndPlay("don_hit")
	elif onp_fly == ONP_FLY_KATSU:
		mc.gotoAndPlay("katsu_hit")
	elif onp_fly == ONP_FLY_DON_DAI_BIG:
		mc.gotoAndPlay("don_d_hit")
	elif onp_fly == ONP_FLY_KATSU_DAI_BIG:
		mc.gotoAndPlay("katsu_d_hit")
	elif onp_fly == ONP_FLY_DON_DAI_SMALL:
		mc.gotoAndPlay("don_renda_d_hit")
	elif onp_fly == ONP_FLY_KATSU_DAI_SMALL:
		mc.gotoAndPlay("katsu_renda_d_hit")
	elif onp_fly == ONP_FLY_GEKI:
		mc.gotoAndPlay("geki_hit")
	if onp_fly != ONP_FLY_GEKI:
		movieclips[COURSE].gotoAndPlay("hit")
	
def set_tamashii(tamashii, _max_tamashii):
	global cur_tamashii, max_tamashii, movieclips, cur_dancer
	max_tamashii = _max_tamashii
	old_gauge_num = int(50.0 * cur_tamashii / max_tamashii + EPS)
	now_gauge_num = int(50.0 * tamashii / max_tamashii + EPS)
	cur_tamashii = tamashii
	now_dancer_num = 1 + now_gauge_num // 8
	
	if old_gauge_num != now_gauge_num:
		movieclips[GAUGE].gotoAndStop("gage_%02d" % now_gauge_num)
		
	if now_dancer_num > DANCER1 - cur_dancer + 1:
		add_dancer()
	
	if old_gauge_num < 40 and now_gauge_num >= 40:
		movieclips[DANCE_BG].gotoAndPlay("normal_fever")
		movieclips[DON].gotoAndStop("norm_up")
		movieclips[ENSO_UP_BG].gotoAndPlay("normal_fever")
	elif old_gauge_num >= 40 and now_gauge_num < 40:
		movieclips[DANCE_BG].gotoAndPlay("fever_normal")
		movieclips[DON].gotoAndStop("norm_down")
	elif old_gauge_num < 50 and now_gauge_num >= 50:
		movieclips[FEVER].fever.gotoAndPlay(fever_start_label)
		movieclips[DON].gotoAndStop("full_gage")
		movieclips[GAUGE].fever.gotoAndPlay("fever_start")
		movieclips[GAUGE].fever_gage.gotoAndPlay("toFever")
	elif old_gauge_num >= 50 and now_gauge_num < 50:
		movieclips[FEVER].fever.gotoAndPlay(fever_end_label)
		movieclips[GAUGE].fever.gotoAndPlay("fever_end")
		movieclips[GAUGE].fever_gage.gotoAndPlay("toNormal")
		reset_don()
			
def set_gogotime(is_ggt):
	global movieclips, cur_ggt
	global cur_tamashii, max_tamashii
	
	now_gauge_num = int(50.0 * cur_tamashii / max_tamashii + EPS)
	
	if is_ggt:
		cur_ggt = True
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_start")
		movieclips[MATO].gotoAndPlay("sabi_in")
		
		if now_gauge_num >= 50:
			movieclips[DON].gotoAndStop("full_sabi")
		else:
			movieclips[DON].gotoAndStop("sabi")
			
		movieclips[SPLASH].gotoAndPlay(splash_start_label)
			
	else:
		cur_ggt = False
		movieclips[BG_SAB_EFFECTI].gotoAndPlay("sabi_end")
		movieclips[MATO].gotoAndPlay("sabi_out")
		reset_don()
		
def reset_don():
	global movieclips, cur_tamashii, cur_ggt, cur_miss
	now_gauge_num = int(50.0 * cur_tamashii / max_tamashii + EPS)
	
	don = movieclips[DON]
	if cur_miss >= 6:
		don.gotoAndStop("miss_6")
	elif now_gauge_num < 40:
		if not cur_ggt:
			don.gotoAndPlay("normal")
		else:
			don.gotoAndStop("sabi")
	elif now_gauge_num < 50:
		if not cur_ggt:
			don.gotoAndPlay("norm_idle")
		else:
			don.gotoAndPlay("full_sabi")
	else:
		if not cur_ggt:
			don.gotoAndPlay("full_gage_idle")
		else:
			don.gotoAndPlay("full_sabi")
		
def set_renda_num(num):
	global movieclips, cur_renda
	cur_renda = num
	
	num100 = num // 100
	num10 = (num - num100 * 100) // 10
	num1 = num - num100 * 100 - num10 * 10
	
	mc = movieclips[RENDA_NUM]
	mc.gotoAndPlay("renda_hit")
	
	mc_number = mc.renda_hukidashi
	if num100 > 0:
		mc_number.gotoAndPlay("renda_hit_100")
		mc_number.geki_num_00.gotoAndPlay("number_%d" % num1)
		mc_number.geki_num_10.gotoAndPlay("number_%d" % num10)
		mc_number.geki_num_100.gotoAndPlay("number_%d" % num100)
	elif num10 > 0:
		mc_number.gotoAndPlay("renda_hit_10")
		mc_number.geki_num_00.gotoAndPlay("number_%d" % num1)
		mc_number.geki_num_10.gotoAndPlay("number_%d" % num10)
	else:
		mc_number.gotoAndPlay("renda_hit_00")
		mc_number.geki_num_00.gotoAndPlay("number_%d" % num1)
		
def set_renda_out():
	global movieclips, cur_renda
	if cur_renda > 0:
		cur_renda = 0
		mc = movieclips[RENDA_NUM]
		mc.gotoAndPlay("renda_out")
	
def set_renda_red(head, body, tail, hit_cnt):
	return

def set_branch(has_branch, level):
	global movieclips, cur_level
	mc = movieclips[LANE]
	if not has_branch:
		mc.bunki_moji.gotoAndPlay("no_bunki")
		return
	if cur_level is None:
		cur_level = "normal"
		mc.bunki_moji.gotoAndPlay("normal_start")
	elif cur_level != level:
		mc.bunki_moji.gotoAndPlay("%s>%s" % (cur_level, level))
		if cur_level == "normal" \
				or (cur_level == "kurouto" and level =="tatsujin"):
			movieclips[FUKIDASHI].gotoAndPlay("level_up")
		else:
			movieclips[FUKIDASHI].gotoAndPlay("level_down")
	cur_level = level
		
def on_hit_judge(onp, hit_keys, hit_judge, hitaway):
	global movieclips
	
	hit_big = (hit_judge & HITJUDGE_DAI) > 0
	
	enso_hiteffects = None
	enso_mato = None
	enso_hitjudge = None
	onp_fly = None
	
	enso_hiteffects_type = None
	
	enso_hiteffects_type_str = ("don", "katsu")
	if hit_keys & HIT_DON:
		enso_hiteffects_type = 0
	elif hit_keys & HIT_KATSU:
		enso_hiteffects_type = 1
	else:
		enso_hiteffects_type = 2
		
	if hit_judge == HITJUDGE_NO:
		if enso_hiteffects_type < 2:
			enso_hiteffects = "%s_s" % enso_hiteffects_type_str[enso_hiteffects_type]
		else:
			enso_hiteffects = "none"
		enso_mato = enso_hitjudge = "hit_no"
		onp_fly = ONP_FLY_NONE
	else:
		_, _, onp_flys, _, onp_fly_on_break = ONP_CFG[onp]
		
		if hit_judge == HITJUDGE_FUKA:
			enso_hiteffects = "none"
		else:
			enso_hiteffects = "%s_hit" % enso_hiteffects_type_str[enso_hiteffects_type]
		
		if hit_judge == HITJUDGE_HIT:
			enso_mato = enso_hitjudge = "hit_no"
		elif hit_judge == HITJUDGE_FUKA:
			enso_mato = enso_hitjudge = "hit_huka"
		elif hit_judge == HITJUDGE_KA:
			enso_mato = enso_hitjudge = "hit_ka"
		elif hit_judge == HITJUDGE_RYO:
			enso_mato = enso_hitjudge = "hit_ryo"
		elif hit_judge == HITJUDGE_RYO_DAI:
			enso_mato = "hit_dai_ryo"
			enso_hitjudge = "hit_ryo_big"
		elif hit_judge == HITJUDGE_KA_DAI:
			enso_mato = "hit_dai_ka"
			enso_hitjudge = "hit_ka_big"
		else:
			enso_mato = enso_hitjudge = "hit_no"
			print "[WARNING] unknown hit_judge %d" % hit_judge
		
		if onp_fly_on_break != hitaway or hit_judge == HITJUDGE_FUKA:
			onp_fly = ONP_FLY_NONE
		else:
			onp_fly = onp_flys[enso_hiteffects_type + int(hit_big) * 2]
			
		#print enso_mato, enso_hiteffects, enso_hitjudge, onp_fly
	
	if enso_hitjudge != "hit_no":
		movieclips[HITJUDGE].hit.gotoAndPlay(enso_hitjudge)
	if enso_hiteffects != "none":
		movieclips[LANE].effect.gotoAndPlay(enso_hiteffects)
	if enso_mato != "hit_no":
		movieclips[MATO].hit.gotoAndPlay(enso_mato)
	if onp_fly != ONP_FLY_NONE:
		play_onp_fly(onp_fly)

	# chibi and rendaeffects
	if hit_judge == HITJUDGE_NO:
		pass
	elif hit_judge == HITJUDGE_HIT and onp in (ONP_RENDA1, ONP_RENDA_DAI1):
		mc = movieclips[RENDA_EFFECT].alloc(INDEX_RENDA_EFFECT)
		if mc: 
			x_range = enso_cfg.RENDA_EFFECT_X_RANGE
			y_range = enso_cfg.RENDA_EFFECT_Y_RANGE
			x = random.randint(x_range[0], x_range[1])
			y = random.randint(y_range[0], y_range[1])
			mc.set_pos(x, y)
			enso_cfg.RENDA_EFFECT_FUNC(mc, random.randint(1, enso_cfg.RENDA_EFFECT_NUM))
	elif hit_judge == HITJUDGE_HIT and onp in (ONP_GEKI, ONP_IMO):
		pass
	elif hit_judge == HITJUDGE_FUKA:
		pass
	else: #HITJUDGE_KA, HITJUDGE_KA_DAI, HITJUDGE_RYO, HITJUDGE_RYO_DAI
		assert onp in (HITJUDGE_KA, HITJUDGE_KA_DAI, HITJUDGE_RYO, HITJUDGE_RYO_DAI)
		mc = movieclips[CHIBI].alloc(INDEX_CHIBI_HIT)
		if mc: mc.gotoAndPlay(0)
		
def on_hit(keys):
	global movieclips, cur_miss
	global dong, ka
	
	if cur_miss > 0:
		now_gauge_num = int(50.0 * cur_tamashii / max_tamashii + EPS)
		if now_gauge_num < 40:
			movieclips[ENSO_UP_BG].gotoAndPlay("miss_normal")
		else:
			movieclips[ENSO_UP_BG].gotoAndPlay("miss_fever")

	if keys & HIT_DON:
		player = dong.play()
		player.volume = 2.0
	if keys & HIT_KATSU:
		player = ka.play()
		player.volume = 2.0        
	
def draw_geki_or_imo(render_state, operation, lumen, x, end_x):
	if x > ONP_HIT_X:
		lumen.set_pos(x, ONP_Y)
	elif end_x > ONP_HIT_X:
		lumen.set_pos(ONP_HIT_X, ONP_Y)
	else:
		lumen.set_pos(end_x, ONP_Y)
	lumen.update(render_state, operation & lm_consts.MASK_DRAW)
	
def draw_renda(render_state, operation, lumen_head, lumen_body, lumen_tail, x, end_x):
	set_renda_red(lumen_head, lumen_body, lumen_tail, 0)

	x_body = max(x, ONP_OUT_X)
	body_len = end_x - x_body
	lumen_body.set_pos(x_body, ONP_Y)
	lumen_body.matrix.scale = (body_len / 32.0 ,1.0)
	lumen_body.update(render_state, operation & lm_consts.MASK_DRAW)
	
	lumen_head.set_pos(x, ONP_Y)
	lumen_head.update(render_state, operation & lm_consts.MASK_DRAW)
	
	lumen_tail.set_pos(end_x, ONP_Y)
	lumen_tail.update(render_state, operation & lm_consts.MASK_DRAW)

def set_onps(onps, state):
	global movieclips
	movieclips[ONPS].set_onps(onps, state)
	
class COnpRenderer(object):
	
	def __init__(self, onp_lumens):
		self._onp_lumens = onp_lumens
		self._onps = []
		self._offset = 0
		self._barline_on = False
		self.hit_onp_off = 0
		self.hit_onp_hits = 0
	
	def set_onps(self, onps, state):
		self._onps = onps
		self.offset = state.offset
		self.barline_on = state.barline_on
		self.hit_onp_off = state.hit_onp_off
		self.hit_onp_hits = state.hit_onp_hits
	
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		# update onp lumens without drawing
		for lumen in self._onp_lumens:
			lumen.update(render_state, operation & lm_consts.MASK_NO_DRAW)
			
		# draw from back to front
		end_note = None
		for off, onp, hits, spd in reversed(self._onps):
			x = ONP_HIT_X + (off - self.offset) * spd
			end_x = ONP_IN_X
			if (ONP_SHORT[0] <= onp <= ONP_SHORT[1]) \
				or (ONP_SYOUSETSU[0] <= onp <= ONP_SYOUSETSU[1] and self.barline_on):
				lumen = self._onp_lumens[onp]
				lumen.set_pos(x, ONP_Y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp == ONP_END:
				end_note = (off, onp, hits, spd)
			elif ONP_LONG[0] <= onp <= ONP_LONG[1]:
				if end_note is not None:
					end_x = ONP_HIT_X + (end_note[0] - self.offset) * end_note[3]
					end_note = None
				elif self.hit_onp_off > off: continue
				if onp == ONP_RENDA1:
					draw_renda(render_state, operation,
						self._onp_lumens[ONP_RENDA1], self._onp_lumens[ONP_RENDA2], self._onp_lumens[ONP_RENDA3], x, end_x)
				elif onp == ONP_RENDA_DAI1:
					draw_renda(render_state, operation,
						self._onp_lumens[ONP_RENDA_DAI1], self._onp_lumens[ONP_RENDA_DAI2], self._onp_lumens[ONP_RENDA_DAI3], x, end_x)
				elif onp == ONP_GEKI and (off != self.hit_onp_off or self.hit_onp_hits == 0):
					draw_geki_or_imo(render_state, operation, self._onp_lumens[ONP_GEKI], x, end_x)
				elif onp == ONP_IMO and (off > self._state.hit_onp_off):
					draw_geki_or_imo(render_state, operation, self._onp_lumens[ONP_IMO], x, end_x)
	
# Build up scene
def build_scene(cfg, loader):
	global INDEX_CHIBI_HIT, INDEX_CHIBI_MISS
	global INDEX_RENDA_EFFECT
	global INDEX_SCORE_ADD
	global INDEX_ONP_FLY
	global enso_cfg
	global movieclips
	
	enso_cfg = cfg
	
	LMC = loader.load_movie
	LMCS = loader.load_multi_movie
	LMP = loader.load_movie_pool
	don_cos = config.DATA["don_cos"] % ""
	
	movieclips = [None] * NUM_MOVIECLIP
	movieclips[DANCE_BG] = LMC(cfg.DANCE_BG, cfg.DANCE_BG_POS)
	movieclips[ENSO_UP_BG] = LMC(cfg.ENSO_UP_BG)
	movieclips[BG_SAB_EFFECTI] = LMC(cfg.BG_SAB_EFFECTI, cfg.BG_SAB_EFFECTI_POS)
	movieclips[COURSE] = LMC(cfg.COURSE, cfg.COURSE_POS)
	movieclips[DON] = loader.load_movie_cos(cfg.DON, don_cos, 4, cfg.DON_POS)
	movieclips[DON].speed = 1.5
	movieclips[DON].register_callback("on_trans_animation_end", on_trans_animation_end, None)
	movieclips[GAUGE] = LMC(cfg.GAUGE, cfg.GAUGE_POS)
	# Load renda effect
	_def = (((cfg.RENDA_EFFECT, 30),),)
	movieclips[RENDA_EFFECT] = LMP(_def)
	INDEX_RENDA_EFFECT, = range(len(_def))
	movieclips[SONG_NAME] = LMC(cfg.SONG_NAME, cfg.SONG_NAME_POS)
	movieclips[DANCER1] = LMC(cfg.DANCER1, cfg.DANCER1_POS)
	movieclips[DANCER2] = LMC(cfg.DANCER2, cfg.DANCER2_POS)
	movieclips[DANCER3] = LMC(cfg.DANCER3, cfg.DANCER3_POS)
	movieclips[DANCER4] = LMC(cfg.DANCER4, cfg.DANCER4_POS)
	movieclips[DANCER5] = LMC(cfg.DANCER5, cfg.DANCER5_POS)
	for dancer in xrange(DANCER5, DANCER1 + 1):
		movieclips[dancer].active = False
		movieclips[dancer].register_callback("on_dancer_in_end", on_dancer_in_end, dancer)
	movieclips[LANE] = LMC(cfg.LANE, cfg.LANE_POS)
	movieclips[MATO] = LMC(cfg.MATO, cfg.MATO_POS)
	# ONPS	
	onp_lumens = []
	for filename in cfg.ONPS:
		onp_lumens.append(LMC(filename))
	onp_lumens[ONP_SYOUSETSU_NORMAL].gotoAndStop("normal")
	onp_lumens[ONP_SYOUSETSU_BUNKI].gotoAndStop("bunki")	
	movieclips[FULLCOMBO] = LMC(cfg.FULLCOMBO, cfg.FULLCOMBO_POS)
	movieclips[TAIKO] = LMC(cfg.TAIKO, cfg.TAIKO_POS)
	movieclips[COMBO] = LMC(cfg.COMBO, cfg.COMBO_POS)
	movieclips[HITJUDGE] = LMC(cfg.HITJUDGE, cfg.HITJUDGE_POS)
	movieclips[CHOCHIN] = LMC(cfg.CHOCHIN, cfg.CHOCHIN_POS)
	# Load chibi
	_def = ([], ((cfg.CHIBI_MISS, 40, cfg.CHIBI_MISS_POS),),)
	for chibi_lm, chibi_x, chibi_y in cfg.CHIBI:
		_def[0].append((chibi_lm, 40 / len(cfg.CHIBI), (chibi_x, chibi_y)))
	movieclips[CHIBI] = LMP(_def)
	INDEX_CHIBI_HIT, INDEX_CHIBI_MISS = range(len(_def))
	movieclips[CHIBI].speed = 2
	# Load onp fly
	_def = (((cfg.ONP_FLY, 30, cfg.ONP_FLY_POS),),)
	movieclips[ONP_FLY] = LMP(_def)
	INDEX_ONP_FLY, = range(len(_def))
	movieclips[RENDA_NUM] = LMC(cfg.RENDA_NUM, cfg.RENDA_NUM_POS)
	movieclips[FUKIDASHI] = LMC(cfg.FUKIDASHI, cfg.FUKIDASHI_POS)
	movieclips[SCORE_MAIN] = LMC(cfg.SCORE_MAIN, cfg.SCORE_MAIN_POS)
	# Load score add
	_def = (((cfg.SCORE_ADD, 10, cfg.SCORE_ADD_POS),),)
	movieclips[SCORE_ADD] = LMP(_def)
	INDEX_SCORE_ADD, = range(len(_def))
	# DON_GEKI
	movieclips[DON_GEKI] = loader.load_movie_cos(cfg.DON_GEKI, don_cos, 4, cfg.DON_GEKI_POS)
	movieclips[DON_GEKI].active = False
	movieclips[DON_GEKI].register_callback("on_geki_end", on_balloon_end, None)
	
	# display mekakushi only when widescreen is set
	if config.DATA["widescreen"]:
		movieclips[MEKAKUSHI] = LMC(cfg.MEKAKUSHI)
		
	movieclips[FEVER] = LMC(cfg.FEVER, cfg.FEVER_POS)
	movieclips[FEVER].speed = 2
	movieclips[DON_IMO] = loader.load_movie_cos(cfg.DON_IMO, don_cos, 4, cfg.DON_IMO_POS)
	movieclips[DON_IMO].active = False
	movieclips[DON_IMO].register_callback("on_imo_end", on_imo_break_end, None)	
	movieclips[IMO] = LMC(cfg.IMO, cfg.IMO_POS)
	movieclips[IMO].register_callback("on_imo_in_end", on_imo_in_end, None)
	movieclips[SPLASH] = LMC(cfg.SPLASH, cfg.SPLASH_POS)
	
	# Init fumen
	movieclips[ONPS] = COnpRenderer(onp_lumens)
	
	# Pre load
	movieclips[DANCE_BG].gotoAndPlay("normal_fever")
	movieclips[DANCE_BG].gotoAndPlay("fever")
	movieclips[DANCE_BG].gotoAndPlay("fever_normal")
	movieclips[DANCE_BG].gotoAndPlay("normal")

	movieclips[SPLASH].gotoAndPlay(splash_start_label)
	movieclips[SPLASH].gotoAndPlay("wait")

	return movieclips
	
def on_update(dt):
	global enso_started
	global movieclips, fumen_mgr
	global music_player
	global fumen_started, music_started
	
	# Enso logic
	if enso_started:
		fumen_off = fumen_mgr._state.offset
		if not music_started:
			if fumen_off < 0:
				fumen_started = True
			if fumen_off >= 0:
				music_player.seek(0)
				music_player.play()
				music_started = True
				fumen_mgr._state.offset = 0
				fumen_started = True
				print "way1"
		elif not fumen_started and music_player.time * 1000.0 >= fumen_off:
			fumen_started = True
			fumen_mgr._state.offset = music_player.time * 1000.0
			print "way2"
	
		# Fumen advance
		if fumen_started:
			fumen_mgr.update()
			fumen_mgr._state.offset += dt * 1000.0			
			
	# Rendering
	
	#glClearColor(1, 1, 1, 1)
	#window.clear()
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
			
	glOrtho(left, right, bottom, top, -1, 1)

	renderer.begin()
	
	for movieclip in movieclips:
		#if movieclip not in (movieclips[SONG_NAME], ): continue
		if movieclip is None: continue
		movieclip.update(renderer)
			
	renderer.end()
	
	glScalef(1.0, -1.0, 1.0)
	
	# Draw song name
	if config.DATA["use_texture_as_song_name"]:
		song_name_label.blit(640, -235)
	else:
		song_name_label.draw()

def setup_viewport():
	global left, right, top, bottom	
	cfg = config.DATA
	
	width = cfg["wnd_width"]
	height = cfg["wnd_height"]
	left = top = 0
	right = width
	bottom = height
	if cfg["widescreen"]:
		left -= cfg["widescreen_padding"]
		right += cfg["widescreen_padding"]

def on_enter(this):
	# Update config
	on_config_update()
	
	# Init enso data
	init_enso_data()

	# init movieclips
	global movieclips
	global loader
	global renderer
	global fumen_mgr
	global song_name_label
	global dong, ka
	global music_player
	global music_started, fumen_started, enso_started
	
	if movieclips is None:
		renderer = lm_render_state.CRenderer()
		renderer.init()
	
		cfg = config.DATA
		loader = lm_loader.CLoader("wii", cfg["lm_root"], renderer)
		movieclips = build_scene(cfg["enso_skin"], loader)
		
		fumen_mgr = tja_onp_mgr.CMgr()

		# Load SE
		dong = pyglet.resource.media("dong2.mp3", streaming=False)
		ka = pyglet.resource.media("ka2.mp3", streaming=False)
		
		setup_viewport()

		
	pyglet.resource.path.append(os.path.split(config.DATA["fumen_file"])[0])	
	pyglet.resource.reindex()

	fumen_mgr.reset(this, config.DATA["fumen_file"], config.DATA["enso_option"])
	song_name = fumen_mgr.get_song_name()
	
	if config.DATA["use_texture_as_song_name"]:
		song_name_label = pyglet.image.load(config.DATA["def_song_name_label"])
		song_name_label.anchor_x = song_name_label.width
		song_name_label.anchor_y = song_name_label.height / 2
	else:
		song_name_label = pyglet.text.Label(song_name, "DFKanTeiRyu-W11", color=(255, 255, 255, 255),
			x=630, y=-240, width=640, height=35, anchor_x="right", anchor_y="center",
			font_size=20)

	# Load WAVE
	audio_file = fumen_mgr.get_audio_file()
	music = pyglet.resource.media(audio_file, streaming=False)
	music_player = music.play()
	music_player.pause()
	music_player.volume = fumen_mgr._fumen.header["SONGVOL"] / 100.0
	
	music_started = False
	fumen_started = False
	enso_started = False

def on_exit():
	pass

def on_key_press(symbol, modifiers):
	global fumen_mgr, enso_started
	if enso_started:
		if symbol == pyglet.window.key.F:
			fumen_mgr.add_key(HIT_LEFT_DON)
		elif symbol == pyglet.window.key.J:
			fumen_mgr.add_key(HIT_RIGHT_DON)
		elif symbol == pyglet.window.key.R:
			fumen_mgr.add_key(HIT_LEFT_KATSU)
		elif symbol == pyglet.window.key.U:
			fumen_mgr.add_key(HIT_RIGHT_KATSU)
	elif symbol == pyglet.window.key.J:
		enso_started = True
		add_dancer()
	if symbol == pyglet.window.key.SPACE:
		game_state.set_game_state(game_state.GAME_STATE_SONG_SELECT)
