def func0(this, _global):
	this._parent.gotoAndPlay("dance")
	this._root.fscommand("callback", "on_dancer_in_end")
	
def func1(this, _global):
	this.stop()

DATA = (
	func0,
	func1,
)