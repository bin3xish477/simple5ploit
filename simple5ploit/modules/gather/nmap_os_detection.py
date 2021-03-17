from .internal.base import Gather
from os import geteuid
from json import dumps

class NnmapOSDetection(Gather):
    def __init__(self):
        super().__init__()
        self.prompt = "(NmapOSDetection) : "
        self.args = {
            "host":
                { "description": "the target machine (hostname|IP)",
                    "required": True },
            "to_file":
                { "description": "save nmap JSON output to file, default=False",
                    "required": False }
        }
        
        for arg in self.args.keys():
            self.__dict__[arg] = "N/a"

    def run(self):
        from nmap3 import Nmap
        from nmap3.exceptions import NmapNotInstalledError
        try:
            result = dumps(Nmap().nmap_os_detection(self.__dict__["host"]))
            if self.__dict__["to_file"].strip().lower() == "true":
                with open(f"{self.__dict__['host']}_os_detection.json", "w") as fd:
                    fd.write(result)
                    print("[**]::nmap results written to file")
            else: print(result)
        except NmapNotInstalledError:
            print("[!!]::Nmap must be intstalled in order to use Nmap modules")
            return
