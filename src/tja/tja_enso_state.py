class CEnsoState(object):
	
	def __init__(self, header):
		self.bpm = header["BPM"]
		self.measure = 4
		self.scroll = 1.0
		self.gogotime = False
		self.barline_on = True
		self.level = "normal"
		self.offset = -header["OFFSET"] * 1000
		self.balloons = list(header["BALLOON"])
		
		self.long_note = None
		self.bar_offset = 0
		self.branch_bar = False	# is the next bar a start of new branch
		self.last_hitaway_left = -9999
		self.last_hitaway_right = -9999
		self.last_hitaway = False
		self.tohit_off = -9999
		