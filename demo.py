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

class IntroSlide(ExecutionNode):
	def __init__(self,data):
		super().__init__(data)
	def __call__(self,game,*a,**k):
		game.screen.display.fill(self.color)


class IntroRootNode(ExecutionNode):
	current_slide = -1
	def __init__(self,data):
		self.field_mappings = {
			"timer":Timer,
			"loop_head":IntroSlide,
			"slides":IntroSlide
		}
		super().__init__(data)
		self.timer.duration = self.continue_response.nextnode.duration
	def is_finished(self):
		if self.timer.elapsed():
			self.timer.reset()
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
		self.field_mappings['rootnode'] = IntroRootNode
		super().__init__(data)

if __name__=="__main__":
	DemoGame({
		"rootnode":{
			"timer":{
				"duration":3000,
				"elapsed":0
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