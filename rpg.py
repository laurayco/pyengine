from engine import *
from jsonconstruct import *
from overworld import *

class RpgGame(GameApplication):
	def __init__(self,data):
		super().__init__(data,"rpg")
		self.loaded_save = None
	def load_save(self,save):
		self.load_save = save
		self.start_playing()