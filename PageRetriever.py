from Dependent import Dependent
import os, pathlib, requests, json, hashlib, urllib.request as urlreq

# TODO: Check if directory ends with '/'
# TODO: Remove files on start if older than optional value
# TODO: debug level
class PageRetriever(Dependent):
	""" Manages retrieving of web pages, and cache """
	
	def __init__(self, injection):
		super().__init__(injection, ["retrieved_directory"])

		self.assertDirectoryExists()

	def assertDirectoryExists(self):
		try:
			os.makedirs(self.props["retrieved_directory"])
		except FileExistsError:
			# print("# Directory exists, continuing ...")
			pass

	def	loadFromFile(self, path):
		return json.loads(pathlib.Path(path).read_text())

	def dumpIntoFile(self, path, content):
		# TODO: try
		with open(path, 'w') as file:
			file.write(json.dumps(content))

	# TODO: Return content of file
	# TODO: History insted of hash cache
	def retrieve(self, url):
		# TODO? try?
		digest = hashlib.sha256(url.encode('utf-8')).hexdigest()
		path = self.props["retrieved_directory"] + digest

		if os.path.isfile(path):
			print("# Reusing cached file ...")
			return self.loadFromFile(path)

		# TODO: try
		responseObject = requests.get(url)
		response = { "url": responseObject.url, \
			"text": responseObject.text }

		# Save response into file
		self.dumpIntoFile(path, response)

		return response