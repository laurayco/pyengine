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
			d = data[key]
			if isinstance(d,str):
				# filename
				with open(d) as f:
					d = json.load(f)
			data[key] = mappings[key](d)
		self.__dict__.update(data)
