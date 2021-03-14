#!/usr/bin/env python3

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from argparse import ArgumentParser
from simple5ploit.utils.server import serve
from simple5ploit.modules.exploits.internal.cli import cli as exploit_cli
from .modules.gather.internal.cli import cli as gather_cli
from os.path import isfile
from os import listdir
from os import sep
from simple5ploit.__init__ import __version__
from simple5ploit.__init__ import __author__
from simple5ploit.__init__ import __repo__


banner = f"""
  _____   _                   __         _____              __         _  _
 (_____) (_)                 (__)  ____ (_____) ____       (__)       (_)(_)_
(_)___    _   __   __   ____  (_) (____)(_)___ (____) ____  (_)  ___   _ (___)
  (___)_ (_) (__)_(__) (____) (_)(_)_(_)(_____)(_)__ (____) (_) (___) (_)(_)
  ____(_)(_)(_) (_) (_)(_)_(_)(_)(__)__  ____(_)_(__)(_)_(_)(_)(_)_(_)(_)(_)_
 (_____) (_)(_) (_) (_)(____)(___)(____)(_____)(____)(____)(___)(___) (_) (__)
                       (_)                           (_)
                       (_)                           (_)

         \033[31;1;4mAuthor\033[0m:  {__author__}
         \033[31;1;4mGitHub\033[0m:  {__repo__}
         \033[31;1;4mVersion\033[0m: {__version__}"""

menu = """
\t {1} Exploits
\t {2} Gather
\t {3} Exit
"""

def main(args):
    path = __file__.replace(f"{sep}{__name__}.py", '')
    exploits_path = f"{path}{sep}modules{sep}exploits"
    gather_path   = f"{path}{sep}modules{sep}gather"
    exploit_modules = [ f"exploit::{f}" for f in listdir(exploits_path) if isfile(f"{exploits_path}{sep}{f}") ]
    gather_modules  = [ f"gather::{f}" for f in listdir(gather_path) if isfile(f"{gather_path}{sep}{f}") ]
    modules = list(map(lambda s: s.rstrip(".py"), exploit_modules + gather_modules))
    if args.server:
        serve(args.server)
        return
    if args.list_modules:
        print("\n--- Available Modules ---")
        for module in modules:
            print(' '*3, f"\u2022 {module}")
        return
    
    if args.module:
        if args.module not in modules:
            print(f"[X]::{args.module} is not a valid module, " \
                    "use the `-l` arg to list available modules")
            return
        if "exploit::" in args.module:
            exploit_cli(exploit=args.module).init()
        else:
            gather_cli(script=args.module).init()
    if not args.quite:
        print(banner)
    options = WordCompleter(["exploits", "gather", "exit"], ignore_case=True)
    style = Style.from_dict({
        "prompt": "#f7ff00"
    })
    message = [("class:prompt", "〔Main〕❯ ")]
    while True:
        print(menu)
        try:
            selected = prompt(
                    message,
                    completer=options,
                    style=style,
                    complete_while_typing=False
            ).strip()
        except KeyboardInterrupt:
            print("Press [CTRL+D] to exit")
            continue
        except EOFError:
            print("❌❌❌ Goodbye ❌❌❌")
            break

        if selected == "": continue

        elif selected == "exploits":
            exploit_cli().init()
        elif selected == "gather":
            gather_cli().init()
        elif selected == "exit":
            print("❌❌❌ Goodbye ❌❌❌")
            break
        else:
            print("[‼] Invalid option")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-q", "--quite", action="store_true", help="don't print simple5ploit banner")
    parser.add_argument("-l", "--list-modules", action="store_true", help="list all available modules")
    parser.add_argument("-m", "--module", help="specify module to load")
    parser.add_argument("-s", "--server", type=int, metavar="PORT",
            help="HTTP server using `http.server` module")
    main(parser.parse_args())
