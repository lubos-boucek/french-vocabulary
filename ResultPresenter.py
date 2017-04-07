from Dependent import Dependent

class ResultPresenter(Dependent):
	""" Manages presentation of parsed page """

	def __init__(self, injection):
		super().__init__(injection, ["parse_engine"])

	def define(self, word):
		self.result = self.props["parse_engine"].parse(word)

		if not len(self.result["entities"]):
			# >&2, logging
			print("# No result has been returned for " + word + "!")
			return

		for entity in self.result["entities"]:
			print(entity["description"], "(" + entity["heading"] + ")")

			for definition in entity["definitions"]:
				print(":", definition)
			
			print()