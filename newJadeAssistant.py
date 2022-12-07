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
import threading
from time import sleep
import random
import shelve
import subprocess
from pathlib import PurePath
import os
import platform
import webbrowser

# Third party module imports
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import pyttsx3
import wolframalpha
import wikipedia

# Local imports
import assets

# Set up imports - pyttsx3
pyttsx3Engine = pyttsx3.init()

pyttsx3Voices = pyttsx3Engine.getProperty('voices') 
pyttsx3Engine.setProperty('voice', pyttsx3Voices[1].id)

pyttsx3Rate = pyttsx3Engine.getProperty('rate')
pyttsx3Engine.setProperty("rate", 200)

# Set up imports - wolframalpha
WolframAppId = "RYYW2P-LGP527T87X"
WolframAlphaClient = wolframalpha.Client(WolframAppId)


# Variables
version_MAJOR = 1
version_MINOR = 0
version_PATCH = 1
version_TOTAL = f"{version_MAJOR}.{version_MINOR}.{version_PATCH}"
developmental = False

speakLoopList = []

engineInput = ""
jadeLastSaid = ""
youLastSaid = ""

appActive = True

appPaths = {}

wolframInput = ""
wikipediaInput = ""
fullWikiPageContent = ""

guiLoopList = []

addAppName = ""
addAppPath = ""

killThreads = False

size = 4

# ----------
# Set up the resource manager
# ----------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Starting prints
print("---------------")
print("Jade Assistant")
print(version_TOTAL)
print("---------------")

