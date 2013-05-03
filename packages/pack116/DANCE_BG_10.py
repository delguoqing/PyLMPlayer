def func_0(this, _global):
	this.gotoAndPlay(0)
	
def func_1(this, _global):
	def onEnterFrame(_this, _global):
		_this._x -= 2
		if _this._x <= -480:
			_this._x = 0
	this.onEnterFrame = onEnterFrame
	
def func_2(this, _global):
	this.stop()

DATA = (
	func_0,
	func_1,
	func_2,
)