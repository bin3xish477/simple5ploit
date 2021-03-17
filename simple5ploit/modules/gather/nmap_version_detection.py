from .internal.base import Gather
from os import geteuid
from json import dumps

class NmapVersionDetection(Gather):
    def __init__(self):
        super().__init__()
        self.prompt = "(NmapVersionDetection) % "
        self.args = {
            "host" : 
                { "description": "the target machine (hostname|IP)",
                  "required": True },
            "to_file" :
                {
                  "description": "save nmap JSON output to file, default=False",
                  "required": False }
        }

        for arg in self.args.keys():
            self.__dict__[arg] = "N/a"

    def run(self):
        from nmap3 import Nmap
        from nmap3.exceptions import NmapNotInstalledError
        try:
            if geteuid() != 0:
                print("[!!]::Nmap version detection scan requires `root` privileges")
                return
            result = dumps(Nmap().nmap_version_detection(self.__dict__["host"]))
            if self.__dict__["to_file"].strip().lower() == "true":
                with open(f"{self.__dict__['host']}_version_results.json", "w") as fd:
                    fd.write(result)
                    print("[**]::nmap results written to file")
            else: print(result)
        except NmapNotInstalledError:
            print("[!!]::Nmap must be installed in order to use Nmap modules")
            return
