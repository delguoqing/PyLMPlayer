def func_0(this):
	def onEnterFrame(_this):
		bg = _this.bg
		bg._x -= 0.5
		if bg._x <= -270:
			bg._x = 0
	this.onEnterFrame = onEnterFrame

def func_1(this):
	this.stop()
	
def func_2(this):
	pass

DATA = (
	func_0,
	func_1,
	func_2,
)