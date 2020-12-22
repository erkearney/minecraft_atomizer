import argparse
import sys
import csv

items = {}

raw_materials = {
    'cobblestone' : 0,
    'coal_ore' : 0,
    'iron_ore' : 0,
    'log' : 0,
    'redstone_ore' : 0,
    'netherquartz_ore' : 0
}

def get_item_to_atomize():
    parser = argparse.ArgumentParser(description="Minecraft item atomizer")
    parser.add_argument("item_name", nargs=1, help="Name of the minecraft item to atomize")
    args = parser.parse_args()
    #argparse returns even a single arg as a list, using (ITEM_NAME,) sets
    #ITEM_NAME to only the first entry in that list.
    (ITEM_NAME,) = args.item_name
    return ITEM_NAME


def read_items_from_csv(filename):
    with open(filename, 'r') as csvfile:
        items = {}
        items_csv = csv.reader(csvfile)
        for line in items_csv:
            item_name = line[0]
            item_quantity = int(line[1])
            materials = line[2:]
            for i in range(1, len(materials), 2):
                materials[i] = int(materials[i]) / item_quantity
            items[item_name] = materials
    csvfile.close()
    return items
                    

def atmoize(item, quantity=1):
    materials = items[item]
    if materials == [''] or materials == []:
        raw_materials[item] += quantity
    else:
        for i in range(0, len(materials), 2):
            atmoize(materials[i], materials[i+1] * quantity)
        

def write_to_csv(filename):
    with open(filename, 'w') as csvfile:
        for key in raw_materials:
            csvfile.write("%s, %s\n" % (key, raw_materials[key]))


if __name__ == '__main__':
    ITEM_NAME = get_item_to_atomize()
    items = read_items_from_csv('items.csv')
    atmoize(ITEM_NAME)
    print(raw_materials)
    write_to_csv('output')
