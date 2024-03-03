import time
import random
import msvcrt
import sys

class Typing:
    def __init__(self):
        self.__enter = False

    def holding_enter(self):
        return self.__enter

    def type(self, *words):
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
            if (char == ".") or (char == "!") or (char == ":"):
                time.sleep(0.5)
            if char == ",":
                time.sleep(0.4)
            self.cleanup()

    def slowtype(self, *words):
        str = ''
        for item in words:
            str = str + item
        # str += "\n"
            for char in str:
                if self.holding_enter() == True:
                    time.sleep(0.01)
                else:
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]))
                sys.stdout.write(char)
                sys.stdout.flush()
                if (char == ".") or (char == "!") or (char == ":") or (char == ";") or (char == "?"):
                    time.sleep(0.7)
                if char == ",":
                    time.sleep(0.4)
                
                self.cleanup()

    def cleanup(self):
        while msvcrt.kbhit():
            byte = msvcrt.getch()
            print(byte)
            if byte == b'\r':
                self.__enter = True
            else:
                self.__enter = False


type = Typing()
type.slowtype("Type for like 3 sec pleas i beg of you do it now pelase")
print()
time.sleep(3)
type.slowtype("Cleaning typing")
output = input("Enter whatevs: ")
type.slowtype("Type for like 3 sec pleas i beg of you do it now pelase")
print(output)