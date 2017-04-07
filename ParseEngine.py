from Dependent import Dependent
from bs4 import BeautifulSoup as bs
import unicodedata, re

LAROUSSE_ROOT_URL = "http://larousse.fr/"
LAROUSSE_FRENCH_URL = "dictionnaires/francais/"
LAROUSSE_URL = LAROUSSE_ROOT_URL + LAROUSSE_FRENCH_URL

class ParseEngine(Dependent):
	""" Receives and parses response """

	def __init__(self, injection):
		super().__init__(injection, ["page_retriever"])

		self.reset()

	def reset(self):
		self.result = { "entities": [] }

	def processPartialUrl(self, url, entity):
		""" Extracts entity query and id from URL """

		if url.startswith("/" + LAROUSSE_FRENCH_URL):
			url = url[1 + len(LAROUSSE_FRENCH_URL):]
		else:
			# TODO? throw?
			return

		m = re.match("([^/]*)/([0-9]*)", url)

		entity["query"] = m.group(1)
		entity["id"] = m.group(2)

	def parseEntity(self, entity):
		""" Parses entity """

		url = LAROUSSE_URL + entity["query"] + "/" + entity["id"]
		response = self.props["page_retriever"].retrieve(url)
		
		soup = bs(response["text"], "html.parser")

		# Parse out heading
		h2 = soup.find("h2", { "class": "AdresseDefinition" })
		entity["heading"] = h2.get_text().strip()

		# Parse out definitions
		entity["definitions"] = []
		lis = soup.find_all("li", { "class": "DivisionDefinition" })

		for li in lis:
			normalized = unicodedata.normalize("NFKD", li.get_text())
			entity["definitions"].append(normalized)

	def parseArticle(self, article):
		entity = {}
		self.processPartialUrl(article.a.get("href"), entity)
		entity["description"] = article.h3.a.get_text().strip()
		self.result["entities"].append(entity)

	def parse(self, word):
		self.reset()

		url = LAROUSSE_URL + word
		self.result["searched"] = word

		response = self.props["page_retriever"].retrieve(url)
		soup = bs(response["text"], "html.parser")

		# Get all entities
		div = soup.find("div", { "class": "wrapper-search" })
		
		# TODO? throw?
		# No results
		if not div:
			return self.result

		articles = div.find_all("article")
		for article in articles:
			self.parseArticle(article)

		# Filter out duplicates
		# TODO? Simplify?
		self.result["entities"] = \
			[entity for i, entity in enumerate(self.result["entities"]) \
			if i == [x["id"] for x in

		for entity in self.result["entities"]:
			self.parseEntity(entity)

		return self.result