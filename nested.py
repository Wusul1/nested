import tkinter as tk
import copy
from random import randint
#todo: remove fix in ThingContent
#move stuff to ThingFileEngine (like LLM ENGInE)
#add dependencies/noncooexistence with other elements
#add thingfile selector
#add merging thingfiles
#add thingfiles specifing root, let the use select which thingfiles root to use
#add pagination for many things
#make the whole thing procedural instead of random
#make option to use LLM to generate contents
class ThingContent():
    def __init__(self, name, percentage, min, max, needs_to_exist, cant_exist):
        self.name = name
        self.percentage = int(percentage)
        self.min = int(min)
        if max=="n": #fix
            max=1
        self.max = int(max)
        self.needs_to_exist = needs_to_exist
        self.cant_exist = cant_exist
class Thing():
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents
class ThingFile():
    def __init__(self, filename):
        self.filename = filename
        self.things_in_file = self.load()
    def return_thing_by_name(self,thingname):
        for thing in self.things_in_file:
            if thing.name == thingname:
                return thing
    def exists_in_thingfile(self,thingname):
        for thing in self.things_in_file:
            if thing.name == thingname:
                return True
        return False
    def load(self):
        things_in_file = []#list an dingen, die es gibt, wird aus textdatei geladen
        lines = open(self.filename, "r", encoding="utf-8").readlines()
        lines = [line.strip() for line in lines] #leerzeichen vor und nach zeilen von thingsdatei entfernen
        for line in lines:
            sections=line.split("!")#splitted zeile in ihre zwei sektionen (ding:inhalt)
            thing=Thing(sections[0], self.content_string_to_content_list(sections[1]))#create new thing object
            things_in_file.append(thing)
        return things_in_file
    #converts the content string (the things after the ! in each line of the thingfile) into a list of ThingContent
    def content_string_to_content_list(self, content_string):
        thing_contents=[]
        content_string_parts = content_string.split(",")#, sperates the different content things of a thing in the thingsfile
        for content_string_part in content_string_parts:
            content_string_part_attributes=content_string_part.split(".")#liste der attribute eines thing_contents
            for i in range(4,6):
                try:
                    if content_string_part_attributes[i]=="n":
                        content_string_part_attributes[i]=[]
                    else:
                        content_string_part_attributes[i]=content_string_part_attributes[i].split("/")
                except:
                    content_string_part_attributes.append([])
            if len(content_string_part_attributes)<6:
                continue
            else:
                thing_content = ThingContent(*content_string_part_attributes)
                thing_contents.append(thing_content)
        return thing_contents
            
class HistoryManager():
    def __init__(self):
        self.history_holder=[]
    def get_history_count(self):
        return len(self.history_holder)
    def return_and_delete_latest(self):
        latest = self.history_holder[-1]
        del self.history_holder[-1]
        return latest
    def add_to_historie(self, state):
        self.history_holder.append(copy.deepcopy(state))#make sure changing state will never change it's value in history_holder
class NestedApp:
    def __init__(self, root, startthings, thingfilename):
        self.root = root
        self.things = startthings #die dinge die gerade angezeigt werden
        self.historiemanager = HistoryManager()
        self.thingfile = ThingFile(thingfilename)
        self.show_window()
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def back(self):
        self.things = self.historiemanager.return_and_delete_latest()
        self.show_window()
    def show_window(self):
        self.clear_window()
        buttons_to_place=[]
        for thing in self.things:
            if self.thingfile.exists_in_thingfile(thing):
                buttons_to_place.append(tk.Button(self.root, text=thing, command=lambda: self.open_thing(thing)))
            else:
                buttons_to_place.append(tk.Button(self.root, text=thing, state="disabled"))
        grid_position_row = -1
        grid_position_column = 0
        back_button_row = 0
        update_back_button_position = True
        for button in buttons_to_place:
            if update_back_button_position:
                back_button_row+=1
            grid_position_row+=1
            button.grid(row=grid_position_row, column=grid_position_column)
            
            if grid_position_row==20:
                grid_position_column+=1
                grid_position_row=-1
                update_back_button_position = False
        if self.historiemanager.get_history_count() < 1:
            back_button = tk.Button(self.root, text="Zurück", state="disabled")
        else:
            back_button = tk.Button(self.root, text="Zurück", command=self.back, bg="#f55f5f")
        back_button.grid(row=back_button_row, column=0)
    def check_requirements(needs_to_exist,cant_exist):
        needs_to_exist_met=True
        cant_exist_met=True
        for requirement in needs_to_exist:
            if requirement not in self.things:
                needs_to_exist_met=False
                break
        for requirement in cant_exist:
            if requirement in self.things:
                cant_exist_met=False
                break
        if needs_to_exist_met and cant_exist_met:
            return True
        else:
            return False
    def open_thing(self,thingname):
        self.historiemanager.add_to_historie(self.things)
        self.things=[]
        thing_to_open = self.thingfile.return_thing_by_name(thingname)
        for content in thing_to_open.contents:
            random_number=randint(1,100)
            if random_number>100-content.percentage:
                if content.min == content.max:
                    count_of_thing = content.min
                else:
                    count_of_thing = randint(content.min,content.max)
                if check_requirements(content.needs_to_exist, content.cant_exist):
                    for i in range(1,count_of_thing+1):
                        self.things.append(content.name)
        self.show_window()
def main():
    root = tk.Tk()
    app = NestedApp(root,["Raumschiff"],"things_raumschiff.txt")
    root.mainloop()
    
if __name__ == "__main__":
    main()
