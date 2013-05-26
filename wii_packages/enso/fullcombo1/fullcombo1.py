def func0(this, _global):
	this.stop()

def func1(this, _global):
	this._root.fscommand("event", "end")
	
DATA = (
	func0,
	func1,
)