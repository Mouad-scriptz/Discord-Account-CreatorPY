import threading, os
from colorama import Fore, init

init(convert=True)
print_lock = threading.Lock()

def print_with_lock(text):
    print_lock.acquire()
    print(text)
    print_lock.release()

class console():
    def information(text):
        print_with_lock(
            f"({Fore.LIGHTYELLOW_EX}*{Fore.RESET}) {Fore.YELLOW}{text}{Fore.RESET}"
        )
    def content(text, content):
        print_with_lock(
            f"({Fore.LIGHTGREEN_EX}+{Fore.RESET}) {text}: {Fore.GREEN}{content}{Fore.RESET}"
        )
    def success(text, content):
        print_with_lock(
            f"({Fore.LIGHTBLUE_EX}+{Fore.RESET}) {text}: {Fore.CYAN}{content}{Fore.RESET}"
        )
    def error(text):
        print_with_lock(
            f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.LIGHTRED_EX}{text}{Fore.RESET}"
        )
    def failure(text):
        print_with_lock(
            f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.RED}{text}{Fore.RESET}"
        )
    def input(text, custom=None):
        if custom != None:
            data = input(
                f"({Fore.LIGHTCYAN_EX}~{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET}" 
            )
        else:
            data = input(
                f"({Fore.LIGHTCYAN_EX}~{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET} >> " 
            )
        return data
    def clear(): # ONLY FOR WINDOWS
        os.system("cls")