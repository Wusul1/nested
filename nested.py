from tkinter import * 
import random
def load():
    inthings = [[],[]]
    #datei öffnen und alle zeilen einlesen
    lines_n = open("things.txt","r").readlines()
    #zeilen absatz entfernen
    lines = []
    for line_n in lines_n:
        lines.append(line_n.rstrip("\n"))
    #jedes große elements durchgehen
    for line in lines:
        sections_1 = line.split("!")
        inthings[0].append(sections_1[0])
        inthings[1].append([])
        for sections_2 in sections_1[1].split(","):
            section_2_list = []
            for section_3 in sections_2.split("."):
                section_2_list.append(section_3)
            inthings[1][len(inthings[1])-1].append(section_2_list)
    return inthings
def openThing(thing,inthings):
    global inthing_2
    global things
    global historie
    historie.append(things)
    num = -1
    for inthing in inthings[0]:
        num=num+1
        if inthing == thing:
            break
    elements = []
    for inthing_2 in inthings[1][num]:
            ranNum = random.randint(1,100)
            if ranNum>100-int(inthing_2[1]):
                if inthing_2[2] == inthing_2[3]:
                 anzahl = int(inthing_2[2])
                else:
                 anzahl = random.randint(int(inthing_2[2]),int(inthing_2[3]))
                while anzahl>0:
                    if inthing_2[4] == "n":
                        if check_a(elements,inthing_2[5]) == True:
                           elements.append(inthing_2[0])
                           anzahl = anzahl-1
                        else:
                            break
                    else:
                        exists_2 = False
                        for thing___ in inthing_2[4].split("/"):
                            exists_2 = False
                            for element in elements:
                                if thing___ == element:
                                    exists_2 = True
                            if exists_2 == False:
                               break
                        if exists_2:
                            if check_a(elements,inthing_2[5]):
                                elements.append(inthing_2[0])
                                anzahl = anzahl-1
                            else:
                                break
                        else:
                            break
    things = elements
    showRootWindow()
def check_a(elements_,toCheck):
                            if toCheck == "n":
                                return True
                            else:
                                for thing___ in toCheck.split("/"):
                                    exists_3 = True
                                    for element in elements_:
                                        if element == thing___:
                                            exists_3 = False
                                    if exists_3 == False:
                                        break
                                if exists_3:
                                    return True
                                else:
                                    return False
def back():
    global things
    global historie
    things = historie[len(historie)-1]
    del historie[len(historie)-1]
    showRootWindow()
def check(thing):
    global inthings
    exist = False
    for inthing in inthings[0]:
        if thing == inthing:
            exist = True
    return exist
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
         exec("buttons.append(Button(root,text=thing,command=lambda: openThing(\""+thing+"\",inthings)))")
        else:
         buttons.append(Button(root,text=thing,state=DISABLED))
    gridPosR = -1
    gridPosC = 0
    backButtonPos = 0
    updateBackButtonPos = True
    for button in buttons:
        if updateBackButtonPos:
            backButtonPos = backButtonPos+1
        elements_tk.append(button)
        gridPosR=gridPosR+1
        button.grid(row=gridPosR,column=gridPosC)
        if gridPosR == 20:
            updateBackButtonPos = False
            gridPosC = gridPosC+1
            gridPosR = -1
    if len(historie) >0:
     backButton = Button(root,text="Zurück",command=back,bg="#f55f5f")
    else:
        backButton=Button(root,text="Zurück",state=DISABLED)
    backButton.grid(row=backButtonPos,column=0)
    elements_tk.append(backButton)
def clearElements():
    global elements_tk
    for element in elements_tk:
        element.destroy()
elements_tk = []
historie = []
inthings = load()
things = ["Raumschiff"]
historie = []
root = Tk()
showRootWindow()
root.mainloop()
