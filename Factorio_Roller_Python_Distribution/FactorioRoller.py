import numpy as np
import os
import Interface
import json
import sys
#import cv2
from PIL import Image
from mask import mask

good_seeds_list = []
RGBA_dict = {
    "water": [45, 94, 127],
    "coal": [30, 30, 30],
    "copper": [255, 127, 0],
    "stone": [255, 255, 0],
    "iron": [0, 229, 229],
    "blacklist": [250, 100, 250],
    "outside_radius": [0, 125, 0],
    "starter_iron": [0, 100, 100],
    "starter_copper": [125, 60, 0],
    "starter_stone": [100, 90, 65],
    "starter_coal": [50, 50, 50],
    "coal_rock": [159, 130, 39],
    "crude_oil": [255, 0, 255],
    "power_plant_and_gap": [165, 40, 40],
    "base": [150, 100, 150]
}
# numpy array version of dict with just the resource values
numpy_rgb_dict = np.array([[45, 94, 127], [0, 229, 229], [255, 127, 0], [30, 30, 30], [255, 255, 0], [150, 100, 150],
                           [165, 40, 40], [255, 0, 255], [0, 100, 100], [125, 60, 0], [50, 50, 50], [100, 90, 65],
                           [0, 125, 0], [250, 100, 250], [165, 40, 40]]).astype(np.uint8)
Interface.launch_interface()    # launch the UI for setting parameters


def resource_path(relative_path):   # Needed for the exe distribution because the working directory changes, this fixes it
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


directory = resource_path(os.getcwd()) + '\\'  # working directory of scripts and resources (corrected for exe distribution)

# use included instance of Factorio to carry out rerolling so user can have their instance of Factorio running, also simplifies mod settings
factorio_exe_dir = '"' + directory + r'Factorio_x64_1.1.62\Factorio_1.1.62\bin\x64\factorio"'

with open(directory + r'\roller_parameters.JSON', 'r') as f:    # create dictionary from JSON parameters passed from UI
    roller_parameters = json.load(f)

# get global parameters from the dictionary
radius = int(roller_parameters["radius"] / 2)
preview_scale = roller_parameters["preview_scale"]
min_water_tiles = roller_parameters["min_water_tiles"]
min_iron_tiles = roller_parameters["min_iron_tiles"]
min_copper_tiles = roller_parameters["min_copper_tiles"]
min_coal_tiles = roller_parameters["min_coal_tiles"]
min_stone_tiles = roller_parameters["min_stone_tiles"]
min_crude_oil_tiles = roller_parameters["min_crude_oil_tiles"]
min_starter_iron_tiles = roller_parameters["min_starter_iron_tiles"]
min_starter_copper_tiles = roller_parameters["min_starter_copper_tiles"]
min_starter_coal_tiles = roller_parameters["min_starter_coal_tiles"]
min_starter_stone_tiles = roller_parameters["min_starter_stone_tiles"]


