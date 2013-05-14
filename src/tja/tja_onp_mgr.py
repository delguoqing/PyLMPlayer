import sys
sys.path.append("..")

import random
import tja_enso_state
from lm import lm_consts

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

def onp_rand_none(onp):
	return onp

def onp_rand_mirror(onp):
	if onp == "1": return "2"
	if onp == "2": return "1"
	if onp == "3": return "4"
	if onp == "4": return "3"
	return onp

def onp_rand_random(onp):
	use_rand = (random.random() <= 0.3)
	if not use_rand:
		return onp
	else:
		if onp == "1" or onp == "2":
			return random.random() <= 0.5 and "1" or "2"
		if onp == "3" or onp == "4":
			return random.random() <= 0.5 and "3" or "4"
	return onp

def onp_rand_srandom(onp):
	if onp == "1" or onp == "2":
		return random.random() <= 0.5 and "1" or "2"
	if onp == "3" or onp == "4":
		return random.random() <= 0.5 and "3" or "4"
	return onp

class CMgr(object):
	
	def __init__(self, fumen, options=0):
		self._glb_scroll = 1.0
		self._auto = False
		self._onp_rand = 0
		self._onp_rand_func = onp_rand_none
		self._fumen = fumen
		self._state = tja_enso_state.CEnsoState(self._fumen.header)
		self._onps = []
		self._onp_y = 107
		self._onp_hit_x = 104
		
		self.set_option(options)
		
	def set_option(self, options):
		self._auto = (options & OPTION_AUTO_MASK == OPTION_AUTO)
		
		spd = (options & OPTION_SPD_MASK)
		if spd == 0:
			self._glb_scroll = 1.0
		elif spd == OPTION_SPD_2x:
			self._glb_scroll = 2.0
		elif spd == OPTION_SPD_3x:
			self._glb_scroll = 3.0
		elif spd == OPTION_SPD_4x:
			self._glb_scroll = 4.0
		
		self._onp_rand = (options & OPTION_ONP_MASK)
		if self._onp_rand == OPTION_ONP_MIRROR:
			self._onp_rand_func = onp_rand_mirror
		elif self._onp_rand == OPTION_ONP_RANDOM:
			self._onp_rand_func = onp_rand_random
		elif self._onp_rand == OPTION_ONP_SRANDOM:
			self._onp_rand_func = onp_rand_srandom
		else:
			self._onp_rand_func = onp_rand_none
		
		# TODO:
		# apply options to fumen
		
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		self._state.offset += 1000.0 / 60.0
		self._onps = []
		
		if self._fumen.empty():
			return False
		
		self._fumen.update(self._state, self._onps)
		print "active onps: @off=%f" % self._state.offset
		for onp_cfg in self._onps:
			off, onp = onp_cfg[0], onp_cfg[1]
			print "\tonp %s @off=%f" % (onp, off)
		print
		
		return True
		
if __name__ == '__main__':
	import tja_reader
	import tja_fumen
	import sys

	reader = tja_reader.CReader()
	reader.set_file(sys.argv[1])
	
	fumen = tja_fumen.CFumen()
	fumen.read_header(reader)
	fumen.read_fumen(reader)

	onp_mgr = CMgr(fumen, options=0)
	while onp_mgr.update(None):
		pass