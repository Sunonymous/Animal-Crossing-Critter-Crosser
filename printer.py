# Animal Crossing
# Critter Crosser
# Printer Module

import sys, time

# Tuple to hold month names.
month_names = ("", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
# Lambda to print fish or bugs, southern or northern
progmode = lambda x: "Fish" if x == False else "Bugs"
hem = lambda x: "Southern" if x == True else "Northern"

help_string ="""
------------------------------------------------------------------------------------------------------------------
This is a simple program designed to sort and organize the available critters
in Animal Crossing: New Horizons. It will open by default to the current month
of real time and the northern hemisphere, but these can be changed as needed.
*******************************************************************************************

The sections are numbered for reference. Here's a basic guide to the application:
1. Select whether you wish to view fish or bugs.
2. Set these global settings to your current month and hemisphere.
   If you have easy access to the other hemisphere (via a family member, friend, etc.),
   mark this 'Yes'. Note that this will only affect the completion charts.
The next two sections will generate a chart for you.
3a. Here you can create a chart of critters based on the mode you set, and sorted by
    the method you choose.
3b. This section will create a page of instructions on how to catch all the critters
    that you haven't obtained yet. Clicking the button will open a menu which allows
    you to check the boxes for all the critters you have already caught. Once you have
    marked those, click 'Create Chart' to create a page listing the remaining critters.
    If you selected that you have access to both hemispheres, this will be taken into
    consideration and the creatures will be sorted and listed accordingly. The
    instructions will be listed by month and hemisphere.
The chart pages generated are HTML pages which will open in webbrowsers, and they
will open automatically upon creation. The files are automatically saved into the
folder of the application. You are able to set the filenames before they are
created by entering the name in the 'Filename' boxes in the main menu. If there are
existing charts with the same name (or you do not change the default name), the
existing charts will be written over.

Another usage which isn't as obvious is to discover the soonest you are able to
catch any particular critter(s). To do so, generate a completion chart, selecting
all of the critters -except- the one(s) you are looking to find. Generate a chart
to see the soonest month and details on where to catch it! Ensure you have the
hemisphere access settings set correctly and note the hemisphere that it is in!

*******************************************************************************************
All of the information concerning availability was manually compiled from IGN
and the Animal Crossing Wiki. Because of that there may be errors present. Any
bugs or problems, comments or suggestions may be submitted to u/CritterCrosser.
------------------------------------------------------------------------------------------------------------------
                               Credits for images in #Credits.txt
                                              Thank you!"""


def display_critters_names(critters):
    for crit in critters:
        print(crit[0])
    stall()
