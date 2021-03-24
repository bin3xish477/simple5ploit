from .internal.base import Gather


class UserAgent(Gather):
    def __init__(self):
        self.prompt = "[UserAgentParser] >> "
        
        self.args = {
            "user-agent":
                {
                    "description": "user agent string to parse",
                    "required": True
                }
        }

        for arg in self.args.keys():
            self.__dict__[arg] = "N/a"

    def run(self):
        pass
