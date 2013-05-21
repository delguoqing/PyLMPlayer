class CEnsoState(object):
	
	def __init__(self, header):
		###########################
		# Variables shared in Preprocess and Runtime
		###########################
		self.bpm = header["BPM"]
		self.measure = 4
		self.scroll = 1.0
		self.gogotime = False
		self.barline_on = True
		self.level = "normal"
		self.offset = -header["OFFSET"] * 1000
		
		###########################
		# Runtime variable
		###########################
		self.is_hitaway = False
		self.hitaway_off = -9999.0
		self.hit_onp_off = -9999.0
		self.hit_onp = None
		self.hit_onp_keys = 0
		self.hit_onp_hits = 0
		self.hit_onp_start = False
		self.hit_onp_time = 0
		self.imo_break_high_time = 999999
		
		###########################
		# Preprocessing variable
		###########################
		self.bar_offset = 0
		self.long_note = None
		self.branch_bar = False	# is the next bar a start of new branch
		self.balloons = list(header["BALLOON"])
		self.tot_combo = 0
		
		###########################
		# Statistic Variable
		###########################
		self.combo = 0
		self.renda = 0
		self.ryo = 0
		self.ka = 0
		self.fuka = 0	# include miss
		self.tamashii = -1
		self.score = 0
		