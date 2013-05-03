def func_0(this, _global):
	this.gotoAndPlay("loop")
	
def func_1(this, _global):
	this._root.fscommand("event", "end")
	this.stop()

def func_2(this, _global):
	this.stop()

DATA = (
	func_0,
	func_1,
	func_2,
)