# A batch of note scrolling at the same speed
class CNoteBatch(object):
	
	def __init__(self):
		self.offset = None
		self.bpm = None
		self.scroll = None
		self.speed = None
		
		self.commands = []
		
		self.notes = []
		
	def append_notes(self, notes, tot_notes, state):
		t_unit = (60000.0/state.bpm) * state.measure / tot_notes
		
		# Add Barline
		if state.bar_offset == 0:
			self.notes.append((state.offset, "B"))
			print "ONP B @off=%f" % state.offset
			
		# Add Notes
		for idx, note in enumerate(notes):
			off = state.offset + t_unit * idx
			if note == "0" or note == ",":
				continue
			elif note == "5":	# Renda
				self.notes.append((off, note))
				state.long_note = True
				print "ONP %s @off=%f" % (note, off)
			elif note == "7":	# Balloon Renda
				if state.long_note:
					continue
				hit_count = state.balloons.pop(0)
				self.notes.append((off, note, hit_count))
				state.long_note = True				
				print "ONP %s @off=%f, hitcount=%d" % (note, off, hit_count)
			elif note == "9":	# Imo Renda
				if not state.long_note:
					hit_count = state.balloons.pop(0)
					self.notes.append((off, note, hit_count))
					state.long_note = True
					print "ONP %s @off=%f, hitcount=%d" % (note, off, hit_count)
				else:	# A == imo break high/low point
					self.notes.append((off, "A"))
					print "ONP A @off=%f" % off
			elif note == "8":
				state.long_note = False
				print "ONP RENDA END"
			else:
				self.notes.append((off, note))
				print "ONP %s @off=%f" % (note, off)
		
	def read(self, reader, state):
		self.offset = state.offset
		self.bpm = state.bpm
		self.scroll = state.scroll
		
		while not reader.check_commands(("#END", "#BRANCHSTART", "#BRANCHEND", "#N", "#E", "#M",)) \
			and (not reader.check_commands(("#BPMCHANGE", "#SCROLL")) or len(self.notes) == 0):
		
			notes, tot_notes = reader.read_notes()
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
				print "#####"
				print "#####bpm:%f, beats:%f" % (self.bpm, state.measure)
				print "#####scroll:%f, off:%f" % (self.scroll, self.offset)
				print "#####"
				
			# handle notes
			if notes:
				if notes == ",": notes = "0,"
				print "NOTES off=%d:\t%s\tbar_off=%d" % (state.offset, notes, state.bar_offset)
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
				print "[ CMD ] ", cmd_name, args, "@off=%f" % state.offset
				self.commands.append((state.offset, cmd_name, args))
			else:
				print
			reader.skip_line()
			
			# note_dist = 26
			# time = time_per_beat * 0.25
			# speed = note_dist / time
			self.speed = 26 / (60000.0 * 0.25 / bpm)
			
		def update(self, state, onps):
			
			for note_cfg in self.notes:
				off, note = note_cfg[0], note_cfg[1]
				if (off - state.offset) * self.speed
				
			