#Author: Andreas Isaksen, andrisa@stud.ntnu.no
import PySimpleGUI as sg
import functools
import operator
import math

def selectVessel(vesselNames):
    # sg.theme('DarkAmber')   # Add a touch of color

    options = vesselNames

    # All the stuff inside your window.
    layout = [
        [sg.Text('Select one vessel'),
         sg.Listbox(options, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(20, len(options)))],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    # Create the Window
    window = sg.Window('Make your choice', layout)

    # Event Loop to process "events" and get the "values" of the input
    while True:
        event, values = window.read()
        #print(f"event={event}")
        if event is None or event == 'Ok' or event == 'Cancel':  # if user closes window or clicks cancel
            break

    # close  the window
    window.close()

    # Have to make the tuple to a string
    outputVessel = functools.reduce(operator.add, values[0])

    return outputVessel