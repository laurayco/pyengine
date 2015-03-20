from engine import *
from jsonconstruct import *

class LoopingNode(ExecutionNode):
	def __init__(self,data):
		super().__init__(data)
		self.continue_response = NodeResponse()
		self.continue_response.nextnode = self.loop_head
		self.final_response = NodeResponse
	def __call__(self,engine,*a,**k):
		if self.is_finished():
			return self.final_response
		return self.continue_response
	def is_finished(self):
		return True
	def connect(self,node):
		self.final_response.nextnode = node

class ScreenLoop(LoopingNode):
	def __init__(self,data):
		super().__init__(data)
		self.response = NodeResponse()
	def __call__(self,game,*a,**k):
		game.screen.update()
		return super().__call__(game,*a,**k)

class IntroSlide(ExecutionNode):
	def __init__(self,data):
		super().__init__(data)
		self.response = NodeResponse()
	def __call__(self,game,*a,**k):
		game.screen.display.fill(self.color)
		return self.response

class IntroRootNode(ScreenLoop):
	current_slide = -1
	def __init__(self,data):
		self.field_mappings = {
			"timer":Timer,
			"loop_head":IntroSlide,
			"slides":IntroSlide
		}
		super().__init__(data)
		self.loop_head.response.nextnode = self
		for slide in self.slides:
			slide.response.nextnode = self
		self.timer.duration = self.continue_response.nextnode.duration
	def is_finished(self):
		if self.timer.elapsed():
			return not self.progress()
		else:
			return False
	def progress(self):
		self.current_slide += 1
		if self.current_slide >= len(self.slides):
			return False
		self.continue_response.nextnode = self.slides[self.current_slide]
		self.timer.duration = self.continue_response.nextnode.duration
		return True

class DemoGame(GameApplication):
	def __init__(self,data):
		self.field_mappings['root_node'] = IntroRootNode
		super().__init__(data)

if __name__=="__main__":
	DemoGame({
		"root_node":{
			"timer":{
				"duration":3000
			},  "loop_head": {
				"color":(255,0,0),
				"duration":1000
			}, "slides": [
				{
					"color":(255,255,0),
					"duration":30000
				}
			]
		},
		"screen":{
			"resolution":(400,400)
		}
	})()