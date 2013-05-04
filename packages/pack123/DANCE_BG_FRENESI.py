def func_0(this, _global):
	def onEnterFrame(_this, _global):
		candy01 = _this.candy01
		candy02 = _this.candy02
		candy03 = _this.candy03
		candy04 = _this.candy04
		
		candy01._x = candy01._x - 0.5
		candy01._rotation = candy01._rotation + 0.5
		if candy01._x <= -290:		 
			candy01._x = candy01._x + 600
			
		candy02._x = candy02._x - 0.5
		candy02._rotation = candy02._rotation + 1.5
		if candy02._x <= -290:		 
			candy02._x = candy02._x + 600
			
		candy03._x = candy03._x - 0.5
		candy03._rotation = candy03._rotation + 2
		if candy03._x <= -290:		 
			candy03._x = candy03._x + 600
			
		candy04._x = candy04._x - 0.5
		candy04._rotation = candy04._rotation + 2.5
		if candy04._x <= -290:
			candy04._x = candy04._x + 600
			
	this.onEnterFrame = onEnterFrame
	
def func_1(this, _global):
	this.stop()

DATA = (
	func_0,
	func_1
)