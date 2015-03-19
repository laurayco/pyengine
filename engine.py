from jsonconstruct import *
import pygame

def consume(i):
	for x in i:
		pass

class ExecutionNode(JSONStructure):
	def __init__(self,data):
		super().__init__(data)
	def __call__(self,game,*a,**k):
		return NodeResponse()

class NodeResponse(JSONStructure):
	nextnode = None
	def __init__(self,data):
		super().__init__(data)

class Screen(JSONStructure):
	def __init__(self,data):
		super().__init__(data)
		self.display = pygame.display.set_mode(self.resolution)
	def draw(self,source,location,sl=None):
		self.display.blit(source,location,sl)
	def update(self):
		pygame.display.flip()

class Timer(JSONStructure):
	def __init__(self,data):
		super().__init__(data)
		self.clock = pygame.time.Clock()
	def elapsed(self):
		self.tally += self.clock.tick()
		if tally>=self.duration:
			self.tally = 0
			return True
		return False

class GameApplication(Application):
	running = True
	def __init__(self,data):
		self.field_mappings['screen'] = Screen
		super().__init__(data)
	def __call__(self):
		def do_frame(node):
			self.events_dispatch()
			if not(result.nextnode and self.running):
				return None
			return result.nextnode
		node = self.root_node
		while node is not None:
			node = do_frame(node)
	def events_dispatch(self):
		def dispatch(evnt):
			if evnt.type==pygame.QUIT:
				self.running=False
			# send events to subscribers
		consume(map(dispatch,(pygame.events.get())))