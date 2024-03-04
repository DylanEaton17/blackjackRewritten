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
                if ((char == ".") or (char == "!") or (char == ":") or (char == ";") or (char == "?")):
                    time.sleep(0.7)
                if (char == ","):
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
type.slowtype("here are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc")
type.slowtype("here are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc")
type.slowtype("here are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc")
type.slowtype("here are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc")
print()
time.sleep(3)
type.slowtype("Cleaning typing")
output = input("Enter whatevs: ")
type.slowtype("Type for like 3 sec pleas i beg of you do it now pelase")
print(output)