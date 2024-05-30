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

    def fast(self, punc=True, *words):
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
            if ((char == ".") or (char == "!") or (char == ":")) and punc:
                time.sleep(0.5)
            if (char == ",") and punc:
                time.sleep(0.4)
            self.cleanup()

    def slow(self, punc=True, *words):
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
                if ((char == ".") or (char == "!") or (char == ":") or (char == ";")) and punc:
                    time.sleep(0.7)
                if (char == ",") and punc:
                    time.sleep(0.4)
                self.cleanup()

    def type(self, *words, punc=True,):
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

                if punc:
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

    def press_continue(self):
        self.type("Press any key to continue: ", punc=False)
        is_pressed = False
        while not is_pressed:
            is_pressed = self.continue_cleanup()
    
    def continue_cleanup(self):
        while msvcrt.kbhit():
            return True
        
            
            


def main():
    type = Typing()
    type.type("Hello")
    type.press_continue()
    type.type("Wow you made it congratulations")

main()