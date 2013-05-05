LM_PACK_ROOT = r"../packages"
DON_ATAMA = (r"../packages/pack301", 29)
DON_KARADA = (r"../packages/pack330", 29)

# Dance BG
DANCE_BG = r"pack121/DANCE_BG_IDOL.LM"
# Enso up bg. Scrolling from left to right.
ENSO_UP_BG = r"pack99/ENSO_UP_BG_03.LM"
# sabi effect. When game enters gogotime. This is drawn on top of up bg.
BG_SAB_EFFECTI = r"pack97/BG_SAB_EFFECTI.LM"

# Renda effect,
# This is really weird!!! Renda effects are not made in the same standard!
def RENDA_EFFECT_FUNC0(mc, style):
	mc.p1.gotoAndStop("dori_0%d" % style)
	mc.p1.object.gotoAndPlay(0)
	
def RENDA_EFFECT_FUNC1(mc, style):
	mc.p1.gotoAndStop("syuriken_0%d" % style)
	mc.p1.object.gotoAndPlay(0)	
	
def RENDA_EFFECT_FUNC2(mc, style):
	mc.gotoAndPlay("hamaya_start")

# Renda Effect hamachidori
	
#RENDA_EFFECT = r"pack90/RENDA_EFFECT_HAMACHIDORI.LM"
#RENDA_EFFECT_NUM = 6
#RENDA_EFFECT_X_RANGE = (-10, 10)
#RENDA_EFFECT_Y_RANGE = (200, 272)
#RENDA_EFFECT_FUNC = RENDA_EFFECT_FUNC0

#RENDA_EFFECT = r"pack92/RENDA_EFFECT_SYURIKEN.LM"
#RENDA_EFFECT_NUM = 6
#RENDA_EFFECT_X_RANGE = (0, 0)
#RENDA_EFFECT_Y_RANGE = (0, 272)
#RENDA_EFFECT_FUNC = RENDA_EFFECT_FUNC1

RENDA_EFFECT = r"pack91/RENDA_EFFECT_HAMAYA.LM"
RENDA_EFFECT_NUM = 1
RENDA_EFFECT_X_RANGE = (-10, 10)
RENDA_EFFECT_Y_RANGE = (200, 272)
RENDA_EFFECT_FUNC = RENDA_EFFECT_FUNC2

# Dancers: (Appear in the  following order)
# 4    2    1    3    5

#DANCER5 = r"pack352/DANCE_IDOL_HARUKA.LM"
#DANCER4 = r"pack352/DANCE_IDOL_HIBIKI.LM"
#DANCER3 = r"pack352/DANCE_IDOL_TAKANE.LM"
#DANCER2 = r"pack352/DANCE_IDOL_MIKI.LM"
#DANCER1 = r"pack352/DANCE_IDOL_MAMI.LM"

DANCER5 = r"pack355/DANCE_MIKU_05.LM"
DANCER4 = r"pack355/DANCE_MIKU_04.LM"
DANCER3 = r"pack355/DANCE_MIKU_03.LM"
DANCER2 = r"pack355/DANCE_MIKU_02.LM"
DANCER1 = r"pack355/DANCE_MIKU_01.LM"

# Fever(Appear when tamashii gauge is full.)
FEVER = r"pack359/FEVER_IDOL.LM"

# Course icon. not affected by sabi effect.
COURSE = r"pack63/COURSE_ONI.LM"
# Character don.(At normal states)
DON = r"pack363/DON_COS00_DIET.LM"
# The tamashi gauge
GAUGE = r"pack66/GAUGE_DON_H.LM"

CHIBI = (
	r"pack85/CHIBI_1P_IDOL_01.LM",
	r"pack85/CHIBI_1P_IDOL_02.LM",
	r"pack85/CHIBI_1P_IDOL_03.LM",
	r"pack85/CHIBI_1P_IDOL_04.LM",
)

CHIBI_MISS = r"pack84/CHIBI_TAMA_01.LM"

LANE = r"pack44/ENSO_LANE.LM"
HITEFFECTS = r"pack44/ENSO_HITEFFECTS.LM"
BUNKI = r"pack44/ENSO_BUNKI.LM"
MATO_GOGO = r"pack44/ENSO_MATO_GOGO.LM"
BUNKI_MOJI = r"pack44/ENSO_BUNKI_MOJI.LM"
MATO = r"pack44/ENSO_MATO.LM"
FULLCOMBO = r"pack45/ENSO_FULLCOMBO.LM"

# =========> onps <====================

# The taiko.
TAIKO = r"pack44/ENSO_TAIKO.LM"
# Left/Right Don/Kats.
LEFT_DON = r"pack44/ENSO_LEFT_DON.LM"
LEFT_KATS = r"pack44/ENSO_LEFT_KATS.LM"
RIGHT_DON = r"pack44/ENSO_RIGHT_DON.LM"
RIGHT_KATS = r"pack44/ENSO_RIGHT_KATS.LM"
# Combo number and Cherry(every 100 combo).
COMBO = r"pack44/ENSO_COMBO.LM"

# [WARNING!!!]Maintain order!!!
ONP_FLY = (
	r"pack43/ONP_FLY_DON.LM",
	r"pack43/ONP_FLY_DON_D.LM",
	r"pack43/ONP_FLY_KATSU.LM",
	r"pack43/ONP_FLY_KATSU_D.LM",
	r"pack43/ONP_FLY_GEKI.LM",		
)

# Hitjudge
HITJUDGE = r"pack44/ENSO_HITJUDGE.LM"

BALLOON = r"pack53/DON_GEKI_1P.LM"
IMO = r"pack54/IMO.LM"

#######################
# HUD Part!
#######################
# Scores.
# Score Add: How many score is added in the last hit
# Score Main: The total score.
# Fukidashi: The current combo(every 10 combo), Level up, Level down, Miss
# Renda Num: The current hit of the renda onp
FUKIDASHI = r"pack52/DON_1P_FUKIDASHI.LM"
RENDA_NUM = r"pack52/RENDA_NUM.LM"
SCORE_ADD = r"pack50/ENSO_SCORE_ADD.LM"
SCORE_MAIN = r"pack50/ENSO_SCORE_MAIN.LM"