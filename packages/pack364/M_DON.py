def func_0(this, _global):
	this._root.fscommand("callback", "combo_end")
	this.stop()

def func_1(this, _global):
	this.stop()	
	
def func_2(this, _global):
	this._root.fscommand("callback", "baloon_success_end")
	this.stop()
	
def func_3(this, _global):
	this._root.fscommand("callback", "miss1_end")
	this.stop()
	
def func_4(this, _global):
	this._root.fscommand("callback", "miss2_end")
	this.stop()

def func_5(this, _global):
	this.gotoAndPlay("miss_7")

def func_6(this, _global):
	this._root.fscommand("callback", "miss_normal_start_end")
	this.stop()	

def func_7(this, _global):	
	this._root.fscommand("callback", "norma_up_end")
	this.stop()
		
def func_8(this, _global):	
	this._root.fscommand("callback", "norma_down_end")
	this.stop()
	
def func_10(this, _global):	
	this._root.fscommand("callback", "full_gauge_start_end")
	this.stop()

def func_11(this, _global):	
	this._root.fscommand("callback", "sabi_end_end")
	this.stop()

def func_12(this, _global):	
	this._root.fscommand("callback", "full_sabi_end_end")
	this.stop()

def func_13(this, _global):	
	this._root.fscommand("callback", "full_sabi_start_end")
	this.stop()
					
def func_14(this, _global):	
	this._parent.gotoAndPlay("result_wait")

def func_15(this, _global):	
	this.gotoAndPlay("sabi_loop")
		
def func_16(this, _global):	
	this._root.fscommand("callback", "imo_in_end")
	this.stop()
		
def func_17(this, _global):	
	this._root.fscommand("callback", "imo_break_end")
	this.stop()
		
def func_18(this, _global):	
	this._root.fscommand("callback", "imo_miss_end")
	this.stop()

def func_19(this, _global):	
	this.gotoAndPlay("full_gage_idle")

def func_20(this, _global):	
	this.gotoAndPlay("full_sabi")	
	
	
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
)