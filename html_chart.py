# HTML_CHART.py
# Functions to write html

from yattag import Doc

all_year_fish = ["Pale Chub", "Crucian Carp", "Dace", "Carp", "Koi", "Goldfish", "Pop-eyed Goldfish", "Ranchu Goldfish", "Freshwater Goby", "Bluegill", "Black Bass", "Anchovy", "Horse Mackerel", "Sea Bass", "Red Snapper", "Olive Flounder", "Barreleye", "Coelacanth"]
all_year_bugs = ["Paper Kite Butterfly", "Moth", "Wasp", "Citrus Long-horned Beetle", "Bagworm", "Ant", "Hermit Crab", "Wharf Roach", "Fly", "Snail", "Spider"]

def write_html_head(doc, title: str, obj) -> None:
    """Produces the <head> tag and its contents. Comp_mode returns a different background"""
    completion_background = 'body{background-image: url("images/backgrounds/woodTexture.jpg");background-size: 100%;}'
    fish_background = 'body{background-image: url("images/backgrounds/blueShapes.jpg");background-size: 100%;}'
    bugs_background = 'body{background-image: url("images/backgrounds/greenShapes.jpg");background-size: 100%;}'
    with doc.tag("head"):
        with doc.tag("title"):
            doc.text(title)
        doc.stag("meta", charset="UTF-8")
        #doc.stag("link", rel="stylesheet", type="text/css", href="style.css")
        with doc.tag("style"):
            if obj.comp_mode:
                doc.text(completion_background)
            else:
                if obj.mode: # Bugs
                    doc.text(bugs_background)
                else:
                    doc.text(fish_background)
            if obj.mode: # Bugs
                doc.text(obj.bugscss)
            else:
                doc.text(obj.fishcss)
        doc.stag("meta", name="viewport", content="width=device-width, initial-scale=1")

def write_table_headers(doc, obj):
    with doc.tag('th'):
        doc.text("Name")
    with doc.tag('th'):
        doc.text("Image")
    with doc.tag('th'):
        doc.text("Price")
    with doc.tag("th"):
        doc.text("Location")
    if not obj.mode:
        with doc.tag('th'):
            doc.text("Shadow Size")
    with doc.tag('th'):
        doc.text(" Time")

def write_table_critters(doc, lst, obj):
    """lst should be separated segment/month of critters in list form
    obj should be program"""
    #Lambda to get data
    props = lambda x: obj.fish_props if x == False else obj.bugs_props
    data = props(obj.mode)
    #print(lst) #DEBUG
    for critter in lst:
        #print(f"Testing: {critter}") #DEBUG
        with doc.tag('tr'):
            with doc.tag('td'): #NAME
                if critter in all_year_fish:
                    doc.text(f"{critter}*")
                elif critter in all_year_bugs:
                    doc.text(f"{critter}*")
                else:
                    doc.text(critter)
            with doc.tag('td'): #IMAGE
                mode = lambda x: "images\\bugs\\" if x == True else "images\\fish\\"
                loc = mode(obj.mode)
                image_format = '.png'
                strung = loc + data[critter]["IMAGE"] + image_format
                doc.stag("img", src=strung, alt="critter pic")
            with doc.tag('td'): #PRICE
                doc.text(data[critter]["PRICE"])
            with doc.tag('td'): #LOCATION
                doc.text(data[critter]["LOCATION"])
            if not obj.mode:
                with doc.tag('td'):
                    doc.text(data[critter]["SHADOWSIZE"])
            with doc.tag('td'): #Time
                doc.text(data[critter]["TIME"])
