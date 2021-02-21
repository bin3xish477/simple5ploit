from prompt_toolkit import WordCompleter

class cli():
    _menu_ = {
            "help": "show this help menu",
            "show": "get all available exploits",
            "select": "select an exploit by number"
            "back": "go back to previous menu",
            "exit": "exit program"
    }

    def show():
        pass

    def select():
        pass

    def init(self):
        menu_words = self._menu.keys()
        while True:
            selected = input("❯ ")