def preview_import_and_count_python(coordinates):  # import Factorio generated preview png, mask image, count all resources, and return counts of resources
    image_name_string = directory + 'Screenshots\\' + os.listdir(directory + r'Screenshots')[0]    # get first image in folder
    image = Image.open(image_name_string).convert('RGB')
    img = image.copy()
    imgarr = np.array(img)
    del img
    #image = cv2.cvtColor(cv2.imread(image_name_string, 1), cv2.COLOR_BGR2RGB)
    #imgarr = image.copy()
    scale = preview_scale

    # find the middle of the lake (average all x and y positions of lake tiles from the mask
    water_mask = imgarr[:, :, 0] == 45
    water_tiles = np.count_nonzero(water_mask) * scale

    if water_tiles < min_water_tiles:  # if there's not enough water tiles, short circuit the heavy part of the function
        iron_tiles = stone_tiles = copper_tiles = coal_tiles = starter_iron_tiles = starter_stone_tiles = \
            starter_copper_tiles = starter_coal_tiles = crude_oil_tiles = seed = water_tiles
        return water_tiles, iron_tiles, stone_tiles, copper_tiles, coal_tiles, starter_iron_tiles, starter_stone_tiles,\
               starter_copper_tiles, starter_coal_tiles, crude_oil_tiles, seed

    column_average = int(np.average(np.nonzero(water_mask)[0]))
    row_average = int(np.average(np.nonzero(water_mask)[1]))
    outside_radius_mask = np.ones((1024, 1024), dtype=bool)
    starter_mask = np.zeros((1024, 1024), dtype=bool)

    # coordinates = [pp_x0, pp_x1, pp_y0, pp_y1, b_x0, b_x1, b_y0, b_y1, s_x0, s_x1, s_y0, s_y1, mv, mh]
    # Blacklisting the base and beyond the set radius as well as marking the starter zone
    step_v = coordinates[12]  # get vertical step direction depending on mirror of coordinates

    # power plant and gap mask
    imgarr[(column_average + coordinates[2]):(column_average + coordinates[3]):step_v,
    (row_average + coordinates[0]):(row_average + coordinates[1])] = RGBA_dict["power_plant_and_gap"]

    # base mask
    imgarr[(column_average + coordinates[6]):(column_average + coordinates[7]):step_v,
    (row_average + coordinates[4]):(row_average + coordinates[5])] = RGBA_dict["base"]

    # forbid area outside radius
    outside_radius_mask[
    (column_average + coordinates[6] - step_v * radius):(column_average + coordinates[7] + step_v * radius):step_v,
    (row_average + coordinates[4] - radius):(row_average + coordinates[5] + radius)] = False

    # starter zone mask for finding starter patch resources
    starter_mask[(column_average + coordinates[10]):(column_average + coordinates[11]):step_v,
    (row_average + coordinates[8]):(row_average + coordinates[9])] = True

    imgarr[water_mask] = numpy_rgb_dict[0]  # add back water that got destroyed by power plant and base masking above

    # pass masked image, color dictionary array, and zone masks to cython method for faster processing,
    # return debugging output image array "a" and needed tile counts
    a, iron_tiles, stone_tiles, copper_tiles, coal_tiles, starter_iron_tiles, starter_stone_tiles, \
    starter_copper_tiles, starter_coal_tiles, crude_oil_tiles \
        = mask(imgarr, numpy_rgb_dict, outside_radius_mask, starter_mask, preview_scale)

    # image output of the masks for debugging
    #im = Image.fromarray(a.astype(np.uint8), mode='RGBA')
    #im.save("master_mask_output.png")
    #cv2.imwrite("master_mask_output.png", cv2.cvtColor(a, cv2.COLOR_BGR2RGB))

    seed = int(image_name_string.replace(directory + 'Screenshots\\', '').removesuffix('.png'))

    del image, imgarr, water_mask, outside_radius_mask, starter_mask, a

    return water_tiles, iron_tiles, stone_tiles, copper_tiles, coal_tiles, starter_iron_tiles, starter_stone_tiles, starter_copper_tiles, starter_coal_tiles, crude_oil_tiles, seed


def reroll():  # rolls batch size of maps with random string(s) and places the preview image file(s) in the screenshots folder
    os.system(r"cmd /c " + factorio_exe_dir + " --generate-map-preview " + directory + r"Screenshots\ " +
              "--map-gen-settings " + directory + "MapGenSettings.JSON " + "--map-settings " +
              directory + "MapSettings.JSON --map-preview-size=1024 --map-preview-scale=" +
              str(preview_scale) + " --generate-map-preview-random " + str(roller_parameters["batch"]))


def reroll_set_seed(seed):  # rolls map with a set seed and places the preview image file in the screenshots folder
    os.system(r"cmd /c " + factorio_exe_dir + " --generate-map-preview " + directory + r"Screenshots\ " +
              "--map-gen-settings " + directory + "MapGenSettings.JSON " + "--map-settings " +
              directory + "MapSettings.JSON --map-preview-size=1024 --map-preview-scale=" +
              str(preview_scale) + " --map-gen-seed " + seed)


