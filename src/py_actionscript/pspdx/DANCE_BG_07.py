def func_0(this, fscommand):
	def onEnterFrame(_this):
		if _this.kame._x <= -280:
			this.kame._x = 474
		else:
			this.kame._x -= 2
	this.onEnterFrame = onEnterFrame
	
def func_1(this, fscommand):
	def onEnterFrame(_this):
		_this._x -= 0.5
		if _this._x <= -480:
			_this._x = 0
	this.onEnterFrame = onEnterFrame
	
def func_2(this, fscommand):
	this.stop()
	
DATA = (
	func_0,
	func_1,
	func_2,
)