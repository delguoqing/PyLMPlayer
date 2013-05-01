def func_0(this, _global):
	def onEnterFrame(_this, _global):
		medetai = _this.medetai
		medetai._x -= 1.5
		if medetai._x <= -480:
			medetai._x = 0
	this.onEnterFrame = onEnterFrame
	
def func_1(this, _global):
	this.stop()
	
DATA = (
	func_0,
	func_1,
)