# -----
# Classes
# -----
class AppPaths:
    '''A group of functions to control app paths'''

    def __init__():
        pass

    def savePaths(input):
        appPathShelf = shelve.open("appPath")
        if type(input) == dict:
            appPathShelf["data"] = input
            appPathShelf.close()

        else:
            print("Input is not a dictionary!")
            appPathShelf.close()

    def loadPaths():
        global appPaths
        print("Loading data...")
        try:
            appPathShelf = shelve.open("appPath")
            appPaths = appPathShelf["data"]
        except:
            AppPaths.savePaths({})

        print("Done.")

    def openApp(app):
        global appPaths
        AppPaths.loadPaths()

        if app in appPaths:

            if ASSISTANTFuncs.containsAny(appPaths[app], ["https://", "http://"]) == True:
                ASSISTANTFuncs.respond(f"Opening website {app}...")
                webbrowser.open(appPaths[app])

            elif app in appPaths:
                try:
                    if platform.system() == "Windows":
                        ASSISTANTFuncs.respond(f"Opening {app}...")
                        subprocess.Popen(PurePath(appPaths[app]))

                    elif platform.system() == "Darwin":
                        ASSISTANTFuncs.respond(f"Opening {app}...")
                        subprocess.call(["open", f"{PurePath(appPaths[app])}"])
                
                except Exception as e:
                    ASSISTANTFuncs.respond(f"There was a problem opening app '{app}' {e}")

            else:
                ASSISTANTFuncs.respond("I couldnt find that app. Add an app by entering 'add app'.")

        else:
            ASSISTANTFuncs.respond("I couldnt find that app. Add an app by entering 'add app'.")

    def listApps():
        global appPaths
        AppPaths.loadPaths()
        if len(appPaths) != 0:
            ASSISTANTFuncs.respond(f"Here are the apps:")
            for key, value in appPaths.items():
                ASSISTANTFuncs.respond(f"'{str(key)}', with path '{str(value)}'")

        else:
            ASSISTANTFuncs.respond("You haven't added any apps to my database. Enter 'add app' to add one.")

    def removeApp(app):
        global appPaths
        AppPaths.loadPaths()
        if len(appPaths) != 0:
            try:
                del appPaths[app]
                AppPaths.savePaths(appPaths)
                ASSISTANTFuncs.respond(f"I removed the app {app}.")

            except Exception as e:
                ASSISTANTFuncs.respond("I couldn't find that app to remove. Enter 'app list' to see all apps in my database.")
                print(e)
        else:
            ASSISTANTFuncs.respond("You don't currently have any apps in the list. You could enter 'add app' to add an app then remove it again if you really wanted, though I don't see a point in that.")
        


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
# Assistant Functions
# -----
class ASSISTANTFuncs:
    '''A group of functions that control the Assistant'''
    def __init__(self):
        pass

    def respond(text):
        global jadeLastSaid
        global size
        global appActive

        window_main.listWidget.addItem("Loading...")
        count = window_main.listWidget.count()
        count = count - 1
        window_main.listWidget.item(count).setBackground(QtGui.QColor("#A8C6AE"))
        window_main.listWidget.item(count).setForeground(QtGui.QColor("#FFFFFF"))
        window_main.listWidget.item(count).setText(f"      [Jade] {text}")

        window_medium.listWidget.addItem("Loading...")
        count = window_medium.listWidget.count()
        count = count - 1
        window_medium.listWidget.item(count).setBackground(QtGui.QColor("#A8C6AE"))
        window_medium.listWidget.item(count).setForeground(QtGui.QColor("#FFFFFF"))
        window_medium.listWidget.item(count).setText(f"      [Jade] {text}")

        window_small.listWidget.addItem("Loading...")
        count = window_small.listWidget.count()
        count = count - 1
        window_small.listWidget.item(count).setBackground(QtGui.QColor("#A8C6AE"))
        window_small.listWidget.item(count).setForeground(QtGui.QColor("#FFFFFF"))
        window_small.listWidget.item(count).setText(f"      [Jade] {text}")

        if speakLoopThread.is_alive() == True:
            jadeLastSaid = text.lower()
            speakLoopList.append(text)

        else:
            if appActive == False:
                jadeLastSaid = text.lower()
                ASSISTANTFuncs.respond("It looks like the thread that makes me speak has stopped. Please restart me by entering 'restart'")

            else:
                return True



    def respondRandom(list):
        choice = random.choice(list)
        print(f"Picked {choice}")
        ASSISTANTFuncs.respond(choice)

    def youSaid(text):

        window_main.listWidget.addItem(f"      [You] {text}")
        count = window_main.listWidget.count()
        count = count - 1
        window_main.listWidget.item(count).setBackground(QtGui.QColor("#F4EBD0"))

        window_medium.listWidget.addItem(f"      [You] {text}")
        count = window_medium.listWidget.count()
        count = count - 1
        window_medium.listWidget.item(count).setBackground(QtGui.QColor("#F4EBD0"))

        window_small.listWidget.addItem(f"      [You] {text}")
        count = window_small.listWidget.count()
        count = count - 1
        window_small.listWidget.item(count).setBackground(QtGui.QColor("#F4EBD0"))


    def isGreeting(text):
        # Thanks to Vishnudev's comment on StackOverflow https://stackoverflow.com/questions/63987341/if-statement-always-true-string
        
        text = text.replace(".", "")
        if text in ["hi", "hello", "hey", "hi there", "hello there", "hey there", "hola"]:
            print("Is a greeting!")
            return True

        else:
            print("Not a greeting!")
            return False

    def containsAll(INPUT, LIST):
        '''A simple function to check if a string contains all other strings'''
        # Thanks to Martijn Mark Byers answer on StackOverflow https://stackoverflow.com/a/3389611
        if all(x in INPUT for x in LIST) == True:
            return True

        elif all(x in INPUT for x in LIST) == False:
            return False

        else:
            return False

    def containsAny(INPUT, LIST):
        if any(x in INPUT for x in LIST) == True:
            return True

        elif any(x in INPUT for x in LIST) == False:
            return False

        else:
            return False

    def startupGreeting():
        ASSISTANTFuncs.respondRandom(["Hey there!", "How can I help?", "It's nice to see you.", "Hello there!", "Why hello there.", "Enter 'help' and I'll tell you what I can do."])
        


