import pygame
import jsonconstruct

class Tileset(jsonconstruct.JSONStructure):
	def __init__(self,data):
		jsonconstruct.JSONStructure.__init__(self,data)
		self.spritesheet = pygame.image.load(self.spritesheet)
		self.animation_frame = 0
		self.num_frames = self.spritesheet.get_width() // 16
	def progress_frame(self):
		self.animation_frame = (self.animation_frame + 1) % self.num_frames
	def draw_tile(self,target,position,tile):
		tslice = [self.animation_frame*16,tile*16, 16, 16]
		target.blit(self.spritesheet,position,tslice)

class Model(jsonconstruct.JSONStructure):
	def __init__(self,data):
		jsonconstruct.JSONStructure.__init__(self,data)

class Renderer(jsonconstruct.JSONStructure):
	field_mappings = {
		"tileset":Tileset
	}
	def __init__(self,mapdata):
		jsonconstruct.JSONStructure.__init__(self,mapdata)
		self.models = list(sorted(self.models,key=lambda m:m.layer))
		current_layers = []
		insertion_point = -1
		for model in self.models:
			if model.layer > insertion_point:
				for ii,layer in enumerate(current_layers):
					self.layers.insert(layer,ii)
				# create a new layer list
				current_layers = []
			else:
				for i,layer in enumerate(model.tile_layers):
					while i>=len(current_layers):
						current_layers.append([-1] * self.dimensions[0] * self.dimensions[1])
					tile = 0
					for y in range(model.position[1],model.position[1]+model.height):
						for x in range(model.position[0],model.position[0]+model.width):
							current_layers[i][(y*self.width)+x] = layer[tile]
	def actual_size(self):
		return (self.dimensions[0]*16,self.dimensions[1]*16)
	def render(self,target,position=None):
		xa,ya = (position or (0,0))
		actual_size = self.actual_size()
		for layer in self.layers:
			tile = 0
			for y in range(0,actual_size[1],16):
				for x in range(0,actual_size[0],16):
					t = layer[tile]
					if t>=0:
						self.tileset.draw_tile(target,(x+xa,y+ya),t)
					tile+=1

class GameSave:
	field_mappings = {
		"location":Renderer
	}
	def __init__(self,data):
		jsonconstruct.JSONStructure.__init__(self,data)