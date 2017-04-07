from Dependent import Dependent

class ResultPresenter(Dependent):
	def __init__(self, injection):
		super().__init__(injection, ["parse_engine"])

	def define(self, word):
		self.result = self.props["parse_engine"].parse(word)

		# print(self.result)

		if not self.result["key"]:
			# >&2, logging
			print("No result has been returned!")
			return

		print(self.result["key"])

		for definition in self.result["definitions"]:
			print(":", definition)