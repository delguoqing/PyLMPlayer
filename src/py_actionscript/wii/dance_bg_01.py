def func_0(this, _global):
	def onEnterFrame(_this, _global):
		bg = _this.bg
		bg._x -= 0.5
		if bg._x <= -360:
			bg._x = 0
	this.onEnterFrame = onEnterFrame

def func_1(this, _global):
	this.stop()
	
def func_2(this, _global):
	pass

DATA = (
	func_0,
	func_1,
	func_2,
)