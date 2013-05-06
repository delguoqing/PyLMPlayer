def func_1(this, _global):
	this.stop()

def func_2(this, _global):
	this.gotoAndPlay("fever")
	
def func_4(this, _global):
	this.gotoAndStop(0)

DATA = (
	func_1,
	func_2,
	func_4,
)