import copy
import tja_note_section
import tja_header
import tja_enso_state

SECTION_NORMAL = 2
SECTION_EXPERT = 3
SECTION_MASTER = 4

class CFumen(object):
	
	def __init__(self):
		self.header = tja_header.CData()
		self.sections = []
		self._active_sections = []
		self.tot_combo = 0
		
	def read_header(self, reader):
		self.header.read(reader)
		self.header.refresh()
		
	def read_fumen(self, reader):
		curr_state = tja_enso_state.CEnsoState(self.header)
		next_state = None
		
		while not reader.check_command("#END"):
			cmd_name, args = reader.read_command()
			
			if cmd_name == "#BRANCHSTART":
				reader.skip_line()
				if next_state:
					curr_state, next_state = next_state, None
				curr_state.branch_bar = True
				self.sections.append([True, args, None, None, None])
				#print "======> BRANCHSTART"
			elif cmd_name in ("#N", "#E", "#M"):
				#print "<======> %s BEG" % cmd_name
				reader.skip_line()
				sec = tja_note_section.CNoteSection()
				next_state = copy.copy(curr_state)
				sec.read(reader, next_state)
				if cmd_name == "#N":
					self.sections[-1][SECTION_NORMAL] = sec
				elif cmd_name == "#E":
					self.sections[-1][SECTION_EXPERT] = sec
				elif cmd_name == "#M":
					self.sections[-1][SECTION_MASTER] = sec
				#print "<======> %s END" % cmd_name					
			elif cmd_name == "#BRANCHEND":
				#print "=====> BRANCHEND"
				reader.skip_line()
				if next_state:
					curr_state, next_state = next_state, None
			else:
				#print "=====> NO BUNKI BEG"
				section = tja_note_section.CNoteSection()
				self.sections.append([False, None, section, None, None])
				section.read(reader, curr_state)
				#print "=====> NO BUNKI END"
				
		self.tot_combo = curr_state.tot_combo
		#print "tot_combo = %d" % curr_state.tot_combo
			
	def update(self, state, onps):
		t = state.offset
		
		# check if new section will be activated
		activated_idx = 0
		for has_branch, cond, nfumen, efumen, mfumen in self.sections:
			active = (nfumen and nfumen.active(state)) \
				or (efumen and efumen.active(state)) \
				or (mfumen and mfumen.active(state))
			if not active:
				break
			activated_idx += 1
			
			if not has_branch:
				self._active_sections.append(nfumen)
			else:
				assert False, "Branch not supported yet!"
				
		if activated_idx > 0:
			self.sections = self.sections[activated_idx:]
			
		# execute command and render onps
		out_idx = 0
		for section in self._active_sections:
			if section.empty():
				out_idx += 1
			else:
				section.update(state, onps)
		if out_idx > 0:
			self._active_sections = self._active_sections[out_idx:]
		
		return t

	def empty(self):
		return len(self.sections) == 0 and len(self._active_sections) == 0
	
	def get_first_batch(self):
		for section in self.sections[0][2:]:
			if section is not None:
				return section.get_first_batch()
		return None
		
if __name__ == "__main__":
	import tja_reader
	import sys
	
	reader = tja_reader.CReader()
	reader.set_file(sys.argv[1])
	
	fumen = CFumen()
	fumen.read_header(reader)
	fumen.read_fumen(reader)