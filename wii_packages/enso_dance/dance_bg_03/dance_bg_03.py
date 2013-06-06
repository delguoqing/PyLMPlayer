def func_0(this, _global):
	def onEnterFrame(_this, _global):
		medetai = _this.scroll
		medetai._x -= 1.5
		if medetai._x <= -856:
			medetai._x = 0
	this.onEnterFrame = onEnterFrame

def func_1(this, _global):
	pass

def func_2(this, _global):
	def onEnterFrame(_this, _global):
		bg = _this.bg
		yakata = _this.yakata
		bg._x -= 0.1
		if bg._x <= -1131:
			bg._x = -107
		yakata._x = yakata._x + 0.5
		if yakata._x >= 791:
			yakata._x = -209
	this.onEnterFrame = onEnterFrame
	
def func_3(this, _global):
	this.stop()

DATA = (
	func_0,
	func_1,
	func_2,
	func_3,
)