def func_0(this):
	this.fscommand("callback", "combo_end")
	this.stop()

def func_1(this):
	this.stop()	
	
def func_2(this):
	this.fscommand("callback", "baloon_success_end")
	this.stop()
	
def func_3(this):
	this.fscommand("callback", "balloon_miss_end")
	this.stop()
	
def func_4(this):
	this.fscommand("callback", "miss1_end")
	this.stop()
	
def func_5(this):
#	this.don.gotoAndStop(4)
#	this is bug.
	pass
	
def func_6(this):
	this.fscommand("callback", "miss2_end")
	this.stop()
	
def func_7(this):	
	this.fscommand("callback", "miss_anim_end")	
	this.stop()
	
def func_8(this):
	this.fscommand("callback", "miss_normal_start_end")
	this.stop()	

def func_9(this):	
	this.fscommand("callback", "norma_up_end")
	this.stop()
		
def func_10(this):	
	this.fscommand("callback", "norma_down_end")
	this.stop()
	
def func_11(this):
	this.fscommand("callback", "normal_down_end")
	this.stop()
		
def func_12(this):	
	this.fscommand("callback", "full_gauge_start_end")
	this.stop()
		
def func_13(this):	
	this.fscommand("callback", "imo_in_end")
	this.stop()
		
def func_14(this):	
	this.fscommand("callback", "imo_break_end")
	this.stop()
		
def func_15(this):	
	this.fscommand("callback", "imo_miss_end")
	this.stop()
		
def func_16(this):	
	this.fscommand("event", "end")
	this.stop()
	
def func_17(this):	
	this.fscommand("callback", "mode_in_end")
	this.fscommand("event", "end")
	this.stop()
	
def func_18(this):
	this.fscommand("callback", "cos_change")
	pass

def func_19(this):	
	this.fscommand("callback", "music_select_in_end")
	this.stop()

def func_20(this):	
	this.fscommand("callback", "music_select_out_end")
	this.fscommand("event", "end")	
	this.stop()	
	
def func_21(this):
	this.fscommand("sound", "don_step")
	pass
	
def func_22(this):
	this.fscommand("sound", "don_step")
	this.fscommand("event", "end")
	this.stop()	
	
def func_23(this):	
	this.gotoAndPlay("idling_0")

def func_24(this):
	this.gotoAndPlay("idling_4")	
	
def func_25(this):	
	this.gotoAndPlay(0)

def func_26(this):		
	this.fscommand("sound", "don_hand")
	pass
	
	
DATA = (
	func_0,
	func_1,
	func_2,
	func_3,	
	func_4,
	func_5,
	func_6,
	func_7,
	func_8,
	func_9,
	func_10,
	func_11,
	func_12,
	func_13,
	func_14,
	func_15,
	func_16,
	func_17,
	func_18,
	func_19,
	func_20,
	func_21,
	func_22,
	func_23,					
	func_24,	
	func_25,		
	func_26,
)