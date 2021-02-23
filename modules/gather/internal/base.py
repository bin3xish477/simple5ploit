class Gather:
	def __init__(self):
		self.info = {
                    "Author": "N/a",
                    "Author Repo": "N/a",
                    "Short Description": "N/a",
                    "Date Completed": "N/a"
		}
		# For custom prompt, default is set below
		self.prompt = "❯ "
		self.args = {}

	def run(self):
		raise NotImplementedError