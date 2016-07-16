import os
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
  #sleep(1)

