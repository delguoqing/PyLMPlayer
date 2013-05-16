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
	
	ONP_DON = 0
	ONP_KATSU = 1
	ONP_DON_DAI = 2
	ONP_KATSU_DAI = 3
	ONP_RENDA1 = 4
	ONP_RENDA2 = 5
	ONP_RENDA3 = 6
	ONP_RENDA_DAI1 = 7
	ONP_RENDA_DAI2 = 8
	ONP_RENDA_DAI3 = 9
	ONP_GEKI = 10
	ONP_IMO = 11
	ONP_SYOUSETSU = 12
	ONP_SYOUSETSU_BUNKI = 13
	
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
		
	def set_onp_lumens(self, lumens):
		self._onp_lumens = lumens
	
		self._onp_lumens[self.ONP_SYOUSETSU].gotoAndPlay("normal")
		self._onp_lumens[self.ONP_SYOUSETSU_BUNKI].gotoAndPlay("bunki")
		
	def log_onps(self, onps):
		print "active onps:"
		for off, onp, hits, spd in onps:
			print "\t%s @off=%f, spd=%f" % (onp, off, spd)
		print
		
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
		
		# update onp lumens without drawing
		for lumen in self._onp_lumens:
			lumen.update(render_state, operation & lm_consts.MASK_NO_DRAW)
		
		self._fumen.update(self._state, self._onps)
		
		#self.log_onps(self._onps)
		
		# draw from back to front
		end_note = None
		for off, onp, hits, spd in reversed(self._onps):
			x = self._onp_hit_x + (off - self._state.offset) * spd
			if onp == "1":
				lumen = self._onp_lumens[self.ONP_DON]
				lumen.matrix.translate = (x, self._onp_y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp == "2":
				lumen = self._onp_lumens[self.ONP_KATSU]
				lumen.matrix.translate = (x, self._onp_y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp == "3":
				lumen = self._onp_lumens[self.ONP_DON_DAI]
				lumen.matrix.translate = (x, self._onp_y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp == "4":
				lumen = self._onp_lumens[self.ONP_KATSU_DAI]
				lumen.matrix.translate = (x, self._onp_y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp == "B" and self._state.barline_on:
				lumen = self._onp_lumens[self.ONP_SYOUSETSU]
				lumen.matrix.translate = (x, self._onp_y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp == "C":
				lumen = self._onp_lumens[self.ONP_SYOUSETSU_BUNKI]
				lumen.matrix.translate = (x, self._onp_y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp.endswith("E"):
				end_note = (off, onp, hits, spd)
			elif onp == "5":
				if end_note is None:
					end_x = 480
				else:
					end_x = self._onp_hit_x + (end_note[0] - self._state.offset) * end_note[3]
				self.draw_renda(render_state, operation, self.ONP_RENDA1, self.ONP_RENDA2, self.ONP_RENDA3,
								x, end_x)
				end_note = None
				
			elif onp == "6":
				if end_note is None:
					end_x = 480
				else:
					end_x = self._onp_hit_x + (end_note[0] - self._state.offset) * end_note[3]
				self.draw_renda(render_state, operation, self.ONP_RENDA_DAI1, self.ONP_RENDA_DAI2,
								self.ONP_RENDA_DAI3, x, end_x)
				end_note = None
				
			elif onp == "7":
				if end_note is None:
					end_x = 480
				else:
					end_x = self._onp_hit_x + (end_note[0] - self._state.offset) * end_note[3]
				self.draw_geki_or_imo(render_state, operation, self.ONP_GEKI, x, end_x)
				end_note = None
				
			elif onp == "9":
				if end_note is None:
					end_x = 480
				else:
					end_x = self._onp_hit_x + (end_note[0] - self._state.offset) * end_note[3]
				self.draw_geki_or_imo(render_state, operation, self.ONP_IMO, x, end_x)
				end_note = None
				
		if end_note:
			off, onp, hits, spd = end_note
			x = 0
			end_x = end_x = self._onp_hit_x + (off - self._state.offset) * spd
			if onp == "5E":
				self.draw_renda(render_state, operation, self.ONP_RENDA1, self.ONP_RENDA2, self.ONP_RENDA3, x, end_x)
			elif onp == "6E":
				self.draw_renda(render_state, operation, self.ONP_RENDA_DAI1, self.ONP_RENDA_DAI2, self.ONP_RENDA_DAI3, x, end_x)
			elif onp == "7E":
				self.draw_geki_or_imo(render_state, operation, self.ONP_GEKI, x, end_x)
			elif onp == "9E":
				self.draw_geki_or_imo(render_state, operation, self.ONP_IMO, x, end_x)
			else:
				assert False, "Invalid end note %s" % onp
			end_note = None
				
	def draw_geki_or_imo(self, render_state, operation, index, x, end_x):
		lumen = self._onp_lumens[index]
		if x > self._onp_hit_x:
			lumen.matrix.translate = (x, self._onp_y)
		elif end_x > self._onp_hit_x:
			lumen.matrix.translate = (self._onp_hit_x, self._onp_y)
		else:
			lumen.matrix.translate = (end_x, self._onp_y)
		lumen.update(render_state, operation & lm_consts.MASK_DRAW)
		
	def draw_renda(self, render_state, operation, head, body, tail, x, end_x):
		body_len = end_x - x
		
		lumen_body = self._onp_lumens[body]
		lumen_body.matrix.translate = ((x + end_x) * 0.5, self._onp_y)
		lumen_body.matrix.scale = (body_len / 32.0 ,1.0)
		lumen_body.renda.gotoAndStop("yellow")
		lumen_body.update(render_state, operation & lm_consts.MASK_DRAW)
		
		lumen_head = self._onp_lumens[head]
		lumen_head.matrix.translate = (x, self._onp_y)
		lumen_head.update(render_state, operation & lm_consts.MASK_DRAW)
		
		lumen_tail = self._onp_lumens[tail]
		lumen_tail.renda.gotoAndStop("yellow")
		lumen_tail.matrix.translate = (end_x, self._onp_y)
		lumen_tail.update(render_state, operation & lm_consts.MASK_DRAW)
	
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