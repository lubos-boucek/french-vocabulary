class Dependent:
	""" Checks whether all requirements are present in injection """
	
	def __init__(self, injection, required):
		self.props = {}
		
		for req in required:
			try:
				# Double checking
				if injection[req] == None:
					raise KeyError
				self.props[req] = injection[req]
			except KeyError:
				# TODO: &>2, logging
				print("# Requirement " + req + " not props or None")
				raise