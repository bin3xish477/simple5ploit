from prompt_toolkit import WordCompleter
from sys import exit

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
        menu_words = WordCompleter(self._menu_.keys(), ignore_case=True)
        message = [("class:prompt", "〔apis〕❯ ")]
        while True:
            try:
                selected = prompt(
                    message,
                    style=self.style,
                    completer=menu_words,
                    complete_while_typing=False
                ).strip()
            except KeyboardInterrupt:
                continue
            except EOFError:
                print("❌❌❌ Goodbye ❌❌❌")
                exit(1)

            if selected == "show":
                self.show()
            elif "select" in selected:
                try:
                    n = int(selected.split()[-1])
                except ValueError:
                    print("[X] Select module by integer value")
                    continue
                exit = self.select(n)
            elif selected == "help":
                self.help()
            elif selected == "cls":
                print("\n"*75)
            elif selected == "back":
                break
            elif selected == "exit":
                print("❌❌❌ Goodbye ❌❌❌")
                exit(0)
