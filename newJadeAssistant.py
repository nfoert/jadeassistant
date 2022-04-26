'''
Jade Assistant (NEW)
Jade assistant is the ultimate helper
for school, work, or your day to day activities
Launched via the Jade Launcher
'''
# -----
# Imports and variables
# -----

# Python standard library imports
import sys
import datetime

# Third party module imports
from PyQt5 import QtWidgets, uic, QtCore, QtGui

# Variables
version_MAJOR = 0
version_MINOR = 0
version_PATCH = 1
version_TOTAL = f"{version_MAJOR}.{version_MINOR}.{version_PATCH}"

# Starting prints
print("---------------")
print("Jade Assistant")
print(version_TOTAL)
print("---------------")


# -----
# Utility Functions
# -----
class UTILITYFuncs:
    def __init__(self):
        pass

    def log(tag, text):
        now = datetime.datetime.now()
        logFile = open("JadeAssistantLog.txt", "a")
        logFile.write(f"[{now.month}/{now.day}/{now.year}] [{now.hour}:{now.minute}] |{tag}| > '{text}'")
        logFile.close()

# -----
# Graphics
# -----

# Define the app
app = QtWidgets.QApplication(sys.argv)

# load uis
developmental = True
if developmental == True:
    
    window_main = uic.loadUi("ui/main.ui")

elif developmental == False:
    #Running as an .exe
    print("djhfkjahs")

else:
    print("There was a problem determining if it's developental or not.")

class UIFuncs:
    def __init__(self):
        pass

    


window_main.show()
app.exec()
