import random
import time
import sys
from colorama import Fore, Back, Style, init
init(convert=True)
import lists
import msvcrt

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""

# all the pretty colors
def red(text):
    return (Fore.RED + text + Fore.WHITE)

def green(text):
    return (Fore.GREEN + text + Fore.WHITE)
            
def magenta(text):
    return (Fore.MAGENTA + text + Fore.WHITE)

def yellow(text):
    return (Fore.YELLOW + text + Fore.WHITE)

def cyan(text):
    return (Fore.CYAN + text + Fore.WHITE)
            
def bright(text):
    return (Style.BRIGHT + text + Style.NORMAL)

def open_quote(text):
    return ("\"" + text)

def close_quote(text):
    return (text + "\"")

def quote(text):
    return ("\"" + text + "\"")

def space_quote(text):
    return ("\"" + text + "\" ")

class Typing:
    def __init__(self):
        self.__type_speed = "Default"

    def fast(self, *words):
        str = ''
        for item in words:
            str = str + item
        # str += "\n"
        for char in str:
            time.sleep(random.choice([
            0.03, 0.05, 0.04, 0.02,
            0.05, 0.03, 0.02, 0.05, 0.04, 0.01
            ]))
            sys.stdout.write(char)
            sys.stdout.flush()
            if ((char == ".") or (char == "!") or (char == ":")):
                time.sleep(0.5)
            if (char == ","):
                time.sleep(0.4)
            self.cleanup()

    def slow(self, *words):
        str = ''
        for item in words:
            str = str + item
        # str += "\n"
            for char in str:
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]))
                sys.stdout.write(char)
                sys.stdout.flush()
                if ((char == ".") or (char == "!") or (char == ":") or (char == ";")):
                    time.sleep(0.7)
                if (char == ","):
                    time.sleep(0.4)
                self.cleanup()

    def suspense(self, *words):
        str = ''
        for item in words:
            str = str + item
        # str += "\n"
            for char in str:
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]) + 0.05)
                sys.stdout.write(char)
                sys.stdout.flush()
                if ((char == ".") or (char == "!") or (char == ":") or (char == ";")):
                    time.sleep(0.7)
                if (char == ","):
                    time.sleep(0.4)
                self.cleanup()

    def type(self, *words):
        str = ''
        for item in words:
            str = str + item
            for char in str:
                if self.__type_speed == "Default":
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]))
                if self.__type_speed == "Fast":
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]) - 0.01)
                if self.__type_speed == "Fastest":
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]) - 0.02)
                if self.__type_speed == "Print":
                    time.sleep(0.001)

                sys.stdout.write(char)
                sys.stdout.flush()

                if self.__type_speed =="Default" and ((char == ".") or (char == "!") or (char == ";")):
                    time.sleep(0.7)
                elif self.__type_speed =="Fast" and ((char == ".") or (char == "!") or (char == ";")):
                    time.sleep(0.5)
                elif self.__type_speed =="Fastest" and ((char == ".") or (char == "!") or (char == ";")):
                    time.sleep(0.4)

                if self.__type_speed =="Default" and (char == ","):
                    time.sleep(0.4)
                elif self.__type_speed =="Fast" and (char == ","):
                    time.sleep(0.3)
                elif self.__type_speed =="Fastest" and (char == ","):
                    time.sleep(0.2)

                if self.__type_speed =="Default" and (char == "?") or (char == ":"):
                    time.sleep(0.3)
                elif self.__type_speed =="Fast" and (char == "?") or (char == ":"):
                    time.sleep(0.2)
                elif self.__type_speed =="Fastest" and (char == "?") or (char == ":"):
                    time.sleep(0.1)
                
                self.cleanup()


    def print_key(self):
        while True:
            while msvcrt.kbhit():
                byte = msvcrt.getch()
                print(byte)
                if byte == b'\r':
                    return
                

    def print_key_int(self):
        while True:
            while msvcrt.kbhit():
                byte = msvcrt.getch()
                print(ord(byte))
                if byte == b'\r':
                    return


    def cleanup(self):
        while msvcrt.kbhit():
            byte = msvcrt.getch()
            if byte == b',':
                self.__type_speed = "Default"
            elif byte == b'.':
                self.__type_speed = "Fast"
            elif byte == b'/':
                self.__type_speed = "Fastest"
            elif byte == b'p':
                self.__type_speed = "Print"



    
    def continue_cleanup(self):
        while msvcrt.kbhit():
            return True
                    
    def typeover(self, old, new, started=False):
        if not started:
            self.type(old)
        print("", end="\r")
        self.type(" "*len(old))
        print("", end="\r")
        self.type(new)
        print("\n")

type = Typing()

def choose_a_number(a, b):
    while True:
        lucky_number = None
        while lucky_number is None:
            type.fast("Choose a number between " + str(a) + " and " + str(b) + ": ")
            try:
                lucky_number = int(input(""))
            except ValueError:
                print("")
                type.fast(red("That's, like, not a number."))
                print("\n")

        if a<=lucky_number<=b:
            return lucky_number
        else:
            print("")
            type.fast(red("That's not in range."))
            print("\n")


def ticket(max=10, length=5, print_ticket=False):
    type.type()
    lucky_number = choose_a_number(1, max)
    matches = 0
    winning_numbers = []
    unscratched_str = ""
    for _ in range(length):
        unscratched_str += "  **"
    scratched_str = ""
    matches_str = ""
    for _ in range(length):
        new_numb = random.randint(1, max)
        winning_numbers.append(new_numb)
        if 1 <= new_numb <= 9:
            if new_numb == lucky_number:
                matches+=1
                matches_str += "  " + bright(green(str(0) + str(new_numb)))
                scratched_str += "  " + str(0) + str(new_numb)
            else:
                matches_str += "  " + str(0) + str(new_numb) 
                scratched_str += "  " + str(0) + str(new_numb)
        else:
            if new_numb == lucky_number:
                matches+=1
                matches_str += bright(green(str(new_numb))) + "  "
                scratched_str += str(new_numb) + "  "
            else:
                scratched_str += str(new_numb) + "  "
                matches_str += str(new_numb) + "  "
            

    type.slow("Your number is: " + str(lucky_number))
    print()
    type.suspense(unscratched_str[:-2])
    print("", end="\r")
    type.suspense(scratched_str[:-2])
    if matches > 0:
        for blink_count in range(3):
            time.sleep(0.6)
            print("", end="\r")
            print(matches_str, end="\r")
            time.sleep(0.6)
            if blink_count < 2:
                time.sleep(0.6)
                print("", end="\r")
                print(scratched_str, end="\r")
        print("")
        if matches == 1:
            type.type("You had " + str(matches) + " match.")
        else:
            type.type("You had " + str(matches) + " matches.")
    else:
        print("")
        type.type("Welp. Guess that one was a loser.")


def main():
    ticket(20, 25)

main()