def conditional_loop(tiles):    # checks resource counts against user specified minimums, return good if criteria match
    current_good = False
    not_enough_water = False
    water_tiles, iron_tiles, stone_tiles, copper_tiles, coal_tiles, starter_iron_tiles, starter_stone_tiles, starter_copper_tiles, starter_coal_tiles, crude_oil_tiles, seed = tiles
    if water_tiles < min_water_tiles:
        print("Not enough water tiles: " + str(water_tiles) + "/" + str(min_water_tiles))
        not_enough_water = True
        current_good = False
    else:
        print("Enough water tiles: " + str(water_tiles))
        if iron_tiles < min_iron_tiles or copper_tiles < min_copper_tiles or stone_tiles < min_stone_tiles or coal_tiles < min_coal_tiles or crude_oil_tiles < min_crude_oil_tiles or starter_iron_tiles < min_starter_iron_tiles or starter_copper_tiles < min_starter_copper_tiles or starter_stone_tiles < min_starter_stone_tiles or starter_coal_tiles < min_starter_coal_tiles:
            print("Not enough of an ore")
            print("iron: " + str(iron_tiles) + ", " + "copper: " + str(copper_tiles) + ", " + "stone: " + str(
                stone_tiles) + ", " + "coal: " + str(coal_tiles) + ", " + "crude oil: " + str(crude_oil_tiles))
            print("Starting: iron: " + str(starter_iron_tiles) + ", " + "copper: " + str(
                starter_copper_tiles) + ", " + "stone: " + str(
                starter_stone_tiles) + ", " + "coal: " + str(starter_coal_tiles))
            current_good = False
        else:
            print("Enough of everything")
            print("iron: " + str(iron_tiles) + ", " + "copper: " + str(copper_tiles) + ", " + "stone: " + str(
                stone_tiles) + ", " + "coal: " + str(coal_tiles) + ", " + "crude oil: " + str(crude_oil_tiles))
            print("Starting: iron: " + str(starter_iron_tiles) + ", " + "copper: " + str(
                starter_copper_tiles) + ", " + "stone: " + str(
                starter_stone_tiles) + ", " + "coal: " + str(starter_coal_tiles))
            current_good = True
            good_seeds_list.append(seed)
    return current_good, not_enough_water


def rotate_ccw(coordinates):  # rotates coordinates counterclockwise 90 degrees
    # coordinates = [pp_x0, pp_x1, pp_y0, pp_y1, b_x0, b_x1, b_y0, b_y1, s_x0, s_x1, s_y0, s_y1, mv, mh]
    rotated_coordinates = coordinates.copy()
    rotated_coordinates[0] = coordinates[2]  # pp_x0 = pp_y0  swap x0 and y0
    rotated_coordinates[1] = coordinates[3]  # pp_x1 = pp_y1  swap x1 and y1
    rotated_coordinates[2] = -coordinates[1]  # pp_y0 = -pp_x1 swap x1 and y0 and negate
    rotated_coordinates[3] = -coordinates[0]  # pp_y1 = -pp_x0 swap x0 and y1 and negate
    rotated_coordinates[4] = coordinates[6]  # b_x0 = b_y0 same as above for the base
    rotated_coordinates[5] = coordinates[7]  # b_x1 = b_y1
    rotated_coordinates[6] = -coordinates[5]  # b_y0 = -b_x1
    rotated_coordinates[7] = -coordinates[4]  # b_y1 = -b_x0
    rotated_coordinates[8] = coordinates[10]  # swap s_x0 and s_y0
    rotated_coordinates[9] = coordinates[11]  # swap s_x1 and s_y1
    rotated_coordinates[10] = -coordinates[9]  # swap s_x1 and s_y0 and negate
    rotated_coordinates[11] = -coordinates[8]  # swap s_x0 and s_y1 and negate
    return rotated_coordinates


def mirror_along_horizontal(coordinates):  # mirror coordinates along the horizontal axis (up down mirror)
    # decided to ignore mirrors when I realized the base BP can't be mirrored. Mirroring just the power plant rarely
    # yields a better map, so cut the computation time in half for checking only for rotations
    # coordinates = [pp_x0, pp_x1, pp_y0, pp_y1, b_x0, b_x1, b_y0, b_y1, s_x0, s_x1, s_y0, s_y1, mv, mh]
    mirrored_coordinates = coordinates.copy()
    mirrored_coordinates[2] = -coordinates[2]
    mirrored_coordinates[3] = -coordinates[3]
    mirrored_coordinates[6] = -coordinates[6]
    mirrored_coordinates[7] = -coordinates[7]
    mirrored_coordinates[10] = -coordinates[10]
    mirrored_coordinates[11] = -coordinates[11]
    mirrored_coordinates[14] = -mirrored_coordinates[12]
    return mirrored_coordinates