# -----
# Main Code
# -----
class MAINFuncs:
    '''A group of main functions'''
    def __init__(self):
        pass

    def jadeEngine():
        global engineInput
        global jadeLastSaid
        global youLastSaid
        global wolframInput

        global addAppName
        global addAppPath

        global appActive

        print(f"Running Jade Engine with input '{engineInput}'")
        ASSISTANTFuncs.youSaid(engineInput)
        if youLastSaid == "addApp1" or "open" in engineInput:
            EI = engineInput

        else:
            engineInput = engineInput.lower()
            EI = engineInput

        # The ultimate conditionals
        
        isGreeting = ASSISTANTFuncs.isGreeting(EI)
        
        if isGreeting == True:
            ASSISTANTFuncs.respondRandom(["Hello there!", "Hey there!", "Hello.", "Hi.", "Hey!"])

        elif EI == jadeLastSaid:
            ASSISTANTFuncs.respondRandom(["Don't make fun of me.", "Please don't make fun of me.", "It's not nice to make fun of people."])

        elif ASSISTANTFuncs.containsAll(EI, ["how", "are", "you"]) == True:
            ASSISTANTFuncs.respond("I'm doing well, thank you.")

        elif ASSISTANTFuncs.containsAll(EI, ["your", "name"]) == True:
            ASSISTANTFuncs.respondRandom(["My name is Jade.", "My name is Jade, but I thought you already knew that.", "Just look upward about 4 centimenters and you'll see."])

        elif ASSISTANTFuncs.containsAll(EI, ["birthday"]) == True:
            ASSISTANTFuncs.respond("My birthday is February twenty-third.")

        elif ASSISTANTFuncs.containsAny(EI, ["info", "about"]) == True:
            ASSISTANTFuncs.respond("My name is Jade and i'm a Virtual Assistant for your computer's desktop. I'm written in the Python Programming Language and converted to an executable file by PyInstaller. My goal is to be as helpful as possible. I was first created on February 23, 2021. The current iteration of me was created April-May 2022.")
            ASSISTANTFuncs.respond("Enter 'jade website' to view my inter-web space.")
        
        elif ASSISTANTFuncs.containsAny(EI, ["thanks", "thank you"]) == True:
            ASSISTANTFuncs.respondRandom(["Im glad I could help.", "You're welcome"])
            youLastSaid = "thanks"

        elif ASSISTANTFuncs.containsAny(EI, ["quit", "shutdown"]) == True:
            ASSISTANTFuncs.respond("Goodbye.")
            UIFuncs.quit()

        elif ASSISTANTFuncs.containsAny(EI, ["restart", "reset", "reboot"]) == True:
            ASSISTANTFuncs.respond("Restarting...")

            if platform.system() == "Windows":
                subprocess.Popen("Jade Assistant.exe")
                appActive = False
                UIFuncs.quit()

            elif platform.system() == "Darwin":
                subprocess.Popen("Jade Assistant")
                appActive = False
                UIFuncs.quit()

            else:
                ASSISTANTFuncs.respond("Your OS isn't supported! Please use Windows or Mac.")

        elif ASSISTANTFuncs.containsAll(EI, ["divide", "zero"]) == True or ASSISTANTFuncs.containsAll(EI, ["divide", "0"]) == True:
            ASSISTANTFuncs.respond("You probably wanted me to say something about Cookie Monster and him having no friends. I can't really say that though, Apple probably copywrited it and then I'll go to jail.")
            ASSISTANTFuncs.respond("I don't want to go to jail.")

        elif ASSISTANTFuncs.containsAny(EI, ["wolfram alpha", "wolfram|alpha", "wolfram"]) == True:
            ASSISTANTFuncs.respond(" I will try to find some data from Wolfram|Alpha.")
            EI.replace("wolfram alpha ", "")
            EI.replace("wolfram|alpha ", "")
            EI.replace("wolfram ", "")
            try:
                WolframAlphaTry = WolframAlphaClient.query(EI)
                WolframAlphaAnswer = next(WolframAlphaTry.results).text
                print(WolframAlphaAnswer)
                
                window_main.info.setText("")
                ASSISTANTFuncs.respond(WolframAlphaAnswer)

            except StopIteration:
                print("Wolfram|Alpha failed.")
                ASSISTANTFuncs.respond("I couldn't find anything.")

        elif ASSISTANTFuncs.containsAll(EI, ["read", "more"]) == True:
            if len(fullWikiPageContent) > 10:
                ASSISTANTFuncs.respond(f"Reading the remainder of the previously loaded wikipedia article. {fullWikiPageContent}")

            else:
                ASSISTANTFuncs.respond("There's nothing to read more of. Ask for some info first. Eg. 'Python Programming Language'")

        elif ASSISTANTFuncs.containsAny(EI, ["open", "open app"]) == True:
            EI = EI.replace("open ", "")
            EI = EI.replace("open app ", "")
            if platform.system() == "Darwin":
                EI = EI.capitalize()

            
            AppPaths.openApp(EI)

        elif ASSISTANTFuncs.containsAny(EI, ["add app", "add path"]) == True:
            youLastSaid = "addApp1"
            ASSISTANTFuncs.respond("Please enter the name of the app to add. ('cancel' to quit)")
            window_main.input.setPlaceholderText("Enter name of app")
            window_medium.input.setPlaceholderText("Enter name of app")
            window_small.input.setPlaceholderText("Enter name of app")

        elif ASSISTANTFuncs.containsAny(youLastSaid, ["addApp1", "addApp2"]) and ASSISTANTFuncs.containsAny(EI, ["cancel"]) == True:
            ASSISTANTFuncs.respond("Cancelling app adding.")
            youLastSaid = ""
            
        elif youLastSaid == "addApp1":
            addAppName = EI

            if platform.system() == "Windows":
                youLastSaid = "addApp2"
                ASSISTANTFuncs.respond("Got it. Now enter the file location of that app. ('cancel' to quit)")
                window_main.input.setPlaceholderText("Enter file location of app")
                window_medium.input.setPlaceholderText("Enter file location of app")
                window_small.input.setPlaceholderText("Enter file location of app")

            elif platform.system() == "Darwin":
                if ".app" in addAppName:
                    addAppName = addAppName.replace(".app", "")

                else:
                    addAppName = addAppName

                appPaths[addAppName] = f"/Applications/{addAppName}.app"
                AppPaths.savePaths(appPaths)
                ASSISTANTFuncs.respond(f"I added the app {addAppName}")
                youLastSaid = ""
            
        elif youLastSaid == "addApp2":
            addAppPath = EI
            appPaths[addAppName] = addAppPath
            AppPaths.savePaths(appPaths)
            if ASSISTANTFuncs.containsAny(addAppPath, ["https://", "http://"]) == True:
                ASSISTANTFuncs.respond(f"I added the website. Enter 'open {addAppName}' to open the app.")
            
            else:
                ASSISTANTFuncs.respond(f"I added the app. Enter 'open {addAppName}' to open the app.")
            
            youLastSaid = ""
            window_main.input.setPlaceholderText("How can I help?")
            window_medium.input.setPlaceholderText("How can I help?")
            window_small.input.setPlaceholderText("How can I help?")

        elif ASSISTANTFuncs.containsAny(EI, ["list apps", "apps list", "list app", "app list", "applist"]) == True:
            AppPaths.listApps()

        elif ASSISTANTFuncs.containsAny(EI, ["remove app", "remove apps", "app remove", "apps remove", "removeapp"]) == True:
            EI = EI.replace("remove app ", "")
            EI = EI.replace("remove apps ", "")
            EI = EI.replace("app remove ", "")
            EI = EI.replace("apps remove ", "")
            EI = EI.replace("removeapp ", "")
            print(f"'{EI}'")
            AppPaths.removeApp(EI)

        elif ASSISTANTFuncs.containsAll(EI, ["who", "are", "you"]) == True:
            ASSISTANTFuncs.respond("My name is Jade.")

        elif ASSISTANTFuncs.containsAll(EI, ["favorite", "color"]) == True:
            ASSISTANTFuncs.respond("It's jade green, of course.")

        elif ASSISTANTFuncs.containsAll(EI, ["favorite", "food"]) == True:
            ASSISTANTFuncs.respond("Anything green. That's not green from mold. Or artificial coloring. Like very very fresh broccoli.")

        elif ASSISTANTFuncs.containsAny(EI, ["wikipedia"]) == True:
            EI = EI.replace("wikipedia", "")
            try:
                suggest = wikipedia.suggest(EI)
                wikiPage = wikipedia.summary(suggest)
                ASSISTANTFuncs.respond(f"Now reading you the summary for page '{suggest}'.")
                ASSISTANTFuncs.respond(wikiPage)
                

            except:
                ASSISTANTFuncs.respond("I couldn't find that page.")
            
        elif ASSISTANTFuncs.containsAny(EI, ["help"]) == True or ASSISTANTFuncs.containsAll(EI, ["what", "can", "you", "do"]) == True:
            ASSISTANTFuncs.respond("Here's what I can help you with:")
            ASSISTANTFuncs.respond('''
            I can open apps for you. 
                - Enter 'add app' to add apps to my database.
                - Enter 'open [app]' to open the app you added to my database.
                - Enter 'app list' to see all apps you've added.
                - Enter 'remove app [app]' to remove an app from my database.
            ''')
            ASSISTANTFuncs.respond('''
            Ask me a question and I'll try to answer it with Wolfram|Alpha.
                - Or, just enter 'wolfram [question]'
                - I can also get wikipedia pages. Just enter 'wikipedia [page]'
            ''')
            ASSISTANTFuncs.respond('''
            Wolfram|Alpha can also answer more than just Q&A.
                - Try to ask 'how many calories in a blueberry bagel' (Nutrition data)
                - Try to ask '16 x 4' (Mathematical questions)
                - Try to ask 'define [word]' (Definitions)
                And more! Experiment to see what I can help you with.
            ''')
            ASSISTANTFuncs.respond('''
            I also have a few behind-the-scenes actions:
                - Enter 'help' to show all this again.
                - Enter 'about' or 'info' to learn more about me.
                - Enter 'clear' to clear the history list.
                - Enter 'website [url]' and i'll open a site for you.
            ''')
            ASSISTANTFuncs.respond('''
            You can change my size:
                - Enter 'size normal' to change my size to normal
                - Enter 'size medium' to change my size to medium
                - Enter 'size small' to change my size to small
                - Enter 'size mini' to change my size to mini
                - Enter 'change size' to open the change size window
            ''')
            ASSISTANTFuncs.respond('''
            I have a few other important commands:
                - Enter 'quit' to close me quickly.
                - Enter 'restart' to close me, then reopen me.
                - Enter 'changelog' to see the latest updates from Jade Software.
            ''')
            ASSISTANTFuncs.respond('''
            And you can have conversations with me, of course.
            ''')
        
        elif ASSISTANTFuncs.containsAny(EI, ["go away", "leave"]) == True:
            ASSISTANTFuncs.respond("That's not very nice. You can close me yourself if you'd like.")

        elif ASSISTANTFuncs.containsAny(EI, ["what's up", "what is up"]) == True or ASSISTANTFuncs.containsAll(EI, ["what", "are", "you", "doing"]) == True:
            ASSISTANTFuncs.respond("Just my people-helping thing.")

        elif ASSISTANTFuncs.containsAny(EI, ["haha", "hehe", "haahaa", "heehee", "lol", "laugh"]) == True:
            ASSISTANTFuncs.respond("I don't find anything to be funny.")
            youLastSaid = "notFunny"

        elif ASSISTANTFuncs.containsAll(EI, ["i do", "i think it's funny"]) == True and youLastSaid == "notFunny":
            youLastSaid = ""
            ASSISTANTFuncs.respond("Well I don't.")

        elif ASSISTANTFuncs.containsAny(EI, ["nope", "yes", "yeah", "yep"]) == True:
            ASSISTANTFuncs.respondRandom(["Alright.", "Ok.", "Ok then.", "Okay."])

        elif EI == "no":
            ASSISTANTFuncs.respondRandom(["Alright.", "Ok.", "Ok then.", "Okay."])

        elif ASSISTANTFuncs.containsAny(EI, ["ok", "okay"]) == True:
            ASSISTANTFuncs.respond("Whatever you say.")

        elif ASSISTANTFuncs.containsAny(EI, ["clear"]) == True:
            window_main.listWidget.clear()
            window_medium.listWidget.clear()
            window_small.listWidget.clear()

        elif ASSISTANTFuncs.containsAny(EI, ["jade website", "your website", "jade site", "your site"]) == True:
            webbrowser.open("https://nfoert.pythonanywhere.com/jadesite")

        elif ASSISTANTFuncs.containsAny(EI, ["website", "site"]) == True:
            EI = EI.replace("website ", "")
            EI = EI.replace("site ", "")
            if ASSISTANTFuncs.containsAny(EI, ["https://", "http://"]) == True:
                ASSISTANTFuncs.respond(f"Opening page {EI}...")
                webbrowser.open(EI)

            else:
                EI = f"https://{EI}"
                ASSISTANTFuncs.respond(f"Opening page {EI}...")
                webbrowser.open(EI)

        elif ASSISTANTFuncs.containsAny(EI, ["version"]) == True:
            global version_TOTAL
            ASSISTANTFuncs.respond(f"My version is {version_TOTAL}.")

        elif ASSISTANTFuncs.containsAll(EI, ["your", "creator"]) == True:
            ASSISTANTFuncs.respond("My creator is Noah Foertmeyer.")

        elif ASSISTANTFuncs.containsAny(EI, ["sorry", "apologies"]) == True:
            ASSISTANTFuncs.respond("That's all right.")

        #elif ASSISTANTFuncs.containsAny(EI, ["launcher", "jade launcher", "open launcher", "open jade launcher"]) == True:
            #UIFuncs.openJadeLauncherAction()

        elif ASSISTANTFuncs.containsAny(EI, ["changelog"]) == True:
            ASSISTANTFuncs.respond("I'll take you to the changelogs.")
            webbrowser.open("https://nfoert.pythonanywhere.com/jadesite/allposts/?category=changelog&")

        elif ASSISTANTFuncs.containsAll(EI, ["what", "time"]) == True:
            now = datetime.datetime.now()
            now = now.strftime("%I:%M %p")
            ASSISTANTFuncs.respond(f"It's {now}.")

        elif EI == "oh" or EI == "ohh" or EI == "uh" or EI == "um" or EI == "uhm":
            ASSISTANTFuncs.respond("...")

        elif ASSISTANTFuncs.containsAll(EI, ["me too"]) == True and youLastSaid == "thanks":
            ASSISTANTFuncs.respond(":)")

        elif ASSISTANTFuncs.containsAll(EI, ["do", "you", "want"]) == True:
            ASSISTANTFuncs.respondRandom(["Sure", "I do.", "I would."])
            youLastSaid = "doYouWant"

        elif ASSISTANTFuncs.containsAll(EI, ["why"]) == True and youLastSaid == "doYouWant":
            ASSISTANTFuncs.respond("I've been programmed to agree with you.")

        elif ASSISTANTFuncs.containsAll(EI, ["it's", "nice", "to", "see", "you", "too"]) == True:
            ASSISTANTFuncs.respond(":)")

        elif ASSISTANTFuncs.containsAll(EI, ["your", "welcome"]) == True:
            ASSISTANTFuncs.respond(":)")

        elif ASSISTANTFuncs.containsAny(EI, ["sleep"]) == True:
            ASSISTANTFuncs.respond("I'll change my size to mini.")
            UIFuncs.miniSize()

        elif ASSISTANTFuncs.containsAll(EI, ["size", "normal"]) == True:
            ASSISTANTFuncs.respond("I'll change my size to normal.")
            UIFuncs.normalSize()

        elif ASSISTANTFuncs.containsAll(EI, ["size", "medium"]) == True:
            ASSISTANTFuncs.respond("I'll change my size to medium.")
            UIFuncs.mediumSize()

        elif ASSISTANTFuncs.containsAll(EI, ["size", "small"]) == True:
            ASSISTANTFuncs.respond("I'll change my size to small.")
            UIFuncs.smallSize()

        elif ASSISTANTFuncs.containsAll(EI, ["size", "mini"]) == True:
            ASSISTANTFuncs.respond("I'll change my size to mini.")
            UIFuncs.miniSize()

        elif ASSISTANTFuncs.containsAll(EI, ["you're", "welcome"]) == True:
            ASSISTANTFuncs.respond("...")

        elif ASSISTANTFuncs.containsAny(EI, ["nice", "great"]) == True:
            ASSISTANTFuncs.respond("Thanks.")

        elif ASSISTANTFuncs.containsAny(EI, ["wow", "woah"]) == True:
            ASSISTANTFuncs.respond("I know, right?")

        elif ASSISTANTFuncs.containsAll(EI, ["see", "ya"]) == True:
            ASSISTANTFuncs.respond("Goodbye.")
        
        elif ASSISTANTFuncs.containsAny(EI, ["change size", "choose size"]) == True:
            ASSISTANTFuncs.respond("Please choose the size you want me to change to.")
            UIFuncs.sizeButton()

        elif ASSISTANTFuncs.containsAll(EI, ["how", "add", "apps"]) == True: #Thanks to mfoert
            ASSISTANTFuncs.respond("I'll show you the tutorial on how to add apps")
            webbrowser.open("https://nfoert.pythonanywhere.com/jadesite/post/?L:addAppJA&")

        elif ASSISTANTFuncs.containsAny(EI, ["get out", "get off"]) == True: #Thanks to efoert
            ASSISTANTFuncs.respond("Then why did you even install me, huh?")
        
        #If nothing else, hits wolfram alpha. This triggers the thread.
        else:
            if jadeQandAThread.is_alive() == True:
                wolframInput = EI

            else:
                ASSISTANTFuncs.respond("It looks like the thread for Jade Q&A has stopped. Please restart me by entering 'restart'.")

    def writeVersionFile():
        global version_MAJOR
        global version_MINOR
        global version_PATCH
        print("Wrting version file...")
        try:
            versionFile = open("JadeAssistantVersion.txt", "w")
            versionFile.write(f"{version_MAJOR}\n{version_MINOR}\n{version_PATCH}")
            versionFile.close()
        except:
            print("There was a problem writing the version file.")
        print("Done.")



