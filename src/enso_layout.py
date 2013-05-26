NUM_MOVIECLIP = 37
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

# Renda effect, 
RENDA_EFFECT,

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
# Character don.(At normal states)
DON,
# The tamashi gauge
GAUGE,

CHIBI,

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

ONPS,

# The taiko.
TAIKO, 
# Left/Right Don/Kats.
LEFT_DON, LEFT_KATS, RIGHT_DON, RIGHT_KATS, 
# Combo number and Cherry(every 100 combo).
COMBO,

ONP_FLY,

# Hitjudge
HITJUDGE, 

# Don chan will go above the enso lane at certain scenes.
# when player hits a balloon or a imo
DON2,
BALLOON,
IMO,

#######################
# HUD Part!
#######################
# Scores.
# Score Add: How many score is added in the last hit
# Score Main: The total score.
# Fukidashi: The current combo(every 10 combo), Level up, Level down, Miss
# Renda Num: The current hit of the renda onp
FUKIDASHI,
RENDA_NUM, 
SCORE_MAIN, SCORE_ADD,

) = range(NUM_MOVIECLIP)