if __name__ == "__main__":
    if roller_parameters["cancel"]:     # if user selected cancel button, quit
        quit()
    for f in os.listdir(directory + 'Screenshots'):     # clean up any stray files left over in screenshots folder
        os.remove(directory + 'Screenshots\\' + f)
    wr_seed = "3921807045"
    l, pp_l, pp_h, g, b_l, b_h, b_hw = roller_parameters["L"], roller_parameters["pp_l"], \
                                       roller_parameters["pp_h"], roller_parameters["g"], \
                                       roller_parameters["b_l"], roller_parameters["b_h"], \
                                       roller_parameters["b_hw"]  # get base and power plant dimensions from user interface dictionary
    max_rolls = roller_parameters["max_rolls"]
    desired_good = roller_parameters["desired_good"]

    # These coordinates are defined as offsets from the center of the lake,
    # where right is positive x and down is positive y,
    # mh and mv are slice step values to indicate direction to slice to reverse slice when coordinates mirrored
    L = int(l / 2)  # half of power plant pumps square
    pp_x0 = -(pp_l - L)  # left-most point of power plant
    pp_x1 = g + L  # right-most point of power plant
    pp_y0 = -b_hw  # top-most point of power plant
    pp_y1 = L  # bottom-most point of power plant
    b_x0 = g + L  # left-most point of base
    b_x1 = g + L + b_l  # right-most point of base
    b_y0 = -b_hw  # top-most point of base
    b_y1 = b_h - b_hw  # bottom-most point of base
    s_x0 = pp_x0  # left-most point of starting area square
    s_x1 = b_x0  # left-most point of starting area square
    s_y0 = pp_y1  # left-most point of starting area square
    s_y1 = b_y1  # left-most point of starting area square
    mv = 1  # vertical step, deprecated from when vertical slice function existed
    mh = 1  # horizontal step for slicing backwards/forwards depending on if coordinates mirrored
    coordinates = np.array([pp_x0, pp_x1, pp_y0, pp_y1, b_x0, b_x1, b_y0, b_y1, s_x0, s_x1, s_y0, s_y1, mv, mh])

    for coordinate in range(len(coordinates) - 2):  # divide user inputs by the preview scale to convert from in game tiles to preview image pixels
        coordinates[coordinate] = int(coordinates[coordinate] / preview_scale)

    super_coordinates = []
    for rotation in range(4):  # create nested array of all coordinates for all 8 orientations of the base (4 rotations and 4 mirrors)
        super_coordinates.append(coordinates)
        # coordinates = mirror_along_horizontal(coordinates)
        # super_coordinates.append(coordinates)
        # coordinates = mirror_along_horizontal(coordinates)
        coordinates = rotate_ccw(coordinates)
    super_coordinates = np.array(super_coordinates, dtype=int)

    reroll()                        # first reroll to generate a starting image(images if batch > 1) in empty directory
    #reroll_set_seed(seed=wr_seed) # for testing the values above with a selected seed (for example, the current WR seed)

    good_maps = 0
    bad_maps = 0
    good = False
    while (good_maps + bad_maps < max_rolls) and (
            good_maps < desired_good):  # loop until max rolls reached or enough good maps found
        image_name_string = r"" + directory + 'Screenshots\\' + os.listdir(directory + 'Screenshots\\')[0]
        for coordinates in range(
                len(super_coordinates)):  # iterate and check resources for all 8 orientations if needed
            good_map, bad_water = conditional_loop(preview_import_and_count_python(super_coordinates[coordinates]))
            if bad_water:
                good = False
                break  # short circuit checking the rest of the orientations if there's not enough water on the map
            elif not good_map:
                #os.rename("master_mask_output.png", "master_mask_output" + str(coordinates) + ".png")
                good = False
            else:
                #os.rename("master_mask_output.png", "master_mask_output" + str(coordinates) + ".png")
                good = True
                break
        os.remove(image_name_string)  # destroy the temporary image
        if not good:
            bad_maps += 1
            print("Bad maps found: " + str(bad_maps))
            print("Good maps found: " + str(good_maps))
            if good_maps + bad_maps < max_rolls and (good_maps < desired_good) and len(
                    os.listdir(directory + 'Screenshots')) == 0:
                reroll()
        else:
            good_maps += 1
            print("Bad maps found: " + str(bad_maps))
            print("Good maps found: " + str(good_maps))
            print("Good seeds: " + str(good_seeds_list))

            # generate a preview image of the good map in the Found_Good_Maps folder for examples of maps
            # this tool finds
            os.system(r"cmd /c " + factorio_exe_dir + " --generate-map-preview " + directory + r"Found_Good_Maps\ " + "--map-gen-settings " + directory + "MapGenSettings.JSON " + "--map-settings " + directory + "MapSettings.JSON --map-preview-size=1024 --map-preview-scale=" + str(
            preview_scale) + " --map-gen-seed " + str(good_seeds_list[good_maps - 1]))

            # if not at max rolls and not enough good maps yet and no images left in the folder, generate more images
            if good_maps + bad_maps < max_rolls and (good_maps < desired_good) and len(
                    os.listdir(directory + 'Screenshots')) == 0:
                reroll()
    for f in os.listdir(directory + 'Screenshots'):     # clean up screenshots folder in case of finding map before processing all images
        os.remove(directory + 'Screenshots\\' + f)
