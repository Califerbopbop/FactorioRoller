from tkinter import *
import json
import os
window = Tk()

radius = IntVar()
preview_scale = IntVar()
min_water_tiles = IntVar()
min_iron_tiles = IntVar()
min_copper_tiles = IntVar()
min_coal_tiles = IntVar()
min_stone_tiles = IntVar()
min_crude_oil_tiles = IntVar()
min_starter_iron_tiles = IntVar()
min_starter_copper_tiles = IntVar()
min_starter_coal_tiles = IntVar()
min_starter_stone_tiles = IntVar()
L = IntVar()
pp_l = IntVar()
pp_h = IntVar()
g = IntVar()
b_l = IntVar()
b_h = IntVar()
b_hw = IntVar()
max_rolls = IntVar()
desired_good = IntVar()
batch = IntVar()


roller_parameters = {
}

directory = os.getcwd() + '\\'
with open(directory + 'roller_parameters_default.JSON', 'r') as f:      # starts interface with default values
    roller_parameters = json.load(f)


def update_settings():      # updates interface fields with parameters from parameters dictionary
    global roller_parameters
    L.set(roller_parameters["L"]), pp_l.set(roller_parameters["pp_l"]), pp_h.set(roller_parameters["pp_h"]), \
    g.set(roller_parameters["g"]), b_l.set(roller_parameters["b_l"]), b_h.set(roller_parameters["b_h"]), b_hw.set(
        roller_parameters["b_hw"])

    radius.set(roller_parameters["radius"]), preview_scale.set(roller_parameters["preview_scale"]), \
    min_water_tiles.set(roller_parameters["min_water_tiles"]), min_iron_tiles.set(roller_parameters["min_iron_tiles"])
    min_copper_tiles.set(roller_parameters["min_copper_tiles"]), min_coal_tiles.set(
        roller_parameters["min_coal_tiles"]), \
    min_stone_tiles.set(roller_parameters["min_stone_tiles"]), min_crude_oil_tiles.set(
        roller_parameters["min_crude_oil_tiles"])
    min_starter_iron_tiles.set(roller_parameters["min_starter_iron_tiles"]), min_starter_copper_tiles.set(
        roller_parameters["min_starter_copper_tiles"]), \
    min_starter_coal_tiles.set(roller_parameters["min_starter_coal_tiles"]), min_starter_stone_tiles.set(
        roller_parameters["min_starter_stone_tiles"])

    max_rolls.set(roller_parameters["max_rolls"]), desired_good.set(roller_parameters["desired_good"]), \
        batch.set(roller_parameters["batch"])


update_settings()


def load_custom():
    global roller_parameters
    with open('roller_parameters_custom.JSON', 'r') as f:
        roller_parameters = json.load(f)
    update_settings()


def load_default():
    global roller_parameters
    with open('roller_parameters_default.JSON', 'r') as f:  # load default settings from default JSON
        roller_parameters = json.load(f)
    update_settings()


def cancel():
    global roller_parameters
    roller_parameters["cancel"] = True                                      # set cancel to True so roller doesn't run
    with open('roller_parameters.JSON', 'w') as json_file:                  # update parameters JSON to pass to roller
        json.dump(roller_parameters, json_file, indent=4, sort_keys=True)
    window.destroy()    # close window


def submit():
    global roller_parameters
    roller_parameters["radius"] = radius.get()
    roller_parameters["preview_scale"] = preview_scale.get()
    roller_parameters["min_water_tiles"] = min_water_tiles.get()
    roller_parameters["min_iron_tiles"] = min_iron_tiles.get()
    roller_parameters["min_copper_tiles"] = min_copper_tiles.get()
    roller_parameters["min_coal_tiles"] = min_coal_tiles.get()
    roller_parameters["min_stone_tiles"] = min_stone_tiles.get()
    roller_parameters["min_crude_oil_tiles"] = min_crude_oil_tiles.get()
    roller_parameters["min_starter_iron_tiles"] = min_starter_iron_tiles.get()
    roller_parameters["min_starter_copper_tiles"] = min_starter_copper_tiles.get()
    roller_parameters["min_starter_coal_tiles"] = min_starter_coal_tiles.get()
    roller_parameters["min_starter_stone_tiles"] = min_starter_stone_tiles.get()
    roller_parameters["L"] = L.get()
    roller_parameters["pp_l"] = pp_l.get()
    roller_parameters["pp_h"] = pp_h.get()
    roller_parameters["g"] = g.get()
    roller_parameters["b_l"] = b_l.get()
    roller_parameters["b_h"] = b_h.get()
    roller_parameters["b_hw"] = b_hw.get()
    roller_parameters["max_rolls"] = max_rolls.get()
    roller_parameters["desired_good"] = desired_good.get()
    roller_parameters["batch"] = batch.get()
    roller_parameters["cancel"] = False

    with open('roller_parameters.JSON', 'w') as json_file:                  # update parameters JSON to pass to roller
        json.dump(roller_parameters, json_file, indent=4, sort_keys=True)
    window.destroy()    # close window


