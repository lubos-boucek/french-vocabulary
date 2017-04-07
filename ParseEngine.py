from Dependent import Dependent
from bs4 import BeautifulSoup as bs
import unicodedata

LAROUSSE = "http://larousse.fr/dictionnaires/francais/"

class ParseEngine(Dependent):
	""" Receives and parses response """
	def __init__(self, injection):
		super().__init__(injection, ["page_retriever"])

		self.reset()

	def reset(self):
		self.result = { "definitions": [] }

	def parse(self, word):
		self.reset()
		self.result["searched"] = word

		url = LAROUSSE + word
		response = self.props["page_retriever"].retrieve(url)
		soup = bs(response["text"], "html.parser")

		# TODO: Get ID
		# print("url: ", response["url"])

		# Get actual displayed key
		h2 = soup.find("h2", { "class": "AdresseDefinition" })
		
		# ... not found
		if not h2:
			self.result["key"] = None
			return self.result

		self.result["key"] = h2.get_text().strip()

		# Get definitions
		lis = soup.find_all("li", { "class": "DivisionDefinition" })

		for li in lis:
			normalized = unicodedata.normalize("NFKD", li.get_text())
			self.result["definitions"].append(normalized)

		return self.result