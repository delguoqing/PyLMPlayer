###################
# ONP DEFINE
###################
ONP_DON = 0
ONP_KATSU = 1
ONP_DON_DAI = 2
ONP_KATSU_DAI = 3

ONP_SHORT = 0, 3
#-----------------------------

ONP_SYOUSETSU_NORMAL = 4
ONP_SYOUSETSU_BUNKI = 5

ONP_SYOUSETSU = 4, 5
#-----------------------------

ONP_RENDA1 = 6
ONP_RENDA_DAI1 = 7
ONP_GEKI = 8
ONP_IMO = 9

ONP_LONG = 6, 9
#-----------------------------
ONP_RENDA2 = 10			# Renda onp body
ONP_RENDA3 = 11			# Renda onp tail
ONP_RENDA_DAI2 = 12		# Renda onp(dai) body
ONP_RENDA_DAI3 = 13		# Renda onp(dai) tail
ONP_END = 14
ONP_IMO_HIGH = 15

ONP_MAX = 15

###################
# ONP FLY DEFINE
###################
ONP_FLY_NONE = 0
ONP_FLY_DON = 1
ONP_FLY_KATSU = 2
ONP_FLY_DON_DAI = 3
ONP_FLY_KATSU_DAI = 4
ONP_FLY_GEKI = 5

###################
# HIT DEFINE
###################
HIT_LEFT_DON = 1
HIT_RIGHT_DON = 2
HIT_LEFT_KATSU = 4
HIT_RIGHT_KATSU = 8
HIT_INVALID = 16
HIT_DON = HIT_LEFT_DON | HIT_RIGHT_DON
HIT_KATSU = HIT_LEFT_KATSU | HIT_RIGHT_KATSU
HIT_ANY = HIT_DON | HIT_KATSU

###################
# ONP CONFIG:
# 1. valid_keys: (input_keys & valid_keys) > 0 ===> count as a hit
# 2. big_hit_keys: (input_keys & big_hit_keys) == big_hit_keys ===> count as a big hit
# 3. onp_fly_define:
# 4. key_buffer_time:
# 5. show onp fly on onp hit break
###################
ONP_CFG = [None] * (ONP_MAX + 1)
ONP_CFG[ONP_DON] = (
	HIT_DON,
	HIT_INVALID,
	(ONP_FLY_DON, ONP_FLY_NONE, ONP_FLY_NONE, ONP_FLY_NONE),
	0,
	True,
)
ONP_CFG[ONP_KATSU] = (
	HIT_KATSU,
	HIT_INVALID,
	(ONP_FLY_NONE, ONP_FLY_KATSU, ONP_FLY_NONE, ONP_FLY_NONE),
	0,
	True,
)
ONP_CFG[ONP_DON_DAI] = (
	HIT_DON,
	HIT_DON,
	(ONP_FLY_DON, ONP_FLY_NONE, ONP_FLY_DON_DAI, ONP_FLY_NONE),
	1,
	True,
)
ONP_CFG[ONP_KATSU_DAI] = (
	HIT_KATSU,
	HIT_KATSU,
	(ONP_FLY_NONE, ONP_FLY_KATSU, ONP_FLY_NONE, ONP_FLY_KATSU_DAI),
	1,
	True,
)
ONP_CFG[ONP_RENDA1] = (
	HIT_ANY,
	HIT_INVALID,
	(ONP_FLY_DON, ONP_FLY_KATSU, ONP_FLY_NONE, ONP_FLY_NONE),
	0,
	False,
)
ONP_CFG[ONP_RENDA_DAI1] = (
	HIT_ANY,
	HIT_INVALID,
	(ONP_FLY_DON_DAI, ONP_FLY_KATSU_DAI, ONP_FLY_NONE, ONP_FLY_NONE),
	0,
	False,
)
ONP_CFG[ONP_GEKI] = (
	HIT_DON,
	HIT_INVALID,
	(ONP_FLY_GEKI, ONP_FLY_NONE, ONP_FLY_NONE, ONP_FLY_NONE),
	0,
	True,
)
ONP_CFG[ONP_IMO] = (
	HIT_DON,
	HIT_INVALID,
	(ONP_FLY_NONE, ONP_FLY_NONE, ONP_FLY_NONE, ONP_FLY_NONE),
	0,
	True,
)
###################
# OPTIONS
###################
OPTION_SPD_2x = 1
OPTION_SPD_3x = 2
OPTION_SPD_4x = 3
OPTION_SPD_MASK = 3

OPTION_AUTO = 4
OPTION_AUTO_MASK = 4

OPTION_ONP_MIRROR = 8
OPTION_ONP_RANDOM = 16
OPTION_ONP_SRANDOM = 24
OPTION_ONP_MASK = 24