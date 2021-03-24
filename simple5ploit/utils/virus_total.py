from vt import Client
from configparser import ConfigParser

class VT:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("../../secrets.ini")
        api_key = self.config["virus_total"]["api_key"].strip()
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = self.configure()
        self.client = Client(self.api_key)

    def configure(self):
        print("[NOTE]::the following prompt will only appear"\
                "\nthe first initial time simple5ploit is ran")
        api_key = input("[++]::please enter your VirusTotal API key: ").strip()
        self.config["virus_total"]["api_key"] = api_key
        with open("../../secrets.ini", "w") as fd:
            self.config.write(fd)
        return api_key

    def scan_file(self):
        pass

    def scan_url(self):
        pass

    def get_file_info(self):
        pass

    def get_url_info(self):
        pass
