def func0(this, _global):
	this.stop()

def func1(this, _global):
	this.gotoAndPlay("loop")		

# script error
def func2(this, _global):
	pass
	
DATA = (func0, func1, func2)