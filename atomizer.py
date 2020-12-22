import argparse
import sys
import csv
from item import Item

items = {}

#class item:
#    def __init__(self, name, num_produced, materials):
#        self.name = name
#        self.num_produced = num_produced
#        self.materials = materials

coal_ore = Item('coal_ore', 1, [])
coal = Item('coal', 1, [(coal_ore, 1)])
cobblestone = Item('cobblestone', 1, [])
stone = Item('stone', 8, [(cobblestone, 8), (coal, 1)])
stone_pressure_plate = Item('stone_pressure_plate', 1, [(stone, 2)])
iron_ore = Item('iron_ore', 1, [])
iron_ingot = Item('iron_ingot', 8, [(iron_ore, 8), (coal, 1)])
netherquartz_ore = Item('netherquartz_ore', 1, [])
netherquartz = Item('netherquartz', 1, [(netherquartz_ore, 1)])
log = Item('log', 1, [])
redstone_ore = Item('redstone_ore', 1, [])
redstone_dust = Item('redstone_dust', 5, [(redstone_ore, 1)])
plank = Item('plank', 4, [(log, 1)])
stick = Item('stick', 4, [(plank, 2)])
torch = Item('torch', 4, [(coal, 1), (stick, 1)])
redstone_torch = Item('redstone_torch', 1, [(redstone_dust, 1), (stick, 1)])
redstone_comparator = Item('redstone_comparator', 1, [(redstone_torch, 3), (netherquartz, 1), (stone, 3)])
detector_rail = Item('detector_rail', 6, [(iron_ingot, 6), (stone_pressure_plate, 1), (redstone_dust, 1)])
activator_rail = Item('activator_rail', 6, [(iron_ingot, 6), (redstone_torch, 1), (stick, 2)])
piston = Item('piston', 1, [(plank, 3), (cobblestone, 3), (iron_ingot, 1), (redstone_dust, 1)])

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
    return getattr(sys.modules[__name__], ITEM_NAME)


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
                    

def atomize(item, num=1):
    materials = item.materials
    num_produced = item.num_produced
    for i in materials:
        if i[0].materials == []:
            raw_materials[i[0].name] += i[1] / num_produced * num
        else:
            atomize(i[0], i[1] / num_produced * num)
         

def atomize2(item, quantity=1):
    materials = items[item]
    if materials == [''] or materials == []:
        raw_materials[item] += quantity
    else:
        for i in range(0, len(materials), 2):
            atomize2(materials[i], materials[i+1] * quantity)
        

def write_to_csv(filename):
    with open(filename, 'w') as csvfile:
        for key in raw_materials:
            csvfile.write("%s, %s\n" % (key, raw_materials[key]))


if __name__ == '__main__':
    #ITEM_TO_ATOMIZE = get_item_to_atomize()
    items = read_items_from_csv('items.csv')
    atomize2('piston')
    #atomize(ITEM_TO_ATOMIZE)
    print(raw_materials)
    write_to_csv('output')
