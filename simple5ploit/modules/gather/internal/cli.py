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
        "list": "list all available gathering scripts",
        "search": "use search string to find scripts",
        "select": "select a script",
        "sh": "run shell command on local system",
        "cls": "clear screen",
        "back": "go back to previous menu",
        "exit": "exit program"
    }

    def __init__(self, script=None):
        if script:
            self.script = script.replace("gather::", '')
        else:
            self.script = script
        self.gather_scripts_path = dirname(abspath(__file__)).replace("/internal", "")
        self.scripts = [f.rstrip(".py")
            for f in listdir(self.gather_scripts_path)
            if isfile(f"{self.gather_scripts_path}{sep}{f}") ]
        self.style = Style.from_dict({
            "prompt": "#00ff00"
        })

    def list(self):
        print("Scripts:")
        for script in self.scripts:
            print(f"\t\u2022 {script}")
        print()

    def select(self, script):
        mod = __import__(f"simple5ploit.modules.gather.{script}", fromlist=["exp"])
        gather_class = [c for (_,c) in getmembers(mod, isclass)
                        if issubclass(c, Gather) & (c is not Gather)][0]
        self.script = None
        self.gather_prompt(gather_class())

    def gather_prompt(self, cls):
        gather_args_dict = {arg: None
                for arg in cls.args.keys()}
        gather_menu_dict = {
            "help": None,
            "options": None,
            "info": None,
            "set": gather_args_dict,
            "unset": gather_args_dict,
            "sh": None,
            "run": None,
            "depends": None,
            "get": None,
            "cls": None,
            "back": None,
            "exit": None
        }

        gather_help_menu = {
            "help": "show this help message",
            "options": "show script options",
            "info": "show script information",
            "set": "set value",
            "unset": "unset value",
            "sh": "run shell command on local system",
            "run": "run script",
            "depends": "shows the dependencies needed for this script",
            "get": "install module dependencies",
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
                        headers=["Command", "Description"],
                        tablefmt="fancy_grid")
                print(table)
            elif selected == "options":
                table = tabulate(
                        [[arg, cls.__dict__[arg]] for arg in cls.args.keys()],
                        headers=["Argument", "Value"],
                        tablefmt="fancy_grid")
                print(table)
            elif selected == "info":
                table = tabulate([[k, v] for k, v in cls.info.items()],
                        headers=["Key", "Value"],
                        tablefmt="fancy_grid")
                print(table)
            elif selected.startswith("unset"):
                cls.__dict__[select.split()[-1].strip()] = ""
            elif selected.startswith("set"):
                selected = selected.split()
                if len(selected) < 2:
                    print("[!!]::the `set` command must be proceeded with an argument and value")
                    print("\nexample:\n\tset url http://localhost:8080")
                    continue
                arg, val = selected[1].strip(), " ".join(selected[2:])
                cls.__dict__[arg] = val
            elif selected == "run":
                all_set = True
                for arg, values in cls.args.items():
                    if values["required"] and (
                        not cls.__dict__[arg]
                        or cls.__dict__[arg].lower() == "n/a"):
                        print("!"*70)
                        print(f"``{arg}`` must be set before running this script")
                        all_set = False
                if all_set:
                    try:
                        cls.run()
                    except NotImplementedError:
                        print("[XX]::This exploits `run` function has not been implemented")
                    except ImportError:
                        print("[XX]::An import error occured. Run `get` to install exploit dependencies")
                    except:
                        print("[XX]::An error occurred while running the exploit")
            elif selected == "get":
                if cls.pip_dependencies:
                    print("[**]::fetching pip dependencies")
                    from pip._internal.cli.main import main as pip_main
                    [pip_main(["install", pkg]) for pkg in cls.pip_dependencies]
                    print("\n[**]::pip dependencies successfully installed")
                    print("[!!]::try re-running the exploit!!!")
                else:
                    print("[NOTE]::this module does not require any dependencies")
            elif selected.startswith("sh"):
                cmd = selected.split()[1:]
                if cmd:
                    try:
                        out = sh(cmd, capture_output=True).stdout
                    except:
                        cmd = ' '.join(cmd)
                        print(f"[XX]::unable to run command: `{cmd}`")
                        continue
                    print(out.decode("utf8"))
                else: print("[!!]::`sh` command used but no shell command was specified")
            elif selected == "cls":
                print("\n"*75)
            elif selected == "back":
                break
            elif selected == "exit":
                print("❌❌❌ Goodbye ❌❌❌")
                exit(0)
            else:
                print(f"[X]::`{selected}` is not a valid command! Type `help` for help menu")

    def help(self):
        print(self._help_)

    def init(self):
        menu = NestedCompleter.from_nested_dict({
            "help": None,
            "list": None,
            "search": None,
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
            if not self.script:
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

                if selected == "list":
                    self.list()
                elif selected.startswith("search"):
                    s = ' '.join(selected.split()[1:])
                    matched_scripts = []
                    for script in self.scripts:
                        if s in script:
                            matched_scripts.append(script)
                    if matched_scripts:
                        print("Matched Scripts:")
                        for script in matched_scripts:
                                print(f"\t* {script}")
                        print()
                    else:
                        print(f"[!!]::no script names matching: `{s}`")
                elif selected.startswith("select"):
                    selected = selected.split()
                    if len(selected) == 1 or selected[-1] == "":
                        print("[!!]::must provide an exploit by name to use, try `show` command")
                        continue
                    script = selected[-1].strip()
                    if script not in self.scripts:
                        print(f"[XX]::{exploit} is not a valid exploit, try `show` command")
                        continue
                    self.select(script)
                elif selected == "help":
                    table = tabulate([[k, v] for k, v in self._help_.items()],
                            headers=["Command", "Description"],
                            tablefmt="fancy_grid")
                    print(table)
                elif selected.startswith("sh"):
                    cmd = selected.split()[1:]
                    if cmd:
                        try:
                            out = sh(cmd, capture_output=True).stdout
                        except:
                            cmd = ' '.join(cmd)
                            print(f"[XX]::unable to run command: `{cmd}`")
                            continue
                        print(out.decode("utf8"))
                    else: print("[!!]::`sh` command used but no shell command was specified")
                elif selected == "cls":
                    print("\n"*75)
                elif selected in ("back"):
                    break
                elif selected == "exit":
                    print("❌❌❌ Goodbye ❌❌❌")
                    exit(0)
                else:
                    print(f"[XX]::`{selected}` is not a valid command! Type `help` for help menu")
            else:
                self.select(script=self.script)
