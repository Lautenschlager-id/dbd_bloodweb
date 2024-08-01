import os
import time
from colorama import Fore, Back, Style, init

init(autoreset=True)

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():

    print(Fore.CYAN + Style.BRIGHT + "=" * 40)
    print(Fore.CYAN + Style.BRIGHT + " " * 12 + "MENU" + " " * 12)
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)
    print()

def print_menu():
    print(Fore.GREEN + "1 - Process All Images")
    print(Fore.GREEN + "2 - Run")
    print(Fore.GREEN + "3 - Bloodweb")
    print(Fore.GREEN + "4 - Leave")
    print("\n")
    print()

def show_menu():
    clear_screen()
    print_header()
    print_menu()
    choice = input(Fore.YELLOW + "Enter your choice (1-4): " + Style.RESET_ALL)
    return choice
