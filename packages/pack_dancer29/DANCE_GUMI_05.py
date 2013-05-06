def func_1(this, _global):
	this._root.fscommand("callback", "in_end")
	this.stop()

def func_2(this, _global):
	this._root.fscommand("callback", "dance_sync")
	this._root.fscommand("callback", "in_start")
	
def func_4(this, _global):
	this.stop()

DATA = (
	func_1,
	func_2,
	func_4,
)