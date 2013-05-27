import sys
sys.path.append("..")

import random
import tja_enso_state

from lm import lm_consts
from tja_consts import *

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
	
	def __init__(self, fumen, scn, options=0):
		self._glb_scroll = 1.0
		
		self._auto = False
		self._auto_hit_left = True
		self._auto_last_hit = -1
		
		self._onp_rand = 0
		self._onp_rand_func = onp_rand_none
		self._fumen = fumen
		self._state = tja_enso_state.CEnsoState(self._fumen.header)
		self._onps = []
		self._onp_y = 107
		self._onp_hit_x = 104
		
		self._judge_ryo = 50 * 0.5
		self._judge_ka = 150 * 0.5
		self._judge_fuka = 217 * 0.5
		
		self._keys = 0
		self._scn = scn
		self.active = True
		
		self.set_option(options)
		first_batch = self._fumen.get_first_batch()
		if first_batch:
			self._state.offset -= first_batch.in_off
		
	def set_onp_lumens(self, lumens):
		self._onp_lumens = lumens
		
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
	
	def add_key(self, key):
		self._keys |= key
	
	def _get_hitjudge(self, onp_off, hit_off):
		off_delta = abs(onp_off - hit_off)
		if off_delta <= self._judge_ryo:
			return HITJUDGE_RYO
		elif off_delta <= self._judge_ka:
			return HITJUDGE_KA
		else:
			return HITJUDGE_FUKA
		return HITJUDGE_NO
	
	def _gen_auto_play(self):
		if self._state.hit_onp is None:
			return 0
		if random.random() > 1:
			return 0
		off, onp, hits, spd = self._state.hit_onp
		if ONP_SHORT[0] <= onp <= ONP_SHORT[1] and off - self._state.offset > self._judge_ryo / 3.0:
			return 0
		if onp == ONP_RENDA1 or onp == ONP_RENDA_DAI1:
			self._auto_last_hit = (self._auto_last_hit + 1) % 5
			if self._auto_last_hit != 0: return 0
		elif onp == ONP_GEKI or onp == ONP_IMO:
			self._auto_last_hit = (self._auto_last_hit + 1) % 2
			if self._auto_last_hit != 0: return 0			
		else:
			self._auto_last_hit = -1
			
		valid_keys, big_keys, _, _, _ = ONP_CFG[onp]
		if big_keys != HIT_INVALID:
			keys = big_keys
			self._auto_hit_left = True
		else:
			keys = valid_keys & (self._auto_hit_left and HIT_MASK_LEFT or HIT_MASK_RIGHT)
			self._auto_hit_left = not self._auto_hit_left
		return keys
			
	def judge(self):
		if self._auto:
			self._keys = self._gen_auto_play()
			
		hit_ok = hit_big = hitaway = False
		onp = ONP_NONE
		hit_judge = None
		# judge
		if self._state.hit_onp:
			off, onp, hits, spd = self._state.hit_onp
			valid_keys, big_keys, onp_flys, delay_judge, fly_on_break = ONP_CFG[onp]
			if self._keys > 0 or (delay_judge > 0 and self._state.hit_onp_start):
				self._state.hit_onp_keys |= self._keys	# combine keys
				hit_ok = bool(self._state.hit_onp_keys & valid_keys)
				hit_big = bool((self._state.hit_onp_keys & big_keys) == big_keys)
				self._state.hit_onp_hits += int(hit_ok)
				hitaway = self._state.hit_onp_hits >= hits \
					and (hit_big or delay_judge == 0 or self._state.hit_onp_start)
				#print hit_big, delay_judge, self._state.hit_onp_start
				if hit_ok:
					self._state.hit_onp_start = True
				if hitaway:
					self._state.hitaway_off = off
			hit_keys = self._state.hit_onp_keys & valid_keys
			if not delay_judge:
				self._state.hit_onp_keys = 0
			if not hit_ok:
				hit_judge = HITJUDGE_NO
			elif ONP_LONG[0] <= onp <= ONP_LONG[1]:
				hit_judge = HITJUDGE_HIT
			else:
				hit_judge = self._get_hitjudge(off, self._state.offset)
				if hit_big and hit_judge != HITJUDGE_FUKA:
					hit_judge |= HITJUDGE_DAI
					
			# special case for ONP_GEKI and ONP_IMO
			if onp == ONP_GEKI and hit_ok:
				if self._state.hit_onp_hits == 1:
					self._scn.set_max_balloon(hits)
				self._scn.set_balloon(hits - self._state.hit_onp_hits)
			elif onp == ONP_IMO and hit_ok:
				self._scn.set_imo(hits - self._state.hit_onp_hits,
					self._state.offset <= self._state.imo_break_high_time)
				
			# Add combo
			if hitaway and ONP_SHORT[0] <= onp <= ONP_SHORT[1]:
				if hit_judge == HITJUDGE_RYO:
					self._state.combo += 1
					self._state.ryo += 1
					self._state.tamashii = min(self._state.tamashii + 1, self._state.tot_tamashii)
				elif hit_judge == HITJUDGE_KA:
					self._state.combo += 1
					self._state.ka += 1
					self._state.tamashii = min(self._state.tamashii + 0.5, self._state.tot_tamashii)
				elif hit_judge == HITJUDGE_RYO_DAI:
					self._state.combo += 1
					self._state.ryo += 1
					self._state.tamashii = min(self._state.tamashii + 1, self._state.tot_tamashii)
				elif hit_judge == HITJUDGE_KA_DAI:
					self._state.combo += 1
					self._state.ka += 1
					self._state.tamashii = min(self._state.tamashii + 0.5, self._state.tot_tamashii)
				elif hit_judge == HITJUDGE_FUKA:
					self._state.combo = 0
					self._state.fuka += 1
					self._state.tamashii = max(self._state.tamashii - 2, 0)
					
				self._scn.set_combo(self._state.combo)
				self._scn.set_tamashii(self._state.tamashii, self._state.tot_tamashii)
		else:
			hit_keys = self._keys
			hit_judge = HITJUDGE_NO
		
		
		self._state.is_hitaway = hitaway
			
		self._scn.on_hit(self._keys)
		self._scn.on_hit_judge(onp, hit_keys, hit_judge, hitaway)
		
		# special case for missing ONP_GEKI
		if onp == ONP_GEKI and self._state.hit_onp_hits != 0 and not hitaway and self._state.hit_onp_time < 1000.0 / 60:
			if not self._auto:
				self._scn.set_balloon_miss()
			else:
				self._scn.set_balloon(0)
			self._state.is_hitaway = True
			self._state.hitaway_off = off
		# special case for missing ONP_IMO
		elif onp == ONP_IMO and not hitaway and self._state.hit_onp_time < 1000.0 / 60.0:
			self._scn.set_imo_miss()
			self._state.is_hitaway
			self._state.hitaway_off = off
			
	def reset(self, scn):
		self._scn = scn
		
		self._scn.add_dancer()
		
		self._state.tamashii = 0
		self._state.tot_tamashii = self._fumen.tot_combo * 0.6
	
	def update(self, render_state, operation=lm_consts.MASK_ALL):
		if not self.active:
			return
		
		self._state.offset += 1000.0 / 60.0
		self._onps = []
		
		# update onp lumens without drawing
		for lumen in self._onp_lumens:
			lumen.update(render_state, operation & lm_consts.MASK_NO_DRAW)
		
		self._fumen.update(self._state, self._onps)
		#self.log_onps(self._onps)
		if self._state.gogotime_dirty:
			self._state.gogotime_dirty = False
			self._scn.set_gogotime(self._state.gogotime)
		
		# Remove hitawayed hit onp
		if self._state.is_hitaway:
			self._state.hit_onp_off += 1
			self._state.hit_onp = None
		
		# Old hit onp	
		hit_onp = self._state.hit_onp
		hit_onp_off = self._state.hit_onp_off
		
		# update current hit onp
		for off, onp, hits, spd in self._onps:
			if off < self._state.hit_onp_off:	# already missed, don't check
				continue
			if self._state.offset + self._judge_fuka < off:		# not ready for check yet
				break
			if ONP_SHORT[0] <= onp <= ONP_SHORT[1]:
				if self._state.offset - self._judge_fuka > off:	# fully missed
					self._state.hit_onp = None
					self._state.fuka += 1
					self._state.combo = 0
					self._state.tamashii = max(self._state.tamashii - 2, 0)
					self._scn.set_combo(self._state.combo)
					self._scn.set_tamashii(self._state.tamashii, self._state.tot_tamashii)
				else:
					self._state.hit_onp = (off, onp, hits, spd) # accept as new hit onp
					self._state.hit_onp_time = 0
					break
			elif onp == ONP_END:
				if self._state.offset > off:	# miss the whole long onp
					self._state.hit_onp = None
				else:	# the long onp still holds
					self._state.hit_onp_time = off - self._state.offset
					break
			elif ONP_LONG[0] <= onp <= ONP_LONG[1]:
				if self._state.offset >= off:	# accept as new hit onp, but continue find
					self._state.hit_onp = (off, onp, hits, spd)
					self._state.hit_onp_time = 999999
			elif onp == ONP_IMO_HIGH:
				self._state.imo_break_high_time = off
			
		if self._state.hit_onp:
			self._state.hit_onp_off = self._state.hit_onp[0]
		elif hit_onp is not None:
			self._state.hit_onp_off += 1
		
		if self._state.hit_onp_off != hit_onp_off: # clear hit count
			if self._state.hit_onp and self._state.hit_onp[1] == ONP_IMO:
				self._scn.set_max_imo(self._state.hit_onp[2])
				self._state.imo_break_high_time = 999999
			self._state.hit_onp_hits = 0
			self._state.hit_onp_keys = 0
			self._state.hit_onp_start = False
			
			
			#print "init hit status"
		
		self.judge()
		
		# clear keys	
		self._keys = 0
		
		# draw from back to front
		end_note = None
		for off, onp, hits, spd in reversed(self._onps):
			x = self._onp_hit_x + (off - self._state.offset) * spd
			end_x = 480
			if (ONP_SHORT[0] <= onp <= ONP_SHORT[1]) \
				or (ONP_SYOUSETSU[0] <= onp <= ONP_SYOUSETSU[1] and self._state.barline_on):
				lumen = self._onp_lumens[onp]
				lumen.matrix.translate = (x, self._onp_y)
				lumen.update(render_state, operation & lm_consts.MASK_DRAW)
			elif onp == ONP_END:
				end_note = (off, onp, hits, spd)
			elif ONP_LONG[0] <= onp <= ONP_LONG[1]:
				if end_note is not None:
					end_x = self._onp_hit_x + (end_note[0] - self._state.offset) * end_note[3]
					end_note = None
				if onp == ONP_RENDA1:
					self.draw_renda(render_state, operation,
						ONP_RENDA1, ONP_RENDA2, ONP_RENDA3, x, end_x)
				elif onp == ONP_RENDA_DAI1:
					self.draw_renda(render_state, operation,
						ONP_RENDA_DAI1, ONP_RENDA_DAI2, ONP_RENDA_DAI3, x, end_x)
				elif onp == ONP_GEKI and (off != self._state.hit_onp_off or self._state.hit_onp_hits == 0):
					self.draw_geki_or_imo(render_state, operation, ONP_GEKI, x, end_x)
				elif onp == ONP_IMO and (off > self._state.hit_onp_off):
					self.draw_geki_or_imo(render_state, operation, ONP_IMO, x, end_x)
	
		# judge full combo
		if self._fumen.empty() and self._state.fuka == 0:
			self._scn.play_fullcombo()
			self.active = False
			
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