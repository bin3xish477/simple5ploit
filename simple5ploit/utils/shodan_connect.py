from shodan import Shodan
from config import ConfigParser

class ShodanConnect:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("../../secrets.ini")

    def search(self):
        pass

    def parse_search_results(self):
        pass
