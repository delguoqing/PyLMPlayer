def func_0(this):
	this.stop()
	
def func_1(this):
	this.fscommand("callback", "in_end")
	this.stop()

def func_2(this):
	this.fscommand("callback", "dance_sync")
	this.fscommand("callback", "in_start")

def func_3(this):
	this.fscommand("callback", "out_end")
	this.stop()
	
def func_4(this):
	this.stop()

DATA = (
	func_0,
	func_1,
	func_2,
	func_3,
	func_4,
)