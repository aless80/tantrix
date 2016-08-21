"""import os
import sys
import tantrix
import subprocess
from time import sleep
for i in range(int(sys.argv[1])):
  #os.system("tantrix.py")
  #os.system('python tantrix.py')
  #subprocess.call("tantrix.py", shell=True)

  print("subprocess " + str(i))
  subprocess.call(['python', 'myscript.py'])
  sleep(01)
"""
from subprocess import Popen
import sys
from time import sleep
for i in range(int(sys.argv[1])):
    Popen(['python', 'tantrix.py'])
    sleep(0.1)
