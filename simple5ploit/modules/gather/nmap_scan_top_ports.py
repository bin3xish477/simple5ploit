from .internal.base import Gather
from json import dumps

class NmapScanTopPorts(Gather):
    def __init__(self):
        super().__init__()
        self.prompt = "(NmapScanTopPorts) : "
        self.args = {
            "host":
                { "description" : "the target machine (hostname|IP)",
                    "required": True },
            "to_file":
                { "description": "save nmap JSON output to file, default=False",
                    "required": False }
        }

        for arg in self.args.keys():
            self.__dict__[arg] = "N/a"

    def run(self):
        from nmap3 import Nmap
        from nmap3.exceptions import Nmap
        try:
            result = Nmap().scan_top_ports(self.__dict__["host"])
            print(dumps(result, indent=2))
            if self.__dict__["to_file"].strip().lower() == "true":
                with open(f"{self.__dict__['host']}_top_ports_results.json", "w") as fd:
                    fd.write(dumps(result, indent=4))
                    print("[**]::nmap results written to file")
        except NmapNotInstalledError:
            print("[!!]::Nmap must be installed in order to use Nmap modules")
            return