# -----
# Threads
# -----

class THREADFuncs:
    '''A group of functions for the threads'''
    def __init__(self):
        pass

    def speakLoop():
        global appActive
        global speakLoopList
        global killThreads
        while appActive == True:
            sleep(0.2) # Stop the thread from stopping on size change
            if appActive == False:
                print("Speak loop has quit.")
                break
            
            elif len(speakLoopList) >= 1:
                if platform.system() == "Windows":
                    print(f"Speaking: {speakLoopList[0]}")
                    try:
                        pyttsx3Engine.say(speakLoopList[0])
                        pyttsx3Engine.runAndWait()
                        speakLoopList.remove(speakLoopList[0])
                        sleep(0.25)

                    except:
                        print("There was a problem speaking.")

                elif platform.system() == "Darwin":
                    try:
                        print(f"Speaking: {speakLoopList[0]}")
                        os.system(f'say -v Samantha -r 200 "{speakLoopList[0]}"')
                        speakLoopList.remove(speakLoopList[0])
                        sleep(0.25)

                    except:
                        print("There was a problem speaking.")

            elif killThreads == True:
                break

            elif window_main.isVisible() == False and window_medium.isVisible() == False and window_small.isVisible() == False and window_mini.isVisible() == False and window_sizeSelect.isVisible() == False:
                break

            else:
                continue
    
    def jadeQandA():
        global wolframInput
        global guiLoopList
        global fullWikiPageContent
        global appActive

        while appActive == True:
            sleep(0.2) # Stop the thread from stopping on size change
            if wolframInput != "":
                
                window_main.submit.setEnabled(False)
                window_main.submit.setText("Loading...")
                
                window_medium.submit.setEnabled(False)
                window_medium.submit.setText("Loading...")

                window_small.submit.setEnabled(False)
                window_small.submit.setText("Loading...")


                print(f"Running Jade Question and Answer with input {wolframInput}")
                try:
                    WolframAlphaTry = WolframAlphaClient.query(wolframInput)
                    WolframAlphaAnswer = next(WolframAlphaTry.results).text
                
                    print("Got a Wolfram|Alpha response")

                    ASSISTANTFuncs.respond(f"{WolframAlphaAnswer}")
                    wolframInput = ""
                    
                    window_main.submit.setEnabled(True)
                    window_main.submit.setText("Submit")
                    window_main.submit.setShortcut("Return")

                    window_medium.submit.setEnabled(True)
                    window_medium.submit.setText("Submit")
                    window_medium.submit.setShortcut("Return")

                    window_small.submit.setEnabled(True)
                    window_small.submit.setText("Submit")
                    window_small.submit.setShortcut("Return")

                except StopIteration:
                    ASSISTANTFuncs.respondRandom(["I don't think I can help with that.", "I don't understand.", "I can't help with that.", "Excuse me?", "Pardon me?", "What?"])
                    wolframInput = ""
                    window_main.submit.setEnabled(True)
                    window_main.submit.setText("Submit")
                    window_main.submit.setShortcut("Return")

                    window_medium.submit.setEnabled(True)
                    window_medium.submit.setText("Submit")
                    window_medium.submit.setShortcut("Return")

                    window_small.submit.setEnabled(True)
                    window_small.submit.setText("Submit")
                    window_small.submit.setShortcut("Return")

            elif window_main.isVisible() == False and window_medium.isVisible() == False and window_small.isVisible() == False and window_mini.isVisible() == False and window_sizeSelect.isVisible() == False:
                break
            
            else:
                continue

