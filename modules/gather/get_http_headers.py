from requests import get
from .internal.base import Gather
from tabulate import tabulate

class GetHTTPHeaders(Gather):
    def __init__(self):
        super().__init__()
        self.prompt = "❯ "

        self.args = {
            "url": "the URL to make request to and parse headers for"
        }

        for arg in self.args.keys():
            self.__dict__[arg] = "N/a"

    def run(self):
        response = get(self.url)

        resp_headers = [
            [k, v] for k, v in response.headers.items()
        ]

        table = tabulate(
            resp_headers,
            headers=["HTTP Header", "Value"],
            tablefmt="presto"
        )
        print(table)
