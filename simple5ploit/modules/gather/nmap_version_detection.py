from .internal.base import Gather

class NmapVersionDetection(Gather):
    def __init__(self):
        super().__init__()
        self.prompt = "nmap_version_detection % "
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
        try:
            if geteuid() != 0:
                print("[!!]::Nmap OS detection scan requires `root` privileges")
                return
            else:
                from nmap3 import Nmap
                from nmap3.exceptions import NmapNotInstalledError
                result = Nmap().nmap_version_detection(self.args["host"])
                if self.args["to_file"]:
                    with open(f"{self.args['host']}_version_results.json", "w") as fd:
                        print("[**]::writing output to file")
                        fd.write(result)
                else: print(result)
        except NmapNotInstalledError:
            print("[!!]::Nmap must be installed in order to use Nmap modules")
            return
