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
		
		self.notes = []

	def log(self, str):
		print str
			
	def append_notes(self, notes, tot_notes, state):
		t_unit = (60000.0/state.bpm) * state.measure / tot_notes
		
		# Add Notes
		for idx, note in enumerate(notes):
			# Add Barline after the frist note
			if idx == 1 and state.bar_offset == 0:
				if state.branch_bar:
					self.notes.append((state.offset, "C", 0, self.speed))
					state.branch_bar = False
				else:
					self.notes.append((state.offset, "B", 0, self.speed))
				
				self.log("ONP B @off=%f" % state.offset)
				
			off = state.offset + t_unit * idx
			if note == "0" or note == ",":
				continue
			elif note == "5" or note == "6":	# Renda
				self.notes.append((off, note, 0, self.speed))
				state.long_note = note
				self.log("ONP %s @off=%f" % (note, off))
			elif note == "7" or note == "9":	# Balloon Renda or Imo Renda
				if state.long_note:
					continue
				hit_count = state.balloons.pop(0)
				self.notes.append((off, note, hit_count, self.speed))
				state.long_note = note
				self.log("ONP %s @off=%f, hitcount=%d" % (note, off, hit_count))
			elif note == "8":
				self.notes.append((off, state.long_note+"E", 0, self.speed))
				state.long_note = None
				self.log("ONP RENDA END")
			else:
				self.notes.append((off, note, 0, self.speed))
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
			self.in_off = (32 + 480 - 104) / self.speed
			self.out_off = (32 + 104 - 80) / self.speed
			
	def update(self, state, onps):
		
		# checking for new notes
		in_idx = 0
		out_idx = 0
		for note_cfg in self.notes:
			off, note = note_cfg[0], note_cfg[1]
			if state.offset - off > self.out_off:
				out_idx += 1
			elif off - state.offset > self.in_off:
				break
			in_idx += 1
			
			# append active onp to queue
			onps.append(note_cfg)
			
		# remove outdated onps
		if out_idx > 0:
			self.notes = self.notes[out_idx:]
		
	def __cmp__(self, o):
		return self.offset - self.in_off - (o.offset - o.in_off)
	
	def active(self, state):
		return (self.offset - state.offset) <= self.in_off
		
	# TODO: also check for commands
	def empty(self):
		return len(self.notes) == 0
		
		