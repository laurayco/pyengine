import json

class JSONStructure:
	field_mappings = {}
	def __init__(self,data):
		mappings = self.field_mappings
		def load_data(k,v):
			if isinstance(v,list):
				return [load_data(k,i) for i in v]
			elif isinstance(v,str):
				with open(v) as f:
					return mappings[k](json.load(f))
			else:
				return mappings[k](v)
		for key in mappings.keys():
			try:
				data[key] = load_data(key,data[key])
			except KeyError:
				pass
		self.__dict__.update(data)

class Application(JSONStructure):
	def __init__(self,data,appname):
		JSONStructure.__init__(self,data)
		self.base_directory = "."
		self.appname = appname
	def __call__(self):
		pass
	def get_file(self,path):
		return os.path.join(self.base_directory,path)
	def media_directory(self):
		return self.get_file("media")
	def data_directory(self):
		return self.get_file("data")
	def user_directory(self):
		# this data comes from the user's home/.application directory.
		userdir = self.base_directory
		return self.get_file(userdir,self.appname)