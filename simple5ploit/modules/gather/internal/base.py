class Gather:
	def __init__(self):
		self.info = {
                    "Author": "N/a",
                    "Author Repo": "N/a",
                    "Description": "N/a",
                    "Date Completed": "N/a"
		}
		# For custom prompt, default is set below
		self.prompt = "❯ "
		self.args = {}
		self.pip_dependencies = []

	def run(self):
		raise NotImplementedError
