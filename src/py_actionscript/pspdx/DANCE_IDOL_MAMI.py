def func_0(this, _global):
	this.fscommand("callback", "in_end")
	this.stop()

def func_1(this, _global):
	this.fscommand("callback", "dance_sync")
	this.fscommand("callback", "in_start")

def func_2(this, _global):
	this.fscommand("callback", "out_end")
	this.stop()
	
def func_3(this, _global):
	this.stop()

DATA = (
	func_0,
	func_1,
	func_2,
	func_3,
)