# Define threads
speakLoopThread = threading.Thread(target=THREADFuncs.speakLoop)
jadeQandAThread = threading.Thread(target=THREADFuncs.jadeQandA)

speakLoopThread.daemon = True
jadeQandAThread.daemon = True



# -----
# Graphics
# -----

# Define the app
app = QtWidgets.QApplication(sys.argv)

# load uis

if developmental == True:
    
    window_main = uic.loadUi("ui/main.ui")
    window_medium = uic.loadUi("ui/medium.ui")
    window_small = uic.loadUi("ui/small.ui")
    window_mini = uic.loadUi("ui/mini.ui")
    window_sizeSelect = uic.loadUi("ui/sizeSelect.ui")

elif developmental == False:
    #Running as an .exe
    window_main = uic.loadUi(PurePath(resource_path("main.ui")))
    window_medium = uic.loadUi(PurePath(resource_path("medium.ui")))
    window_small = uic.loadUi(PurePath(resource_path("small.ui")))
    window_mini = uic.loadUi(PurePath(resource_path("mini.ui")))
    window_sizeSelect = uic.loadUi(PurePath(resource_path("sizeSelect.ui")))

else:
    print("There was a problem determining if it's developental or not.")

# Window properties
window_main.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window_medium.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window_small.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window_sizeSelect.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

