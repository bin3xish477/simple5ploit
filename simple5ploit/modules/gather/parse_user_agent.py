from .internal.base import Gather

class UserAgent(Gather):
    def __init__(self):
        self.prompt = "[UserAgentParser] :> "
        
        self.args = {
            "user_agent":
                {
                    "description": "user agent string to parse",
                    "required": True
                }
        }

        for arg in self.args.keys():
            self.__dict__[arg] = "N/a"

    def run(self):
        from json import loads
        from requests import get

        user_agent_string_api_url = "http://www.useragentstring.com/?uas="
        resp = get(f"{user_agent_string_api_url}{self.__dict__['user_agent']}&getJSON=all").json()
        
        print("Results:")
        print("\tAgentType \033[0;94m::\033[0m" + resp["agent_type"])
        print("\tAgentName \033[0;94m::\033[0m " + resp["agent_name"])
        print("\tAgentVersion \033[0;94m::\033[0m " + resp["agent_version"])
        print("\tOSType \033[0;94m::\033[0m " + resp["os_type"])
        print("\tOSName \033[0;94m::\033[0m " + resp["os_name"])
        print("\tOSVersionName \033[0;94m::\033[0m " + resp["os_versionName"])
        print("\tOSVersionNumber \033[0;94m::\033[0m " + resp["os_versionNumber"])
        print("\tLinuxDistribution \033[0;94m::\033[0m " + resp["linux_distibution"])
        


