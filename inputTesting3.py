import random
import time
import sys
from colorama import Fore, Back, Style
import lists
import msvcrt

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
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


    def retype(self, *words):
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


    def menu_cleanup(self):
        while msvcrt.kbhit():
            byte_int = ord(msvcrt.getch())
            if byte_int == 224:
                byte_int = ord(msvcrt.getch())
                if byte_int == 80:
                    return "Down"
                elif byte_int == 72:
                    return "Up"
            elif byte_int == 13:
                return "Enter"


    def select_one(self, message, options, index = 0):
        self.type(message + ":")
        print()
        for i in range(len(options)):
            if i == index:
                self.type("-> " + options[i])
            else:
                self.type("   " + options[i])
            if i!= len(options)-1:
                print()
            else:
                self.type(" ")
        
        for _ in range(4):
            print('\033[1A')

        key = None
        while True:
            if key == "Up" and index > 0:
                print("   ", end="\r" * (len(options)-index))
                index-=1
                print("-> ", end="\r" * (len(options)-index))
            elif key == "Down" and index < len(options)-1:
                print("   ", end="\r" * (len(options)-index))
                index+=1
                print("-> ", end="\r" * (len(options)-index))
            elif key == "Enter":
                return index
            key = self.menu_cleanup()
    
    def continue_cleanup(self):
        while msvcrt.kbhit():
            return True
                    


def main():
    type = Typing()
    # type.print_key_int()
    type.type("Hello")
    type.retype("Hi bro whats up")

main()