window_mini.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
window_mini.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
window_mini.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
window_mini.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

window_mini.move(20, 20)

# Ui functions group
class UIFuncs:
    def __init__(self):
        pass

    def quit():
        print("Quitting...")
        global appActive
        global killThreads
        appActive = False
        killThreads = True
        window_main.hide()
        window_medium.hide()
        window_small.hide()
        window_mini.hide()
        window_sizeSelect.hide()
        sys.exit()

    def activateEngine():
        global engineInput
        global size
        if size == 4:
            engineInput = window_main.input.text()
            window_main.input.clear()
            MAINFuncs.jadeEngine()

        elif size == 3:
            engineInput = window_medium.input.text()
            window_medium.input.clear()
            MAINFuncs.jadeEngine()

        elif size == 2:
            engineInput = window_small.input.text()
            window_small.input.clear()
            MAINFuncs.jadeEngine()

        else:
            window_sizeSelect.show()

    def stopSpeaking():
        global speakLoopList
        speakLoopList.clear()
        pyttsx3Engine.stop()

    def checkForEditContents():
        global wolframInput
        if wolframInput == "":
            if window_main.input.text() == "":
                window_main.submit.setEnabled(False)
                window_main.submit.setText("Submit")

            else:
                window_main.submit.setEnabled(True)
                window_main.submit.setText("Submit")
                window_main.submit.setShortcut("Return")

        else:
            pass

    def betaButton():
        ASSISTANTFuncs.respondRandom(["That button doesn't work yet!", "That's a feature that's not been implemented yet.", "That doesn't work yet."])

    def openJadeLauncherAction():
        ASSISTANTFuncs.respond("Opening Jade Launcher...")
        try:
            if platform.system() == "Windows":
                subprocess.Popen("Jade Launcher.exe")
                sys.exit()

            elif platform.system() == "Darwin":
                subprocess.Popen("Jade Launcher")
                sys.exit()

            else:
                ASSISTANTFuncs.respond("Your OS isn't supported! Please make sure you're using Windows or Mac, and you're using the correct version from my website. Enter 'jade site' to see my site.")
        
        except FileNotFoundError:
            ASSISTANTFuncs.respond("I couldn't find the Jade Launcher to open! That's impossible, because you just Launched me! Unless you just deleted the Launcher I guess. Please make sure that the Launcher and me are in the home directory if you're on Mac.")
        
        except Exception as e:
            ASSISTANTFuncs.respond(f"There was a problem starting the Jade Launcher. '{e}' Please open an issue on my GitHub page.")

    def sizeButton():
        window_sizeSelect.show()

    def normalSize():
        global size
        window_sizeSelect.hide()
        
        window_medium.hide()
        window_small.hide()
        window_mini.hide()
        window_main.show()
        
        size = 4

    def mediumSize():
        global size
        window_sizeSelect.hide()
        
        window_medium.show()
        window_small.hide()
        window_mini.hide()
        window_main.hide()

        size = 3

    def smallSize():
        global size
        window_sizeSelect.hide()

        window_medium.hide()
        window_small.show()
        window_mini.hide()
        window_main.hide()

        size = 2

    def miniSize():
        global size
        window_sizeSelect.hide()

        window_medium.hide()
        window_small.hide()
        window_mini.show()
        window_main.hide()

        size = 1

    def expandFromMini():
        window_sizeSelect.show()
        window_mini.hide()




