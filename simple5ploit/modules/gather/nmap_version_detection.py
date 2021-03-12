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
            from nmap3 import Nmap
            from nmap3.exceptions import NmapNotInstalledError
            result = Nmap().nmap_version_detection(self.args["host"])
            if self.args["to_file"]:
                with open("version_detection_output.json", "w") as fd:
                    fd.write(result)
            else: print(result)
        except NmapNotInstalledError:
            print("[!!!] Nmap must be installed in order to use Nmap modules")
            return
