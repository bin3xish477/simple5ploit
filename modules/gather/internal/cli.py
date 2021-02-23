from os import listdir
from os.path import isfile
from os.path import abspath
from os.path import dirname
from os.path import sep
from os.path import basename
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from inspect import getmembers
from inspect import isclass
from imp import load_source
from .base import Gather
from sys import exit
from tabulate import tabulate
from subprocess import run as sh

class cli:
    _help_ = {
        "help": "show this help menu",
        "show": "show all available information gathering scripts",
        "select": "select a script",
        "sh": "run shell command on local system",
        "cls": "clear screen",
        "back": "go back to previous menu",
        "exit": "exit program"
    }

    def __init__(self):
        self.gather_scripts_path = dirname(abspath(__file__)).replace("/internal", "")
        self.scripts = [f.rstrip(".py")
                    for i, f in enumerate(listdir(self.gather_scripts_path))
                    if isfile(f"{self.gather_scripts_path}{sep}{f}")
                    and f not in (basename(__file__), "base.py")]
        self.style = Style.from_dict({
            "prompt": "#00ff00"
        })

    def show(self):
        print("Scripts:")
        for script in self.scripts:
            print(f"\t\u2022 {script}")
        print()

    def select(self, script):
        mod = __import__(f"modules.gather.{script}", fromlist=["exp"])
        gather_class = [c for (_,c) in getmembers(mod, isclass)
                        if issubclass(c, Gather) & (c is not Gather)][0]
        return self.gather_prompt(gather_class())

    def gather_prompt(self, cls):
        gather_args_dict = {arg: None
                for arg in cls.args.keys()}
        gather_menu_dict = {
            "help": None,
            "show": None,
            "info": None,
            "set": gather_args_dict,
            "unset": gather_args_dict,
            "sh": None,
            "run": None,
            "cls": None,
            "back": None,
            "exit": None
        }

        gather_help_menu = {
            "help": "show this help message",
            "show": "show the current state of script arguments",
            "info": "show script information",
            "set": "set value",
            "unset": "unset value",
            "sh": "run shell command on local system",
            "run": "run script",
            "cls": "clear screen",
            "back": "go back to previous menu",
            "exit": "exit program"
        }

        gather_menu = NestedCompleter.from_nested_dict(gather_menu_dict)
        message = [("class:prompt", cls.prompt)]
        while True:
            try:
                selected = self.session.prompt(
                    message,
                    style=self.style,
                    completer=gather_menu,
                    complete_while_typing=False
                ).strip()
            except KeyboardInterrupt:
                print("Press [CTRL+D] to exit")
                continue
            except EOFError:
                print("❌❌❌ Goodbye ❌❌❌")
                exit(1)

            if selected == "help":
                table = tabulate(
                        [[k, v] for k, v in gather_help_menu.items()],
                        headers=["Command", "Description"])
                print(table)
            elif selected == "show":
                table = tabulate(
                        [[arg, cls.__dict__[arg]] for arg in cls.args.keys()],
                        headers=["Argument", "Value"])
                print(table)
            elif selected == "info":
                table = tabulate([[k, v] for k, v in cls.info.items()],
                        headers=["Key", "Value"])
                print(table)
            elif selected.startswith("unset"):
                cls.__dict__[select.split()[-1].strip()] = ""
            elif selected.startswith("set"):
                selected = selected.split()
                if len(selected) < 2:
                    print("the `set` command must be proceeded with an argument and value")
                    print("\nexample:\n\tset url http://localhost:8080")
                    continue
                arg, val = selected[1].strip(), " ".join(selected[2:])
                cls.__dict__[arg] = val
            elif selected == "run":
                try:
                    cls.run()
                except NotImplementedError:
                    print("[X] This exploits `run` function has not been implemented")
            elif selected.startswith("sh "):
                cmd = selected.split()[1:]
                if cmd:
                    try:
                        out = sh(cmd, capture_output=True).stdout
                    except:
                        cmd = ' '.join(cmd)
                        print(f"unable to run command: `{cmd}`")
                        continue
                    print(out.decode("utf8"))
                else: print("`sh` command used but no shell command was specified")
            elif selected == "cls":
                print("\n"*75)
            elif selected == "back":
                break
            elif selected == "exit":
                print("❌❌❌ Goodbye ❌❌❌")
                exit(0)
            else:
                print(f"`{selected}` is not a valid command! Type `help` for help menu")

    def help(self):
        print(self._help_)

    def init(self):
        menu = NestedCompleter.from_nested_dict({
            "help": None,
            "show": None,
            "select": {script: None for script in self.scripts},
            "sh": None,
            "cls": None,
            "back": None,
            "exit": None
        })

        self.session = PromptSession(
                complete_while_typing=False,
                auto_suggest=AutoSuggestFromHistory()
        )
        message = [("class:prompt", "〔Gather〕❯ ")]
        while True:
            try:
                selected = self.session.prompt(
                    message,
                    style=self.style,
                    completer=menu,
                ).strip()
            except KeyboardInterrupt:
                print("Press [CTRL+D] to exit")
                continue
            except EOFError:
                print("❌❌❌ Goodbye ❌❌❌")
                exit(1)

            if selected == "show":
                self.show()
            elif selected.startswith("select"):
                selected = selected.split()
                if len(selected) == 1 or selected[-1] == "":
                    print("Must provide an exploit by name to use, try `show` command")
                    continue
                script = selected[-1].strip()
                if script not in self.scripts:
                    print(f"{exploit} is not a valid exploit, try `show` command")
                    continue
                self.select(script)
            elif selected == "help":
                table = tabulate([[k, v] for k, v in self._help_.items()],
                        headers=["Command", "Description"])
                print(table)
            elif selected.startswith("sh"):
                cmd = selected.split()[1:]
                if cmd:
                    try:
                        out = sh(cmd, capture_output=True).stdout
                    except:
                        cmd = ' '.join(cmd)
                        print(f"unable to run command: `{cmd}`")
                        continue
                    print(out.decode("utf8"))
                else: print("`sh` command used but no shell command was specified")
            elif selected == "cls":
                print("\n"*75)
            elif selected in ("back"):
                break
            elif selected == "exit":
                print("❌❌❌ Goodbye ❌❌❌")
                exit(0)
