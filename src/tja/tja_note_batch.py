import collections
from tja_consts import *

# A batch of note scrolling at the same speed
class CNoteBatch(object):
	
	def __init__(self):
		self.offset = None
		self.bpm = None
		self.scroll = None
		self.speed = None
		self.in_off = None
		self.out_off = None
		
		self.commands = []
		
		self.notes = collections.deque()

		self._active_notes = collections.deque()
		self._missed_notes = collections.deque()
		
	def log(self, str):
		return
		print str
		
	def trans_note(self, str):
		TABLE = {
			"1": ONP_DON,
			"2": ONP_KATSU,
			"3": ONP_DON_DAI,
			"4": ONP_KATSU_DAI,
			"5": ONP_RENDA1,
			"6": ONP_RENDA_DAI1,
			"7": ONP_GEKI,
			"8": ONP_END,
			"9": ONP_IMO,
			"A": ONP_IMO_HIGH,
			"B": ONP_SYOUSETSU_NORMAL,
			"C": ONP_SYOUSETSU_BUNKI,
		}
		return TABLE[str]
	
	def append_notes(self, notes, tot_notes, state):
		t_unit = (60000.0/state.bpm) * state.measure / tot_notes
		
		# Add Notes
		for idx, note in enumerate(notes):
			# Add Barline after the frist note
			if idx == 1 and state.bar_offset == 0:
				if state.branch_bar:
					self.notes.append((state.offset, self.trans_note("C"), 0, self.speed))
					state.branch_bar = False
				else:
					self.notes.append((state.offset, self.trans_note("B"), 0, self.speed))
				
				self.log("ONP B @off=%f" % state.offset)
				
			off = state.offset + t_unit * idx
			if note == "0" or note == ",":
				continue
			elif note == "5" or note == "6":	# Renda
				self.long_note = True
				self.notes.append((off, self.trans_note(note), 999999, self.speed))
				self.log("ONP %s @off=%f" % (note, off))
			elif note == "7" or note == "9":	# Balloon Renda or Imo Renda
				if state.long_note:
					if note == "9":
						self.notes.append((off, self.trans_note("A"), 0, self.speed))
					continue
				hit_count = state.balloons.pop(0)
				self.notes.append((off, self.trans_note(note), hit_count, self.speed))
				state.long_note = True
				self.log("ONP %s @off=%f, hitcount=%d" % (note, off, hit_count))
			elif note == "8":
				self.notes.append((off, self.trans_note(note), 0, self.speed))
				state.long_note = False
				self.log("ONP RENDA END")
			else:
				self.notes.append((off, self.trans_note(note), 1, self.speed))
				state.tot_combo += 1
				self.log("ONP %s @off=%f" % (note, off))
		
	def read(self, reader, state):
		self.offset = state.offset
		self.bpm = state.bpm
		self.scroll = state.scroll
		
		while not reader.check_commands(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M",)) \
			and (not reader.check_commands(("#BPMCHANGE", "#SCROLL")) or len(self.notes) == 0):
		
			notes, tot_notes = reader.read_notes()
			if notes == ",":
				notes = "0,"
				tot_notes = 1
			cmd_name, args = reader.read_command()

			# handle commands
			if cmd_name == "#DELAY":
				state.offset += float(args[0])
				if len(self.notes) == 0:
					self.offset = state.offset
			elif cmd_name == "#BPMCHANGE":
				if len(self.notes) == 0:
					self.bpm = state.bpm = float(args[0])
				elif state.bpm != float(args[0]):
					break
			elif cmd_name == "#SCROLL":
				if len(self.notes) == 0:
					self.scroll = state.scroll = float(args[0])
				elif state.scroll != float(args[0]):
					break
			elif cmd_name == "#MEASURE":
				a, b = args[0].split("/", 1)
				a = float(a.strip())
				b = float(b.strip())
				state.measure = 4 * a / b
					
			if len(self.notes) == 0 and notes:
				self.log("#####")
				self.log("#####bpm:%f, beats:%f" % (self.bpm, state.measure))
				self.log("#####scroll:%f, off:%f" % (self.scroll, self.offset))
				self.log("#####")
				
			# handle notes
			if notes:
				self.log("NOTES off=%d:\t%s\tbar_off=%d" % (state.offset, notes, state.bar_offset))
				num_notes = len(notes) - int(notes.endswith(","))
				tot_notes += state.bar_offset
				# set time for notes
				self.append_notes(notes, tot_notes, state)
				# offset advance
				delta = (60000.0/state.bpm) * state.measure * num_notes / tot_notes
				state.offset += (60000.0/state.bpm) * state.measure * num_notes / tot_notes
				# record incomplete bar
				if not notes.endswith(","):
					state.bar_offset += len(self.notes[-1])
				else:
					state.bar_offset = 0
			elif cmd_name:	# Runtime commands
				self.log("[ CMD ] %s %r @off=%f" % (cmd_name, args, state.offset))
				self.commands.append((state.offset, cmd_name, args))
			else:
				self.log("")
			reader.skip_line()
			
			# note_dist = 26
			# time = time_per_beat * 0.25
			# speed = note_dist / time
			self.speed = self.scroll * 26 / (60000.0 * 0.25 / self.bpm)
			
			# 104: hit pos x
			# 480: screen border x
			# 32: padding
			# 80: taiko right border(disappear pos)
			self.in_off = (32 + 480 - 104) / self.speed
			self.out_off = (32 + 104 - 80) / self.speed
			
	def update(self, state, onps):
			
		# executing command
		out_idx = 0
		for off, cmd_name, args in self.commands:
			if state.offset >= off:
				state.execute_command(cmd_name, args)
				out_idx += 1
			else:
				break
		if out_idx > 0:
			self.commands = self.commands[out_idx:]
		
		# Checking for new notes
		out_idx = 0
		for off, note, hits, spd in self.notes:
			if off - state.offset > self.in_off:
				break
			out_idx += 1
		for _ in xrange(out_idx):
			self._active_notes.append(self.notes.popleft())
		
		# Removing missed or hit away notes
		out_idx = 0
		for off, note, hits, spd in self._active_notes:
			if hits > 0 and off > state.hit_onp_off:
				#print "off = %f, behind the hit onp %f, no need to check" % (off, state.hit_onp_off)
				break
			if hits == 0 or off < state.hitaway_off:
				self._missed_notes.append((off, note, hits, spd))
				#print "add missed note %s off = %f / %f" % (note, off, state.hitaway_off)
			elif not state.is_hitaway:
				break

			out_idx += 1
		for _ in xrange(out_idx):
			self._active_notes.popleft()
		
		# Removing outdated notes
		out_idx = 0
		delay_removing = False
		for idx, (off, note, hits, spd) in enumerate(self._missed_notes):
			if state.offset - off > self.out_off:
				if ONP_LONG[0] <= note <= ONP_LONG[1]:
					delay_removing = True
				elif note == ONP_END:
					delay_removing = False
					out_idx = idx + 1
				elif not delay_removing:
					out_idx = idx + 1
			else:
				break
		for _ in xrange(out_idx):
			self._missed_notes.popleft()
			
		# appending missed and active notes
		onps.extend(self._missed_notes)
		onps.extend(self._active_notes)
									
	def __cmp__(self, o):
		return self.offset - self.in_off - (o.offset - o.in_off)
	
	def active(self, state):
		return (self.offset - state.offset) <= self.in_off
		
	# TODO: also check for commands
	def empty(self):
		return len(self.notes) == 0 and  len(self._active_notes) == 0 and len(self._missed_notes) == 0
	