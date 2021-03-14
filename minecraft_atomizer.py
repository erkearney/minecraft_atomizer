'''
This module will take a minecraft item and break it down into its 'raw'
components. Useful for determining how component items you'll need in order to
build a larger project, or for making trades between players. An items.csv
file containing minecraft item names, that items' yield upon crafting
(e.g., 4 for torch), and the items along with the quantities of those items
required to create those items must be placed in the same directory as this
script. Such a file can be obtained on my github TODO: Add link.

Examples
--------
    $ python minecraft_atomizer.py torch

Outputs coal_ore: 0.25, log: 0.03125, as these are the base items required to
produce 1 torch

    $ python minecraft_atomizer.py piston -w

Outputs cobbleston: 3.0, coal_ore: 0.125, iron_ore: 1.0, log: 0.75,
redstone_ore: 0.2. Also writes these results to a file called output.txt

Attributes
----------
ITEM_NAME : string (default: torch)
    The name of the minecraft atom to be atomized

WRITE : bool
    If true, write the results of atomization to a file called output.txt

DEBUG : bool
    If true, be verbose
'''
import argparse
import csv

ITEM_NAME = 'torch'
WRITE = False
DEBUG = False

def setup_args():
    '''
    Sets up command-line arguments

    If running from an IDE instead of the command line, simply set these
    values here (e.g., ITEM_NAME = 'torch', WRITE = TRUE, etc.)

    Attributes
    ----------
    ITEM_NAME : string (optional, default='torch')
        The name of the item to be atomized

    WRITE : bool (optional, default=False)
        If True, write the results of the atmoization to a file called
        output.txt

    DEBUG : bool (optional, default=False)
        if True, print out useful debug information

    parser : ArgumentParser
        Parses command-line arguments

    args : Parsed Arguments
    '''
    global ITEM_NAME
    global WRITE
    global DEBUG

    parser = argparse.ArgumentParser(description='Minecraft item atomizer')
    parser.add_argument('ITEM_NAME', nargs='?', default='torch',
        help='Name of the minecraft item to atomize (default: torch)')
    parser.add_argument('-w', '--WRITE', action='store_true',
        help='Write the atomized results to a file called output')
    parser.add_argument('-d', '--DEBUG', action='store_true',
        help='Be verbose')
    args = parser.parse_args()

    ITEM_NAME = args.ITEM_NAME
    WRITE = args.WRITE
    DEBUG = args.DEBUG


raw_materials = {
    'cobblestone' : 0,
    'coal_ore' : 0,
    'iron_ore' : 0,
    'log' : 0,
    'redstone_ore' : 0,
    'netherquartz_ore' : 0
}


def read_items_from_csv(csv_filename):
    '''
    Reads in minecraft items from a comma separated file which by default
    will be called items.csv

    Attributes
    ----------
    csv_filename : string
        The name of the csv file to read the items from

    csv_items : dictionary {string : list}
        Contains the items once they've been read in. The key is the name of
        the item and the value is the list of materials, along with their
        required quantities to produce ONE of that item.
        (e.g., 'torch' : ['coal',0.25,'stick',0.25])

    items_csv : csvfile
        A temporary variable for the csvfile while it's being read

    item_name : string
        The first value in a line of the csv file, the item's name

    item_quanitity : int
        The second value in a line of the csv file, the number of that item
        that are produced with a single 'recipe', (i.e., it's impossible to
        create a single torch, they are created four at a time)

    materials : list
        The remaining values in a line of the csv file, formatted as the name
        of the item required, followed by the quantity of that item


    Example line in the csv file:
        torch,4,coal,1,stick,1
        Indicated that 4 torches can be created using 1 stick and 1 coal
    '''
    if DEBUG:
        print('---------------------------------')
        print('reading items from {}'.format(csv_filename))
    with open(csv_filename, 'r') as csvfile:
        csv_items = {}
        items_csv = csv.reader(csvfile)
        for line in items_csv:
            if DEBUG:
                print('Now reading line: {}'.format(line))
            item_name = line[0]
            item_quantity = int(line[1])
            materials = line[2:]
            for i in range(1, len(materials), 2):
                materials[i] = int(materials[i]) / item_quantity
            csv_items[item_name] = materials

            if DEBUG:
                print('Adding {}: {} to csv_items list'.format(
                    item_name, materials))
    csvfile.close()
    return csv_items


def atmoize(csv_items, item, quantity=1):
    '''
    Recursively reduced an item down to its base components

    Attributes
    ---------
    csv_items : dictionary {string : list}
        A dictionary of items that should have been created with
        read_items_from_csv

    item : string
        The name of the item to be atomized

    quantity : int
        The number of items required in the recipe

    raw_materials : dictionary {string : int}
        Conatains the results of the atomization (e.g., log : 0.75)
    '''
    if DEBUG:
        print('---------------------------------')
        print('atomizing {}'.format(item))
    materials = csv_items[item]
    if materials in ([''], []):
        if DEBUG:
            print('{} + {}'.format(item, quantity))
        raw_materials[item] += quantity
    else:
        if DEBUG:
            print('Results: {}'.format(materials))
        for i in range(0, len(materials), 2):
            atmoize(csv_items, materials[i], materials[i+1] * quantity)


def write_to_csv(filename):
    '''
    Writes results to a csvfile called filename

    Attributes
    ----------
    filename : string
        Name of the file to write results to

    raw_materials : dictionary {string : int}
        Conatains the results of the atomization (e.g., log : 0.75)
    '''
    if DEBUG:
        print('---------------------------------')
        print('writing to {}'.format(filename))
    with open(filename, 'w') as csvfile:
        for key in raw_materials:
            csvfile.write("%s, %s\n" % (key, raw_materials[key]))


if __name__ == '__main__':
    setup_args()
    imported_csv_items = read_items_from_csv('items.csv')
    atmoize(imported_csv_items, ITEM_NAME)
    print(raw_materials)
    if WRITE:
        write_to_csv('output')
