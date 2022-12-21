from Dependent import Dependent

class ResultPresenter(Dependent):
	""" Manages presentation of parsed page """

	def __init__(self, injection):
		super().__init__(injection, ["data_loader"])

	def define(self, query):
		self.result = self.props["data_loader"].load(query)
		
		if not len(self.result["entities"]):
			# >&2, logging
			print("# No result has been returned for " + query + "!")
			return

		for entity in self.result["entities"]:
			print(entity["description"], "(" + entity["heading"] + ")")

			for definition in entity["definitions"]:
				print(":", definition)
			
			print()