from colorama import Fore, init
init(convert=True)

def info(text):
    print(
        f"({Fore.LIGHTYELLOW_EX}*{Fore.RESET}) {Fore.YELLOW}{text}{Fore.RESET}"
    )
def content(text, content):
    print(
        f"({Fore.LIGHTGREEN_EX}+{Fore.RESET}) {text}: {Fore.GREEN}{content}{Fore.RESET}"
    )
def success(text, content):
    print(
        f"({Fore.LIGHTBLUE_EX}+{Fore.RESET}) {text}: {Fore.BLUE}{content}{Fore.RESET}"
    )


def error(text):
    print(
        f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.LIGHTRED_EX}{text}{Fore.RESET}"
    )

def fail(text):
    print(
        f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.RED}{text}{Fore.RESET}"
    )
def cinput(text, no=None):
    if no != None:
        data = input(
            f"({Fore.LIGHTCYAN_EX}#{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET}" 
        )
    else:
        data = input(
            f"({Fore.LIGHTCYAN_EX}#{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET} >> " 
        )
    return data