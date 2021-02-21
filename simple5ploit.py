#!/usr/bin/env python3

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt

__version__ = "1.0"
__author__  = "binexisHATT"
__repo__    = "https://github.com/binexisHATT"

banner = f"""
  _____   _                   __         _____              __         _  _
 (_____) (_)                 (__)  ____ (_____) ____       (__)       (_)(_)_
(_)___    _   __   __   ____  (_) (____)(_)___ (____) ____  (_)  ___   _ (___)
  (___)_ (_) (__)_(__) (____) (_)(_)_(_)(_____)(_)__ (____) (_) (___) (_)(_)
  ____(_)(_)(_) (_) (_)(_)_(_)(_)(__)__  ____(_)_(__)(_)_(_)(_)(_)_(_)(_)(_)_
 (_____) (_)(_) (_) (_)(____)(___)(____)(_____)(____)(____)(___)(___) (_) (__)
                       (_)                           (_)
                       (_)                           (_)

                    \033[31;1;4mAuthor\033[0m: {__author__}
                    \033[31;1;4mGitHub\033[0m: {__repo__}"""

menu = """
\t\t\t[1] Exploits [5] Utils
\t\t\t[2] Gather   [6] APIs
\t\t\t[3] Crypto   [7] Info
\t\t\t[4] Shells   [8] Exit
"""
def main():
    print(banner)
    options = WordCompleter([str(i) for i in range(1, 8)], ignore_case=True)
    style = Style.from_dict({
        "prompt": "#f7ff00"
    })
    message = [("class:prompt", "〔main〕❯ ")]
    exit = False
    while not exit:
        print(menu)
        try:
            selected = prompt(
                message,
                style=style,
                completer=options,
                complete_while_typing=False).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye ❌❌❌")
            break

        if selected == "": continue

        try:
            selected = int(selected)
        except ValueError:
            print("[‼] Invalid option")
            continue

        if selected == 1:
            from modules.exploits.cli import cli
            exit = cli().init()
        elif selected == 2:
            from modules.gather.cli import cli
            exit = cli().init()
        elif selected == 3:
            from modules.crypto.cli import cli
            exit = cli().init()
        elif selected == 4:
            from modules.shells.cli import cli
            exit = cli().init()
        elif selected == 5:
            from modules.utils.cli import cli
            exit = cli().init()
        elif selected == 6:
            from modules.apis.cli import cli
            exit = cli().init()
        elif selected == 7:
            print("\nGoodbye ❌❌❌")
            break
        else:
            print("[‼] Invalid option")
    else:
        print("Goodbye ❌❌❌")

if __name__ == "__main__":
    main()
