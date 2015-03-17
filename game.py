from jsonconstruct import *
import pygame

class Introduction(JSONSTructure):
	def __init__(self,data):
		JSONSTructure.__init__(self,data)

class Game(Application):
	def __init__(self,data):
		Application.__init__(self,data)
	def __call__(self):
		pygame.display.init()
		frame_limiter = pygame.time.Clock()
		running = True
		window = pygame.display.set_mode(self.resolution)
		try:
			while running:
				for evnt in pygame.event.get():
					if evnt.type==pygame.QUIT:
						running = False
				frame_limiter.tick(self.framerate)
				pygame.display.flip()
		except:
			raise
		finally:
			pygame.quit()
