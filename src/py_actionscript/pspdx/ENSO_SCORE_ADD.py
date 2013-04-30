def func_0(this, fscommand):
	this.stop()

def func_1(this, fscommand):
	fscommand("event", "end")
	this.stop()	
	
DATA = (
	func_0,
	func_1,
)