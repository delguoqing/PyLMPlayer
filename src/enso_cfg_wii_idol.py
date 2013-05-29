LM_PACK_ROOT = r"../wii_packages"

# Character don.
DON = r"don/don_1p/don_1p.lm"
DON_POS = (-37, -69)

DON_COS = r"don/cos/cos_012/cos_012_1p/cos_012_1p.lm"

DON_GEKI = r"don/don_geki_1p/don_geki_1p.lm"
DON_GEKI_POS = (36, 57)

DON_IMO = r"don/don_imo_1p/don_imo_1p.lm"
DON_IMO_POS = (0, 0)

# Dance BG
DANCE_BG = r"enso_dance/dance_bg_idol/dance_bg_idol.lm"
DANCE_BG_POS = (0, 253)
# Chochin
CHOCHIN = r"enso/chochin_idol/chochin_idol.lm"
CHOCHIN_POS = (-1, 435)
# Enso up bg. Scrolling from left to right.
ENSO_UP_BG = r"enso/bg/enso_1p_bg_12/enso_1p_bg_12.lm"
ENSO_UP_BG_POS = (0, 0)
# sabi effect. When game enters gogotime. This is drawn on top of up bg.
BG_SAB_EFFECTI = r"enso/sabi_1p/sabi_1p.lm"
BG_SAB_EFFECTI_POS = (0, 0)

# Renda effect,
# This is really weird!!! Renda effects are not made in the same standard!
def RENDA_EFFECT_FUNC3(mc, style):
	mc.gotoAndPlay("p1")
	mc.p1.gotoAndPlay("dori_0%d" % style)

# Renda Effect hamachidori

RENDA_EFFECT = r"enso/renda_effect_hamachidori/renda_effect_hamachidori.lm"
RENDA_EFFECT_NUM = 6
RENDA_EFFECT_X_RANGE = (-10, 10)
RENDA_EFFECT_Y_RANGE = (400, 480)
RENDA_EFFECT_FUNC = RENDA_EFFECT_FUNC3

# Dancers: (Appear in the  following order)
# 4    2    1    3    5

DANCER5 = r"enso_dance/dance_idol_miki/dance_idol_miki.lm"
DANCER4 = r"enso_dance/dance_idol_mami/dance_idol_mami.lm"
DANCER3 = r"enso_dance/dance_idol_chihaya/dance_idol_chihaya.lm"
DANCER2 = r"enso_dance/dance_idol_hibiki/dance_idol_hibiki.lm"
DANCER1 = r"enso_dance/dance_idol_haruka/dance_idol_haruka.lm"
DANCER5_POS = (580, 436)
DANCER4_POS = (60, 436)
DANCER3_POS = (450, 436)
DANCER2_POS = (190, 436)
DANCER1_POS = (320, 436)

# Fever(Appear when tamashii gauge is full.)
FEVER = r"enso/fever/fever_idol7/fever_idol7.lm"
FEVER_POS = (0, 301)

# Course icon. not affected by sabi effect.
COURSE = r"enso/course_oni/course_oni.lm"
COURSE_POS = (86, -70)
# The tamashi gauge
GAUGE = r"enso/gage_don_h/gage_don_h.lm"
GAUGE_POS = (264.5, 17)

CHIBI = (
	(r"enso_chibi/chibi_1p_idol_01/chibi_1p_idol_01.lm", 0, -32),
	(r"enso_chibi/chibi_1p_idol_02/chibi_1p_idol_02.lm", 0, -32),
	(r"enso_chibi/chibi_1p_idol_03/chibi_1p_idol_03.lm", 0, -32),
	(r"enso_chibi/chibi_1p_idol_04/chibi_1p_idol_04.lm", 0, -32),
)

CHIBI_MISS = r"enso/enso_chibi/chibi_1p_tama_01/chibi_1p_tama_01.lm"
CHIBI_MISS_POS = (0, 0)

LANE = r"enso/enso_lane/enso_lane.lm"
LANE_POS = (104, 107)
MATO = r"enso/enso_lane_hit/enso_lane_hit.lm"
MATO_POS = (150, 154)

FULLCOMBO = r"enso/fullcombo1/fullcombo1.lm"
FULLCOMBO_POS = (104, 107)

ONPS = (
	r"enso/onp/onp_don/onp_don.lm", 
	r"enso/onp/onp_katsu/onp_katsu.lm",
	r"enso/onp/onp_don_dai/onp_don_dai.lm",
	r"enso/onp/onp_katsu_dai/onp_katsu_dai.lm",
	r"enso/syousetsu/syousetsu.lm",
	r"enso/syousetsu/syousetsu.lm",
	r"enso/onp/onp_renda01/onp_renda01.lm",
	r"enso/onp/onp_d_renda01/onp_d_renda01.lm",
	r"enso/onp/onp_geki01/onp_geki01.lm",
	r"enso/onp/onp_imo/onp_imo.lm",
	r"enso/onp/onp_renda02/onp_renda02.lm",
	r"enso/onp/onp_renda03/onp_renda03.lm",
	r"enso/onp/onp_d_renda02/onp_d_renda02.lm",
	r"enso/onp/onp_d_renda03/onp_d_renda03.lm",
)

# The taiko.(No taiko, just mii)
TAIKO = r"enso/enso_1p_taiko/enso_1p_taiko.lm"
TAIKO_POS = (-10, 102)

MEKAKUSHI = r"enso/mekakushi_1p_kingyo/mekakushi_1p_kingyo.lm"
MEKAKUSHI_POS = (0, 0)

# Combo number and Cherry(every 100 combo).
COMBO = r"enso/enso_number/enso_number.lm"
COMBO_POS = (-10, 64)

# onp flys are combined in only one file
ONP_FLY = r"enso/onp/onp_hit_don_2p/onp_hit_don_2p.lm"
ONP_FLY_POS = (149, 154)

# Hitjudge
HITJUDGE = r"enso/enso_lane_hit_effect/enso_lane_hit_effect.lm"
HITJUDGE_POS = (149, 154)

IMO = r"enso/imo_1p/imo_1p.lm"
IMO_POS = (-107, 0)

#######################
# HUD Part!
#######################
# Scores.
# Score Add: How many score is added in the last hit
# Score Main: The total score.
# Fukidashi: The current combo(every 10 combo), Level up, Level down, Miss
# Renda Num: The current hit of the renda onp
FUKIDASHI = r"enso/don_1p_fukidashi/don_1p_fukidashi.lm"
FUKIDASHI_POS = (-30, -60)
RENDA_NUM = r"enso/renda_num/renda_num.lm"
RENDA_NUM_POS = (-32, -45)
SCORE_ADD = r"enso/enso_score_add/enso_score_add.lm"
SCORE_ADD_POS = (464, 78)
SCORE_MAIN = r"enso/enso_score/enso_score.lm"
SCORE_MAIN_POS = (464, 78)

SPLASH = r"enso/combo_splash/combo_splash.lm"
SPLASH_POS = (0, 0)