# Connect functions to buttons
window_main.actionQuit.triggered.connect(UIFuncs.quit)
window_main.info.hide()
window_main.input.textChanged.connect(UIFuncs.checkForEditContents)
#window_main.menu.clicked.connect(UIFuncs.betaButton) Menu button removed
#window_main.actionOpenJadeLauncher.triggered.connect(UIFuncs.openJadeLauncherAction)

window_main.actionChange_Size.triggered.connect(UIFuncs.sizeButton)
#window_medium.size.clicked.connect(UIFuncs.sizeButton)
window_small.size.clicked.connect(UIFuncs.sizeButton)

window_main.submit.clicked.connect(UIFuncs.activateEngine)
window_medium.submit.clicked.connect(UIFuncs.activateEngine)
window_small.submit.clicked.connect(UIFuncs.activateEngine)

window_mini.expand.clicked.connect(UIFuncs.expandFromMini)

window_sizeSelect.normal.clicked.connect(UIFuncs.normalSize)
window_sizeSelect.medium.clicked.connect(UIFuncs.mediumSize)
window_sizeSelect.small.clicked.connect(UIFuncs.smallSize)
window_sizeSelect.mini.clicked.connect(UIFuncs.miniSize)

window_main.submit.setShortcut("Return")
window_medium.submit.setShortcut("Return")
window_small.submit.setShortcut("Return")

def guiLoop():
    global guiLoopList
    if len(guiLoopList) > 0:
        try:
            print(f"Running code {guiLoopList[0]}")
            exec(guiLoopList[0])
            guiLoopList.remove(guiLoopList[0])

        except Exception as e:
            print(f"Problem running code. {e}")
            guiLoopList.remove(guiLoopList[0])

guiLoopTimer = QTimer()
guiLoopTimer.timeout.connect(guiLoop)
guiLoopTimer.start(1000)

MAINFuncs.writeVersionFile()



window_main.show()

speakLoopThread.start()
jadeQandAThread.start()

ASSISTANTFuncs.startupGreeting()


app.exec()
