def func0(this, _global):
	this.gotoAndPlay("loop")
	
def func1(this, _global):
	this._root.fscommand("event", "end")
	this.stop()
	
DATA = (
	func0,
	func1,
)