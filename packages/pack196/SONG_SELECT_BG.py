def func_0(this, _global):
	this.stop()

def func_1(this, _global):
	def onEnterFrame(_this, _global):
		bg = _this.mc_bg_000
		bg._x -= 0.4
		if bg._x <= -192:
			bg._x = 0
	this.onEnterFrame = onEnterFrame
	
DATA = (
	func_0,
	func_1,
)