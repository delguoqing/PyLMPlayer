def func_0(this, fscommand):
	def onEnterFrame(_this):
		bg = _this.bg
		bg._x -= 0.5
		if bg._x <= -270:
			bg._x = 0
	this.onEnterFrame = onEnterFrame

def func_1(this, fscommand):
	this.stop()
	
def func_2(this, fscommand):
	pass

DATA = (
	func_0,
	func_1,
	func_2,
)