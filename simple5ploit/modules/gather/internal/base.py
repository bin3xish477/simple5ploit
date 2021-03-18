from argparse import ArgumentParser

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
		self.cli_args = ArgumentParser()
		self.pip_dependencies = []
		
		self.cli_args.add_argument(
			"-rn", "--run",
			action="store_true",
			help="set programs args and run the module; don't enter interactive mode"
		)
	
	def run(self):
		"""
		If implemented, this function should contain
		the scripts code to run against target
		"""
		raise NotImplementedError