def submit_update_custom():
    global roller_parameters
    roller_parameters["radius"] = radius.get()
    roller_parameters["preview_scale"] = preview_scale.get()
    roller_parameters["min_water_tiles"] = min_water_tiles.get()
    roller_parameters["min_iron_tiles"] = min_iron_tiles.get()
    roller_parameters["min_copper_tiles"] = min_copper_tiles.get()
    roller_parameters["min_coal_tiles"] = min_coal_tiles.get()
    roller_parameters["min_stone_tiles"] = min_stone_tiles.get()
    roller_parameters["min_crude_oil_tiles"] = min_crude_oil_tiles.get()
    roller_parameters["min_starter_iron_tiles"] = min_starter_iron_tiles.get()
    roller_parameters["min_starter_copper_tiles"] = min_starter_copper_tiles.get()
    roller_parameters["min_starter_coal_tiles"] = min_starter_coal_tiles.get()
    roller_parameters["min_starter_stone_tiles"] = min_starter_stone_tiles.get()
    roller_parameters["L"] = L.get()
    roller_parameters["pp_l"] = pp_l.get()
    roller_parameters["pp_h"] = pp_h.get()
    roller_parameters["g"] = g.get()
    roller_parameters["b_l"] = b_l.get()
    roller_parameters["b_h"] = b_h.get()
    roller_parameters["b_hw"] = b_hw.get()
    roller_parameters["max_rolls"] = max_rolls.get()
    roller_parameters["desired_good"] = desired_good.get()
    roller_parameters["batch"] = batch.get()
    roller_parameters["cancel"] = False

    with open('roller_parameters_custom.JSON', 'w') as json_file:           # update custom settings JSON
        json.dump(roller_parameters, json_file, indent=4, sort_keys=True)
    with open('roller_parameters.JSON', 'w') as json_file:                  # update parameters JSON to pass to roller
        json.dump(roller_parameters, json_file, indent=4, sort_keys=True)
    window.destroy()


