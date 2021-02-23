#!/usr/bin/env python3

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession

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

         \033[31;1;4mAuthor\033[0m:  {__author__}
         \033[31;1;4mGitHub\033[0m:  {__repo__}
         \033[31;1;4mVersion\033[0m: {__version__}"""

menu = """
\t [1] Exploits
\t [2] Gather
\t [3] Info
\t [4] Exit
"""

def main():
    print(banner)
    options = WordCompleter([str(i) for i in range(1, 5)], ignore_case=True)
    style = Style.from_dict({
        "prompt": "#f7ff00"
    })
    message = [("class:prompt", "〔main〕❯ ")]
    session = PromptSession(
                style=style,
                completer=options,
                complete_while_typing=False
            )
    while True:
        print(menu)
        try:
            selected = session.prompt(message).strip()
        except KeyboardInterrupt:
            print("Press [CTRL+D] to exit")
            continue
        except EOFError:
            print("❌❌❌ Goodbye ❌❌❌")
            break

        if selected == "": continue

        try:
            selected = int(selected)
        except ValueError:
            print("[‼] Invalid option")
            continue

        if selected == 1:
            from modules.exploits.cli import cli as exploit_cli
            exploit_cli().init()
        elif selected == 2:
            from modules.gather.cli import cli as gather_cli
            gather_cli().init()
        elif selected == 3:
            print("""
            Print information about each module category!!!
            """)
        elif selected == 4:
            print("❌❌❌ Goodbye ❌❌❌")
            break
        else:
            print("[‼] Invalid option")

if __name__ == "__main__":
    main()
