import pygame
from overworld import GameSave
from json import load

try:
	pygame.display.init()
	tileupdate = pygame.time.Clock()
	framerate = 24
	elapsed = 0
	step_frequency = 1500
	with open("testsave.json") as f:
		r=GameSave(load(f))
		resolution=r.location.actual_size()
		window=pygame.display.set_mode(resolution)
		running=True
		while running:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					running = False
			r.location.render(window)
			pygame.display.update()
			elapsed += tileupdate.tick()
			while elapsed>=step_frequency:
				elapsed-=step_frequency
				r.location.tileset.progress_frame()
except:
	raise
finally:
	pygame.quit()
