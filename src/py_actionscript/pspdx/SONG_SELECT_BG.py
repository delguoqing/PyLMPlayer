def func_0(this):
	this.stop()

def func_1(this):
	def onEnterFrame(_this):
		bg = _this.mc_bg_000
		bg._x -= 0.4
		if bg._x <= -192:
			bg._x = 0
	this.onEnterFrame = onEnterFrame
	
DATA = (
	func_0,
	func_1,
)