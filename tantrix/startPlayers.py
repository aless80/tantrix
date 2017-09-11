from subprocess import Popen
import sys
from time import sleep
for i in range(int(sys.argv[1])):
    Popen(['python', 'tantrix.py'])
    sleep(0.1)