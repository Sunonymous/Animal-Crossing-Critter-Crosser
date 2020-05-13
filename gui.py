# Animal Crossing
# Critter Crosser
# GUI Framework

# To Do:
# Declutter Legacy Functions
# Separate the pickle generation into its own file. It is not necessary to have it here.
# Clean up code.

# Necessary Imports and Shorthands
import pickle as pk
import PySimpleGUI as sg
from datetime import datetime
import webbrowser, os.path
import printer as pr
import analyzer as anal
import table as tb
import logging as lg

#Logging
lg.basicConfig(filename='Log.txt', level=lg.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class State:
    # Class for containing state variables of the program.
    def __init__(self):
        self.active = True                  #State of program
        self.mode = False          #False - Fish, True - Bugs
        self.month = datetime.now().month #Set to current month
        self.hemisphere = False    #False - Northern, True - Southern
        self.access = False         # Access to both hemispheres
        self.modifier = 0           # Variable to modify anal.present_in_month function
        self.fish_props, self.bugs_props = tb.generate_property_dictionaries()
        self.sort_by = "NAME"
        # Create data lists
        self.fish = anal.create_list("data\\fish.csv")
        self.bugs = anal.create_list("data\\bugs.csv")
        self.fishcss = ""
        self.bugscss = ""
        self.compcss = ""
        self.chartfilename = ""
        self.completionfilename = ""
        self.comp_mode = False
        # Generate empty container lists for use later.
        self.comp_master, self.comp_caught, self.comp_results = [], [], []

    # This is the only lambda accessed outside of this module.
    crit_mode = lambda self, x: self.fish if x == False else self.bugs

# Color theme for Program
sg.theme('LightYellow')
sg.theme_background_color('#c3d0f3') #c3d0f3
sg.theme_text_color('#FFBB00') #facf50
sg.theme_text_element_background_color('#ad723b') #ad723b
sg.theme_element_background_color('#ad723b') #af783f
sg.theme_element_text_color('#FFBB00') #facf50
sg.theme_slider_color('#e8eef6')
sg.theme_input_background_color('#FFBB00') #faf1a2
sg.theme_input_text_color('#FFFFFF') #9a6e0b
sg.theme_button_color(('#776650', '#faf1a2')) #('#776650', '#faf1a2')

### FUNCTIONS
# Simple function to toggle a boolean
def toggle(bool):
    return not bool

# Lambdas for showing statuses and choosing mode
hem = lambda x: "Southern" if x == True else "Northern"
crit = lambda x: "Fish" if x == False else "Bugs"
month_names = pr.month_names

def bootup():
    """Bootup function is supposed to speed up boot time. Instead of generating
    lists and dictionaries on runtime, they are pre-compiled and saved as a pickle."""
    # Save program into pickle object
    if os.path.isfile("data\\data.pickle"):
        with open("data\\data.pickle", 'rb') as pickle_file:
            program = pk.load(pickle_file)
    else:
        # Create program class state
        program = State()
        # Create CSS Text
        with open("stylefish.css", 'r') as infile:
            program.fishcss = infile.read()
        with open("stylebugs.css", 'r') as infile:
            program.bugscss = infile.read()
        pik_open = open("data\\data.pickle","wb")
        pk.dump(program, pik_open)
        pik_open.close()
    return program

# Generating State Object
program = bootup()

### GUI ###
# Global Options Layout
global_op_layout = [ [sg.Text('Select Month', size=(30, 1), justification='center', pad=((95,0),(20, 0)))],
[sg.Slider(range=(1, 12), orientation='h', size=(33, 20), default_value=datetime.now().month, key="selectmonth")],
[sg.Text('Main Hemisphere:', pad=((0,0),(20, 0))), sg.InputOptionMenu(('Northern', 'Southern'), size=(15, 1), pad=((76,0),(20, 0)), key="selecthemisphere")],
[sg.Text('Access to Both Hemispheres?:', pad=((0,0),(5, 5))), sg.InputOptionMenu(('Yes', 'No'), size=(15, 1), default_value="No", pad=((0,0),(5, 5)), key="selectaccess")], ]

generate_chart_layout = [ [sg.Text('Select Critters to View'), sg.Text('Sort By', pad=((188,0),(0, 0)))],
[sg.InputOptionMenu(('All Critters (Ignore Global Settings)', 'Critters New to This Month', 'This Month\'s Critters', 'Critters Disappearing Next Month'), key="viewcritsby"), sg.InputOptionMenu(("Name", "Price", "Location", "Time"), key="sortby", pad=((28,0),(0, 0)))],
[sg.Text("Filename:"), sg.InputText("Critter_Chart", size=(25, 1), key="selectchartfilename"), sg.Button(button_text='Generate', size=(20,2), target=(None, None))] ]

generate_completion_layout = [ [sg.Text("Create a chart with instructions to catch remaining critters.")],
[sg.Text("Filename:"), sg.InputText("Completion_Chart", size=(25, 1), key="selectcompletionfilename"), sg.Button(button_text="Make Completion List", key="completion", size=(20,2), pad=((10,0),(0, 0)), target=(None, None))] ]

# Program Layout
layout = [ [sg.Text('Animal Crossing Critter Crosser', size=(27, 1), justification='left', font=("Verdana 20 underline"), pad=((25,0),(0, 0)))],
           [sg.Text('1. Choose Critters to View:', pad=((5,0),(5, 5))), sg.InputOptionMenu(('Fish', 'Bugs'), size=(15, 1), pad=((38,0),(5, 5)), key="selectcritters"), sg.Button("Help", pad=((73,0),(5, 5)) )],
           [sg.Frame(layout=global_op_layout, title='2. Global Settings',title_color='#facf50', relief=sg.RELIEF_GROOVE, tooltip='Select the month to view, location, and access to hemispheres (for completion guides).')],
           [sg.Frame(layout=generate_chart_layout, title='3a. Chart Settings',title_color='#facf50', relief=sg.RELIEF_GROOVE, tooltip='Set your options for creating a chart.')],
           [sg.Frame(layout=generate_completion_layout, title='3b. Completion Chart',title_color='#facf50', relief=sg.RELIEF_GROOVE, pad=((0,0),(0, 15)))]
           ]

bigger_box = [ [sg.Frame(layout=layout, title="", relief=sg.RELIEF_GROOVE, pad=((5,5),(10, 10)))] ]

# Create a Window
window = sg.Window('Main Menu', bigger_box)

# Variables to Note State of Completion Window
completion_window_active = False
completion_window_mode = False #0-unchecked 1-checked

# Making Completion Layout
def gen_completion_checklist(obj, completion_window_mode):
    # Pass the state object
    # Make full list of names
    critter_list = [crit[0] for crit in obj.crit_mode(obj.mode)]
    # Make empty lists to hold results
    completion_boxes, columns = [], []
    # Append Critters
    for critter in range(len(critter_list)):
        if not completion_window_mode:
            completion_boxes.append([sg.Checkbox(f"{obj.crit_mode(obj.mode)[critter][0]}", default=False, key=obj.crit_mode(obj.mode)[critter][0])])
        else:
            completion_boxes.append([sg.Checkbox(f"{obj.crit_mode(obj.mode)[critter][0]}", default=True, key=obj.crit_mode(obj.mode)[critter][0])])
    one = completion_boxes[:20]
    two = completion_boxes[20:40]
    three = completion_boxes[40:60]
    four = completion_boxes[60:80]
    # Stitch it Together
    all = [ [sg.Text("Check the boxes for the critters you have already caught.")],
            [sg.Column(layout=one), sg.Column(layout=two), sg.Column(layout=three), sg.Column(layout=four)],
            [sg.Button("Select All"), sg.Button("Deselect All"), sg.Button("Create Chart"), sg.Button("Cancel")] ]
    return all

def generate(values, comp_mode=False):
    #Function
    if not comp_mode:
        assign_selections(values)
    else: #completion function
        assign_selections(values, True)

def assign_selections(dict, comp_mode=False):
    # Function to assign the program variables into the program object.
    #Month
    program.month = int(dict["selectmonth"])
    #Bug/Fish
    if dict["selectcritters"] == 'Fish':
        program.mode = False
    if dict["selectcritters"] == 'Bugs':
        program.mode = True
    #Hemisphere
    if dict["selecthemisphere"] == 'Northern':
        # Check to see the current hemisphere and convert if necessary.
        if program.hemisphere == True:
            program.fish = anal.convert_hemisphere(program.fish)
            program.bugs = anal.convert_hemisphere(program.bugs)
        program.hemisphere = False
    if dict["selecthemisphere"] == 'Southern':
        if program.hemisphere == False:
            program.fish = anal.convert_hemisphere(program.fish)
            program.bugs = anal.convert_hemisphere(program.bugs)
        program.hemisphere = True
    # Hemisphere Access
    ac_trans = lambda x: True if x == "Yes" else False
    program.access = ac_trans(dict["selectaccess"])
    #Sort By
    program.sort_by = dict["sortby"].upper()
    # Filenames
    program.chartfilename = dict["selectchartfilename"] + ".html"
    program.completionfilename = dict["selectcompletionfilename"] + ".html"
    # Determine if making completion or normal chart
    if not comp_mode:
        #Function
        # Lambda to return fish or bugs full dictionary
        full_crit = lambda x: program.fish_props if x == False else program.bugs_props
        #Conditional to determine function
        if dict["viewcritsby"] == "All Critters (Ignore Global Settings)":
            program.modifier = 2
            use = [crit for crit in tb.sort_by_param(full_crit(program.mode), program.sort_by)]
            #lg.debug(f"all critters 'use': {use}") #DEBUG
            tb.make_table_file_from_list(use, full_crit(program.mode), program, bugs=program.mode, path=program.chartfilename)
            webbrowser.open(program.chartfilename, new=2, autoraise=True)
            program.modifier = 0
            #
        elif dict["viewcritsby"] == "Critters New to This Month":
            program.modifier = -1
            use = tb.list_filter(tb.sort_by_param(full_crit(program.mode), program.sort_by), [crit[0] for crit in anal.month_differences(program)])
            tb.make_table_file_from_list(use, full_crit(program.mode), program, bugs=program.mode, path=program.chartfilename)
            webbrowser.open('file://' + os.path.realpath(program.chartfilename), new=2, autoraise=True)
            program.modifier = 0
            #
        elif dict["viewcritsby"] == "This Month\'s Critters":
            program.modifier = 0
            use = tb.list_filter(tb.sort_by_param(full_crit(program.mode), program.sort_by), [crit[0] for crit in anal.month_differences(program)])
            tb.make_table_file_from_list(use, full_crit(program.mode), program, bugs=program.mode, path=program.chartfilename)
            webbrowser.open(program.chartfilename, new=2, autoraise=True)
            #
        elif dict["viewcritsby"] == "Critters Disappearing Next Month":
            program.modifier = 1
            use = tb.list_filter(tb.sort_by_param(full_crit(program.mode), program.sort_by), [crit[0] for crit in anal.month_differences(program)])
            tb.make_table_file_from_list(use, full_crit(program.mode), program, bugs=program.mode, path=program.chartfilename)
            webbrowser.open(program.chartfilename, new=2, autoraise=True)
            program.modifier = 0
            #
        else:
            raise Exception("Something went wrong when determining which function needs to run on assign_selections.")

# Event Loop
while True:
    event1, values1 = window.read()
    if event1 in (None, 'Cancel'):
        break
    if event1 == "Generate":
        generate(values1)
    if event1 == "Help":
        sg.PopupOK(pr.help_string, title="Instructions")
    if event1 == "completion" and not completion_window_active:
        generate(values1, True) # passing true to mark completion function and avoid creating chart
        # Variable to prevent infinite window loop
        close_out = False
        # Loop to allow window regeneration
        while not close_out:
            completion_window_active = True
            sg.theme_background_color('#ad723b')
            window.hide()
            if not completion_window_mode:
                completion_window = sg.Window("Completion", layout=gen_completion_checklist(program, False))
            else:
                completion_window = sg.Window("Completion", layout=gen_completion_checklist(program, True)) # Passing true to check all boxes
            #comp_layout = [ [sg.Frame(layout=completion_boxes, title="", relief=sg.RELIEF_RIDGE) ]] #DEBUG
            while True:
                completion_window.un_hide()
                event2, values2 = completion_window.read()
                if event2 in (None, "Cancel"):
                    completion_window.close()
                    completion_window_active = False
                    window.un_hide()
                    close_out = True
                    break
                if event2 == "Select All":
                    completion_window_mode = 1
                    completion_window.close()
                    break
                if event2 == "Deselect All":
                    completion_window_mode = 0
                    completion_window.close()
                    break
                if event2 == "Create Chart":
                    # Filter List from Values2
                    program.comp_caught = [key for key, val in values2.items() if val == True]
                    program = anal.completion_full(program)
                    if len(program.comp_caught) >= 80:
                        sg.Popup("I can't give you instructions if you have already caught all the critters!", title="Nice Try!")
                        completion_window.close()
                        completion_window_active = False
                        window.un_hide()
                        close_out = True
                        break
                    program.comp_mode = True
                    tb.make_completion_file_from_list(program, path=program.completionfilename)
                    webbrowser.open(program.completionfilename, new=2, autoraise=True)
                    sg.theme_background_color('#c3d0f3')  # reset background color
                    # Close Window
                    completion_window.close()
                    completion_window_active = False
                    window.un_hide()
                    program.comp_mode = False
                    close_out = True
                    break
            continue
window.close()