def launch_interface():
    global roller_parameters
    window.geometry("1200x600")
    window.title('Factorio Map Auto-Roller')

    radius_label = Label(window, text='Radius(around base):', font=('calibre', 10, 'bold'))
    preview_scale_label = Label(window, text='Preview scale:', font=('calibre', 10, 'bold'))
    water_label = Label(window, text='Minimum water:', font=('calibre', 10, 'bold'))
    iron_label = Label(window, text='Minimum iron:', font=('calibre', 10, 'bold'))
    copper_label = Label(window, text='Minimum copper:', font=('calibre', 10, 'bold'))
    coal_label = Label(window, text='Minimum coal:', font=('calibre', 10, 'bold'))
    stone_label = Label(window, text='Minimum stone:', font=('calibre', 10, 'bold'))
    crude_oil_label = Label(window, text='Minimum oil:', font=('calibre', 10, 'bold'))
    starter_iron_label = Label(window, text='Minimum starter iron:', font=('calibre', 10, 'bold'))
    starter_copper_label = Label(window, text='Minimum starter copper:', font=('calibre', 10, 'bold'))
    starter_coal_label = Label(window, text='Minimum starter coal:', font=('calibre', 10, 'bold'))
    starter_stone_label = Label(window, text='Minimum starter stone:', font=('calibre', 10, 'bold'))
    max_rolls_label = Label(window, text='Max number of rerolls:', font=('calibre', 10, 'bold'))
    desired_good_label = Label(window, text='Number of good seeds to find before exiting:', font=('calibre', 10, 'bold'))
    batch_label = Label(window, text='Number of screenshots to generate at a time:', font=('calibre', 10, 'bold'))

    radius_entry = Entry(window, textvariable=radius, font=('calibre', 10, 'normal'))
    preview_scale_entry = Entry(window, textvariable=preview_scale, font=('calibre', 10, 'normal'))
    water_entry = Entry(window, textvariable=min_water_tiles, font=('calibre', 10, 'normal'))
    iron_entry = Entry(window, textvariable=min_iron_tiles, font=('calibre', 10, 'normal'))
    copper_entry = Entry(window, textvariable=min_copper_tiles, font=('calibre', 10, 'normal'))
    coal_entry = Entry(window, textvariable=min_coal_tiles, font=('calibre', 10, 'normal'))
    stone_entry = Entry(window, textvariable=min_stone_tiles, font=('calibre', 10, 'normal'))
    crude_oil_entry = Entry(window, textvariable=min_crude_oil_tiles, font=('calibre', 10, 'normal'))
    starter_iron_entry = Entry(window, textvariable=min_starter_iron_tiles, font=('calibre', 10, 'normal'))
    starter_copper_entry = Entry(window, textvariable=min_starter_copper_tiles, font=('calibre', 10, 'normal'))
    starter_coal_entry = Entry(window, textvariable=min_starter_coal_tiles, font=('calibre', 10, 'normal'))
    starter_stone_entry = Entry(window, textvariable=min_starter_stone_tiles, font=('calibre', 10, 'normal'))
    max_rolls_entry = Entry(window, textvariable=max_rolls, font=('calibre', 10, 'normal'))
    desired_good_entry = Entry(window, textvariable=desired_good, font=('calibre', 10, 'normal'))
    batch_entry = Entry(window, textvariable=batch, font=('calibre', 10, 'normal'))

    L_label = Label(window, text='Max dimension of power plant pumps:', font=('calibre', 10, 'bold'))
    pp_l_label = Label(window, text='Power plant length:', font=('calibre', 10, 'bold'))
    pp_h_label = Label(window, text='Power plant height:', font=('calibre', 10, 'bold'))
    g_label = Label(window, text='Gap between power plant and base:', font=('calibre', 10, 'bold'))
    b_l_label = Label(window, text='Base length:', font=('calibre', 10, 'bold'))
    b_h_label = Label(window, text='Base width:', font=('calibre', 10, 'bold'))
    b_hw_label = Label(window, text='Shortest distance along base length to water input:', font=('calibre', 10, 'bold'))

    L_entry = Entry(window, textvariable=L, font=('calibre', 10, 'normal'))
    pp_l_entry = Entry(window, textvariable=pp_l, font=('calibre', 10, 'normal'))
    pp_h_entry = Entry(window, textvariable=pp_h, font=('calibre', 10, 'normal'))
    g_entry = Entry(window, textvariable=g, font=('calibre', 10, 'normal'))
    b_l_entry = Entry(window, textvariable=b_l, font=('calibre', 10, 'normal'))
    b_h_entry = Entry(window, textvariable=b_h, font=('calibre', 10, 'normal'))
    b_hw_entry = Entry(window, textvariable=b_hw, font=('calibre', 10, 'normal'))

    load_default_btn = Button(window, text='Load default settings', command=load_default)
    load_custom_btn = Button(window, text='Load custom settings', command=load_custom)
    sub_btn = Button(window, text='Submit without saving settings changes', command=submit)
    sub_update_custom_btn = Button(window, text='Submit and update custom settings', command=submit_update_custom)
    cancel_btn = Button(window, text='Cancel and exit program without saving anything', bg="red", command=cancel)

    radius_label.grid(row=0, column=0)
    preview_scale_label.grid(row=1, column=0)
    water_label.grid(row=2, column=0)
    iron_label.grid(row=3, column=0)
    copper_label.grid(row=4, column=0)
    coal_label.grid(row=5, column=0)
    stone_label.grid(row=6, column=0)
    crude_oil_label.grid(row=7, column=0)
    starter_iron_label.grid(row=8, column=0)
    starter_copper_label.grid(row=9, column=0)
    starter_coal_label.grid(row=10, column=0)
    starter_stone_label.grid(row=11, column=0)

    L_label.grid(row=0, column=2)
    pp_l_label.grid(row=1, column=2)
    pp_h_label.grid(row=2, column=2)
    g_label.grid(row=3, column=2)
    b_l_label.grid(row=4, column=2)
    b_h_label.grid(row=5, column=2)
    b_hw_label.grid(row=6, column=2)

    L_entry.grid(row=0, column=3)
    pp_l_entry.grid(row=1, column=3)
    pp_h_entry.grid(row=2, column=3)
    g_entry.grid(row=3, column=3)
    b_l_entry.grid(row=4, column=3)
    b_h_entry.grid(row=5, column=3)
    b_hw_entry.grid(row=6, column=3)

    radius_entry.grid(row=0, column=1)
    preview_scale_entry.grid(row=1, column=1)
    water_entry.grid(row=2, column=1)
    iron_entry.grid(row=3, column=1)
    copper_entry.grid(row=4, column=1)
    coal_entry.grid(row=5, column=1)
    stone_entry.grid(row=6, column=1)
    crude_oil_entry.grid(row=7, column=1)
    starter_iron_entry.grid(row=8, column=1)
    starter_copper_entry.grid(row=9, column=1)
    starter_coal_entry.grid(row=10, column=1)
    starter_stone_entry.grid(row=11, column=1)

    batch_label.grid(row=12, column=0)
    batch_entry.grid(row=12, column=1)
    max_rolls_label.grid(row=13, column=0)
    max_rolls_entry.grid(row=13, column=1)
    desired_good_label.grid(row=14, column=0)
    desired_good_entry.grid(row=14, column=1)
    sub_btn.grid(row=15, column=1)
    sub_update_custom_btn.grid(row=15, column=2)
    cancel_btn.grid(row=15, column=3)
    load_default_btn.grid(row=15, column=0)
    load_custom_btn.grid(row=16, column=0)

    window.mainloop()
