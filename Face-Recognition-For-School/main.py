import os
from colorama import init
from termcolor import colored

init()

while True:
    print(colored('your command >> ','yellow'),end=' ')
    s = input()
    if (s == 'insert'):
        os.system('color a')
        os.system('python dataSetGenerator.py')
        os.system('color b')
        os.system('python trainer.py')
    elif (s == 'start'):
        os.system('python detector.py')