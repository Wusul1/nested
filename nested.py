from tkinter import *
import random
import os
#implement LLM-ENGINE (first for thoughts etc, then for the whole game)
use_ai_engine=False
prompt='User: What is contained in "Earth"? AI: Earth->Continents*7,Sea*5. User: What is contained in "Small Magdellanic Cloud" AI: Small Magdellanic Cloud-> Central Black Hole, Star Region*40, Nebula*4 User: What is contained in Firefighter Ai: '
#implement merging thingfiles
#implement merge confilcts
#implement error message when no thing files have been found
def load(things_file):
    inthings = [[], []]

    # Datei öffnen und Zeilen einlesen
    with open(things_file, "r") as file:
        lines = file.readlines()

    # Zeilenumbrüche entfernen
    lines = [line.strip() for line in lines]

    # Durch jede Zeile gehen
    for line in lines:
        sections_1 = line.split("!")
        inthings[0].append(sections_1[0])
        inthings[1].append([])

        for sections_2 in sections_1[1].split(","):
            section_2_list = sections_2.split(".")
            inthings[1][-1].append(section_2_list)

    return inthings

def searchdirs(dirs):
    thingfiles=[]
    for dir in dirs:
        try:
            files = os.listdir(dir)
        except:
            continue
        #search for valid thingfiles by trying to load them, add them to valid_files if succesfull
        valid_files=[]
        for file in files:
            try:
                load(dir+"/"+file)
                valid_files.append(file)
            except:
                pass
        thingfiles.extend(valid_files)
    return thingfiles

thing_file_dirs=["thingfiles"]#directories that are searched for thingfiles
things_files_list = searchdirs(thing_file_dirs)#If there is more than one thingfile in here, the user should be able to select which one to use, unimplemented
print(things_files_list)
if len(things_files_list)==1: things_file=things_files_list[0]
#dinge aus der oben angegebenen datei laden


# Funktion zum Öffnen eines Elements
def openThing(thing, inthings):
    global things
    global historie

    # Historie aktualisieren
    historie.append(things)

    # Index des ausgewählten Elements finden
    num = inthings[0].index(thing)
    elements = []

    # Durch die Unterabschnitte des Elements gehen
    for inthing_2 in inthings[1][num]:
        ranNum = random.randint(1, 100)

        if ranNum > 100 - int(inthing_2[1]):
            if inthing_2[2] == inthing_2[3]:
                anzahl = int(inthing_2[2])
            else:
                anzahl = random.randint(int(inthing_2[2]), int(inthing_2[3]))

            while anzahl > 0:
                if inthing_2[4] == "n":
                    if check_a(elements, inthing_2[5]):
                        elements.append(inthing_2[0])
                        anzahl -= 1
                    else:
                        break
                else:
                    exists_2 = all(element in elements for element in inthing_2[4].split("/"))
                    if exists_2:
                        if check_a(elements, inthing_2[5]):
                            elements.append(inthing_2[0])
                            anzahl -= 1
                        else:
                            break
                    else:
                        break

    things = elements
    showRootWindow()

# Funktion zum Überprüfen, ob Elemente in der Liste vorhanden sind
def check_a(elements_, toCheck):
    if toCheck == "n":
        return True
    else:
        for thing___ in toCheck.split("/"):
            if thing___ not in elements_:
                return False
        return True

# Funktion zum Zurückkehren zur vorherigen Ansicht
def back():
    global things
    global historie
    things = historie.pop()
    showRootWindow()

# Funktion zum Überprüfen, ob ein Element existiert
def check(thing):
    global inthings
    return thing in inthings[0]

# Funktion zum Anzeigen des Hauptfensters
def showRootWindow():
    global root
    global things
    global elements_tk
    global inthings
    global historie

    clearElements()
    buttons = []

    for thing in things:
        if check(thing):
            buttons.append(Button(root, text=thing, command=lambda t=thing: openThing(t, inthings)))
        else:
            buttons.append(Button(root, text=thing, state=DISABLED))

    gridPosR = -1
    gridPosC = 0
    backButtonPos = 0
    updateBackButtonPos = True

    for button in buttons:
        if updateBackButtonPos:
            backButtonPos += 1

        elements_tk.append(button)
        gridPosR += 1
        button.grid(row=gridPosR, column=gridPosC)

        if gridPosR == 20:
            updateBackButtonPos = False
            gridPosC += 1
            gridPosR = -1

    if len(historie) > 0:
        backButton = Button(root, text="Zurück", command=back, bg="#f55f5f")
    else:
        backButton = Button(root, text="Zurück", state=DISABLED)

    backButton.grid(row=backButtonPos, column=0)
    elements_tk.append(backButton)

# Funktion zum Entfernen aller GUI-Elemente
def clearElements():
    global elements_tk
    for element in elements_tk:
        element.destroy()

elements_tk = []
historie = []
inthings = load(thingsfile)
things = ["SMC"]
historie = []

root = Tk()
showRootWindow()
root.mainloop()

