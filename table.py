import pandas as pd
from yattag import Doc
import html_chart as char
import pprint as pp #DEBUG
import logging as lg #DEBUG

#Logging
lg.basicConfig(filename='Log.txt', level=lg.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def generate_property_dictionaries():
    # Open the CSV and read it into a variable
    fish_props = pd.read_csv(r"data\fish_props.csv", sep=",", engine="python")
    bugs_props = pd.read_csv(r"data\bugs_props.csv", sep=",", engine="python")
    # Create Empty dictionaries to hold the formatted data.
    fish_dict = {}
    bugs_dict = {}
    # Iterate through the data and assign it to a dictionary in the value for the key name of the critter.
    for index, row in fish_props.iterrows():
        fish_dict[row['NAME']] = {"NAME": row["NAME"], "IMAGE": row["IMAGE"], "PRICE":row["PRICE"], "LOCATION":row["LOCATION"], "SHADOWSIZE":row["SHADOWSIZE"], "TIME":row["TIME"]}
    for index, row in bugs_props.iterrows():
        bugs_dict[row['NAME']] = {"NAME": row["NAME"], "IMAGE": row["IMAGE"], "PRICE":row["PRICE"], "LOCATION":row["LOCATION"], "TIME":row["TIME"]}
    return fish_dict, bugs_dict

# Format that the dictionaries are saved in.
#dict format: { 'fish_name': { 'IMAGE': 'icon_name', 'PRICE': 0, 'LOCATION': 'location', 'SHADOWSIZE': 0, 'TIME': 'time' } }
#fish_dict, bugs_dict = generate_property_dictionaries()


def sort_by_param(dict, param): #DEBUG Many lines in this function
    """Sort a dictionary by a particular parameter. Returns a list.
    PARAM OPTIONS: NAME, PRICE, LOCATION, TIME"""
    done = []
    for item in sorted(dict.keys(), key=lambda x: dict[x][param]):
        done.append(item)
    return done

def list_filter(orig, limit):
    """Filters"""
    return [x for x in orig if x in limit ]

# YATTAG Stuff
def new_table(data, bugs=False):
    """DATA Should be a passed dictionary.
    Pass True for the second parameter to do bugs."""
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with doc.tag("title"):
                doc.text("Animal Crossing Critter Crosser")
            doc.stag("meta", charset="UTF-8")
            doc.stag("link", rel="stylesheet", type="text/css", href="style.css")
        with tag('body'):
            with tag('table'):
                with tag('th'):
                    text("Name")
                with tag('th'):
                    text("Image")
                with tag('th'):
                    text("Price")
                with tag("th"):
                    text("Location")
                with tag('th'):
                    text("Time")
                for critter in data:
                    with tag('tr'):
                        with tag('td'): #NAME
                            text(critter)
                        with tag('td'): #IMAGE
                            mode = lambda x: "images\\bugs\\" if x == True else "images\\fish\\"
                            loc = mode(bugs)
                            image_format = '.png'
                            strung = loc + data[critter]["IMAGE"] + image_format
                            doc.stag("img", src=strung, alt="critter pic")
                        with tag('td'): #PRICE
                            text(data[critter]["PRICE"])
                        with tag('td'): #LOCATION
                            text(data[critter]["LOCATION"])
                        with tag('td'): #Time
                            text(data[critter]["TIME"])
    return doc.getvalue()

def new_table_from_list(lst, data, obj, bugs=False):
    """LIST passed a list of available critters
    DATA Should be a passed dictionary.
    Pass True for the second parameter to do bugs."""
    month_names = ("", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    # Lambdas to improve formatting
    hem = lambda x: "Southern" if x == True else "Northern"
    crit = lambda x: "Fish" if x == False else "Bugs"
    chart_desc = (lambda x: f"Available in {month_names[obj.month]}"
                    if x == 0 else (f"Disappearing after {month_names[obj.month]}" if x == 1
                    else (f"Newly Available in {month_names[obj.month]}" if x == -1 else "")))
    # Start Yattag bits
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        char.write_html_head(doc, "Animal Crossing Critter Crosser Chart", obj)
        with tag('body'):
            with tag("div", klass="top"):
                with tag("h1"):
                    text("Animal Crossing New Horizons")
                with tag("h2"):
                    text(f"All {crit(obj.mode)} {chart_desc(obj.modifier)} ({hem(obj.hemisphere)[0]})")
            with tag('table'):
                with tag('th'):
                    text("Name")
                with tag('th'):
                    text("Image")
                with tag('th'):
                    text("Price")
                with tag("th"):
                    text("Location")
                with tag('th'):
                    text("Time")
                for critter in lst:
                    if critter in data:
                        with tag('tr'):
                            with tag('td'): #NAME
                                text(critter)
                            with tag('td'): #IMAGE
                                mode = lambda x: "images\\bugs\\" if x == True else "images\\fish\\"
                                loc = mode(bugs)
                                image_format = '.png'
                                strung = loc + data[critter]["IMAGE"] + image_format
                                doc.stag("img", src=strung, alt="critter pic")
                            with tag('td'): #PRICE
                                text(data[critter]["PRICE"])
                            with tag('td'): #LOCATION
                                text(data[critter]["LOCATION"])
                            with tag('td'): #Time
                                text(data[critter]["TIME"])
    return doc.getvalue()

def check_equal(lst):
    return lst[1:] == lst[:-1]

def completion_list_multi_splitter(lst, val, mode=False):
    """mode is single when true is given instead of false
       this means that the splitter is only present once"""
    container = []
    if mode: #only once
        if val in lst:
            assert val in lst, "list_splitter Error: Value not contained in list."
            container = []
            container.append(lst[:lst.index(val)]) #DEBUG CHECK IF ADDS MISSING FISH
            container.append(lst[(lst.index(val) + 1):])
        else:
            return lst
    else: #val is present more than once in the lst
        while val in lst:
            if len(lst) > 1:
                spotted = lst.index(val)
                container.append(lst[:spotted])
                lst = lst[spotted + 1:]
            else:
                break
            continue
    return container

def new_completion_table(obj):
    """A function to generate HTML for instructions to catch all critters
    LST passed a list of critters already caught
    OBJ is program object for state variables."""
    # Lambda to get data
    props = lambda x: obj.fish_props if x == False else obj.bugs_props
    data = props(obj.mode)
    # Tuple To Display Months
    month_names = ("", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    # Lambdas to improve formatting
    hem = lambda x: "Southern" if x == True else "Northern"
    crit = lambda x: "Fish" if x == False else "Bugs"
    # Variables to Track the Month
    start_mon = obj.month
    month_add = 0
    is_december = lambda month, add: 1 if month + add == 12 else (add + 1)
    # Set  default hemisphere and secondary for ease
    orig_hem = hem(obj.hemisphere)
    sec_hem = hem(not obj.hemisphere)
    # Split up results by month
    split_months = completion_list_multi_splitter(obj.comp_results, '-month-')
    #pp.pprint(split_months) #DEBUG
    # Start Yattag bits
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        char.write_html_head(doc, "Animal Crossing Critter Crosser", obj)
        with tag('body'):
            with tag("div", klass="top"):
                with tag("h1"):
                    text("Animal Crossing New Horizons")
                with tag("h2"):
                    text(f"{hem(obj.hemisphere)} Hemisphere {crit(obj.mode)} Completion Guide")
            with tag('div', klass="note"):
                text("Note: Critters marked with an * after their name may be caught during any month.")
            # MAIN LOOP
            for month in split_months:
                if len(month) <= 0:
                    month_add = is_december(start_mon, month_add)
                else:
                    with tag("div", klass="month"):
                        per_hem = completion_list_multi_splitter(month, '-hemalt-', True) #True for single occurrence mode
                        #lg.debug(f"split month: {per_hem}") #DEBUG
                        if per_hem != []: # if month is not empty
                            with doc.tag('h3'):
                                text(f"Month of {month_names[start_mon + month_add]}")
                                #doc.stag('br') #DEBUG may remove
                            doc.stag('hr')
                            if len(per_hem[0]) > 0:
                                with doc.tag('h4'):
                                    text(f'{orig_hem} Hemisphere')
                            if isinstance(per_hem[0], list): # both hemispheres contain critters to catch
                                if len(per_hem[0]) > 0:
                                    with tag('table'):
                                        char.write_table_headers(doc, obj)
                                        char.write_table_critters(doc, per_hem[0], obj)
                                with doc.tag('h4'):
                                    text(f"\n\t{sec_hem} Hemisphere") # AFTER FIRST MONTH
                                with tag('table'):
                                    char.write_table_headers(doc, obj)
                                    char.write_table_critters(doc, per_hem[1], obj)
                            else:
                                with tag('table'):
                                    char.write_table_headers(doc, obj)
                                    char.write_table_critters(doc, per_hem, obj)
                        #print(f"month index: {start_mon} add: {month_add}") #DEBUG
                        month_add = is_december(start_mon, month_add)
    return doc.getvalue()

def make_completion_file_from_list(obj, path="Completion_Chart.html"):
    """Function to create an HTML table when passed a path and the data to use in the form of a dictionary."""
    with open(path, mode='w') as file:
        file.write(new_completion_table(obj))


def make_table_file_from_list(lst, data, obj, path="Critter_Chart.html", bugs=False):
    """Function to create an HTML table when passed a path and the data to use in the form of a dictionary."""
    with open(path, mode='w') as file:
        file.write(new_table_from_list(lst, data, obj, bugs))

#dict format: { 'fish_name': { 'IMAGE': 'icon_name', 'PRICE': 0, 'LOCATION': 'location', 'SHADOWSIZE': 0, 'TIME': 'time' } }
