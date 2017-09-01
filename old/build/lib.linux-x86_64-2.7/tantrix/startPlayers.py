from subprocess import Popen
import sys
from time import sleep
for i in range(int(sys.argv[1])):
    Popen(['python', 'tantrix.py'])
    sleep(0.1)

"""print(len(sys.argv))
for ar in sys.argv:
    print(ar)"""
"""

if len(sys.argv) == 2:
    ready = str(sys.argv[1])
for i in range(int(sys.argv[1])):
    Popen(['python', 'tantrix.py "'+'player'+str(i)+'"'])
    sleep(0.1)
"""