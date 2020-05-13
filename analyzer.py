# Animal Crossing
# Critter Crosser
# Data Analyzer
#    Works with the data compiled

import pandas as pd
from ast import literal_eval
import logging as lg

#Logging
lg.basicConfig(filename='Log.txt', level=lg.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def create_list(filepath):
    # Open the data and read it.
    data = pd.read_csv(filepath, sep=";", engine="python")
    # Convert strings into list.
    data["MONTHS"] = data["MONTHS"].apply(literal_eval)
    return data.values.tolist()

def convert_hemisphere(critters):
    """Given a list of months, converts the list to months of the opposite hemisphere.
    Returns only the boolean, since the list is mutable."""
    for critter in critters:
        critter[1] = [month + 6 if month <= 6 else month - 6 for month in critter[1]]
    return critters

def present_in_month(obj):
    """When passed the state object, returns a list of available critters in the month."""
    # Lambdas
    is_december = lambda month: 1 if month == 12 else (month + 1)
    is_january = lambda month: 12 if month == 1 else (month - 1)
    return [critter for critter in obj.crit_mode(obj.mode) if obj.month in critter[1]]
#alt(obj.modifier)

def will_disappear(obj):
    """Passed the state object, returns creatures no longer available next month."""
    return [critter for critter in present_in_month(obj) if critter not in present_in_month(obj)]

def month_differences(obj):
    """Passed the state object, returns listed critters newly available as of the specified month."""
    # Lambda to shift the state.month back or forward one month
    is_january = lambda month: 12 if month == 1 else (month - 1)
    is_december = lambda month: 1 if month == 12 else (month + 1)
    # Lambda to determine other lambda
    which_way = lambda x: is_january(x) if obj.modifier == -1 else is_december(x)
    # Store original value in variable
    original = obj.month
    # Create two lists, the second after running the function with the decremented variable
    if obj.modifier != 0:
        first = present_in_month(obj)
        obj.month = which_way(obj.month)
        second = present_in_month(obj)
    elif obj.modifier == 0:
        return present_in_month(obj)
    else:
        raise Exception("Something went wrong in the anal.month_differences function.")
    # Return month to original value
    obj.month = original
    # List comprehension for deciding final comparison
    return [critter for critter in first
    if critter not in second]

def completion_full(obj):
    """Creates an ordered list of critters and shifts to give to the table module.
    LST param is a list of CAUGHT critters taken from popup menu.
    OBJ Parameter passed in should be the State object."""
    # Reset any existing results
    obj.comp_results = []
    month_names = ("", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    # Set Master List to Remaining/UNcaught Fish/Bugs
    obj.comp_master = [crit[0] for crit in obj.crit_mode(obj.mode) if crit[0] not in obj.comp_caught]
    #lg.debug(f"Starting process. Len of caught critters is {len(obj.comp_caught)}.")#DEBUG
    # Set index of ordered months to search
    index = [month for month in range(obj.month, 13)] + [month for month in range(1, obj.month)]
    # Copy obj.month to temp var
    backup = obj.month
    # LOOP
    for month in index:
        # Adjust month to search into the state object
        obj.month = month
        # Conditional for dual hemisphere access
        if obj.access:      # Dual Hemispheres
            # Kind of a mess. Runs the completion filter, toggles the hemisphere
            # and then runs it again, before toggling back to the original state.
            obj = completion_filter(obj)
            convert_hemisphere(obj.crit_mode(obj.mode))
            obj.hemisphere = not obj.hemisphere
            obj = completion_filter_hem_switch(obj)
            convert_hemisphere(obj.crit_mode(obj.mode))
            obj.hemisphere = not obj.hemisphere
            if len(obj.comp_master) == 0:
                #print("\n You can catch every critter by the month of {}.\n".format(month_names[obj.month]))
                obj.comp_master.append("X") # Append random value to prevent printing again.
            else:
                obj.comp_results.append('-month-')
        else:               # One  Hemisphere
            obj = completion_filter(obj)
            # Check if finished
            if len(obj.comp_master) == 0:
                #print("\n You can catch every critter by the month of {}.\n".format(month_names[obj.month]))
                obj.comp_master.append("X") # Append random value to prevent printing again.
            else:
                obj.comp_results.append("-month-")
    # Return state object's month to original value
    obj.month = backup
    results_critters = [crit for crit in obj.comp_results if crit[0] != '-']
    #lg.debug(f"Process completed. Len of Results is {len(results_critters)}")
    #lg.debug(f"Results: {(obj.comp_results)}")
    return obj

def completion_filter(obj):
    # Update container list
    monthly = [crit[0] for crit in present_in_month(obj)]
    # Iterate through both lists
    for critter in monthly:
        if critter in obj.comp_master:
            #lg.debug(f"Found {critter} and will remove it.")
            obj.comp_results.append(critter)
            obj.comp_master.remove(critter)
    return obj

def completion_filter_hem_switch(obj):
    # Update container list
    monthly = [crit[0] for crit in present_in_month(obj)]
    # Create container to verify if anything is added.
    cont = []
    # Iterate through both lists
    for critter in monthly:
        if critter in obj.comp_master:
            #lg.debug(f"Found {critter} and will remove it.")
            cont.append(critter)
            obj.comp_master.remove(critter)
    if len(cont) > 0:
        obj.comp_results.append('-hemalt-')
        for crit in cont:
            obj.comp_results.append(crit)
        #obj.comp_results.append('-hemres-') #DEBUG possibly unnecessary
    return obj

def completion_list_filter(lst, obj):
    #DEBUG Might be unused function
    return [crit[0] for crit in obj.crit_mode(obj.mode) if crit[0] not in lst]

def completion_monthly_check(lst, obj):
    # lst should be list of critters UNcaught
    # obj should be program
    #
    # Set index of ordered months to search
    index = [month for month in range(obj.month, 13)] + [month for month in range(1, obj.month)]
    # Copy obj.month to temp var
    backup = obj.month
    # LOOP HERE

    # Return state object's month to original value
    obj.month = backup
