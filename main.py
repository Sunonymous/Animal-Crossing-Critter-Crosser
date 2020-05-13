# Animal Crossing
# Critter Crosser

from datetime import datetime
import webbrowser
import printer as pr
import analyzer as anal
import table as tb

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
        # Create data lists
        self.fish = anal.create_list("fish.csv")
        self.bugs = anal.create_list("bugs.csv")
        # Generate empty container lists for use later.
        self.comp_master, self.comp_results = [], []

    # This is the only lambda accessed outside of this module.
    crit_mode = lambda self, x: self.fish if x == False else self.bugs


### FUNCTIONS
# Simple function to toggle a boolean
def toggle(bool):
    return not bool

# Lambdas for showing statuses and choosing mode
hem = lambda x: "Southern" if x == True else "Northern"
crit = lambda x: "Fish" if x == False else "Bugs"
month_names = pr.month_names

# Create program class state
program = State()
"""# Create data lists
program.fish = anal.create_list("fish.csv")
program.bugs = anal.create_list("bugs.csv")"""

# Greeting text will only print once.
#pr.intro_greeting() #DEBUG REMOVE WHEN COMPLETE

while program.active:

    # Main Menu
    # Show status of variables and program state
    pr.show_status(pr.month_names[program.month], hem(program.hemisphere), crit(program.mode))

    # Offer choices
    selection = pr.menu_choices()

    # Menu selection branch
    if selection == "1":
        #Change Month
        print("Please enter the month you would like to select. (1-12)")
        program.month = int(pr.get_selection(12))
    if selection == "2":
        #Toggle Hemisphere
        program.fish = anal.convert_hemisphere(program.fish)
        program.bugs = anal.convert_hemisphere(program.bugs)
        program.hemisphere = toggle(program.hemisphere)
    if selection == "3":
        #Toggle Critters
        program.mode = toggle(program.mode)
    if selection == "4":
        #View This Month's Available Critters
        print("These are the available {} during the month of {} in the {} hemisphere.\n".format(crit(program.mode), month_names[program.month], hem(program.hemisphere)), "-" * 95)
        pr.display_critters_names(anal.present_in_month(program))
    if selection == "5":
        #View This Month's New Fish
        print("These are the newly available {} as of the month of {} in the {} hemisphere.\n".format(crit(program.mode), month_names[program.month], hem(program.hemisphere)), "-" * 85)
        program.modifier = -1
        pr.display_critters_names(anal.month_differences(program))
        program.modifier = 0
    if selection == "6":
        #View This Month's Departing Fish
        print("These are the {} disappearing after the month of {} in the {} hemisphere.\n".format(crit(program.mode), month_names[program.month], hem(program.hemisphere)), "-" * 85)
        program.modifier = 1
        pr.display_critters_names(anal.month_differences(program))
        program.modifier = 0
    if selection == "7":
        #Earliest Completion Function
        pr.completion_prompt(program)
        choice = pr.get_selection(3)
        if choice == "1": # Both Hemispheres
            program.access = True
            program = anal.completion_full(program)
            pr.print_completion(program.comp_results)
            pr.stall()
        elif choice == "2": # One Hemisphere
            program.access = False
            program = anal.completion_full(program)
            pr.print_completion(program.comp_results)
            pr.stall()
        else:
            pass
    if selection == "8":
        #Help String
        pr.help()
        pr.stall()
    if selection == "9":
        #Make Table
        lst = [crit[0] for crit in anal.present_in_month(program)]
        tb.make_table_file_from_list(lst, program.fish_props)
        webbrowser.open("lst_gen_table.html", new=2, autoraise=True)
        #print(pr.display_critters_names(program.fish))
    if selection == "10":
        #Exit
        program.active = False #shut it down!

pr.close() #DEBUG REMOVE WHEN COMPLETE
