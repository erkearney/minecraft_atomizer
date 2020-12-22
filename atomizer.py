import argparse
import sys

parser = argparse.ArgumentParser(description="Minecraft item atomizer")
parser.add_argument("item_name", nargs=1, help="Name of the minecraft item to atomize")
args = parser.parse_args()
(ITEM_NAME,) = args.item_name

recipes = {}

class item:
    def __init__(self, name, num_produced, materials):
        self.name = name
        self.num_produced = num_produced
        self.materials = materials
        recipes[self.name] = (self.num_produced, self.materials)

coal_ore             = item('coal_ore', 1, [])
cobblestone          = item('cobblestone', 1, [])
iron_ore             = item('iron_ore', 1, [])
log                  = item('log', 1, [])
netherquartz_ore     = item('netherquartz_ore', 1, [])
redstone_ore         = item('redstone_ore', 1, [])
sugarcane            = item('sugarcane', 1, [])

coal                 = item('coal', 1, [(coal_ore, 1)])
stone                = item('stone', 8, [(cobblestone, 8), (coal, 1)])
stone_pressure_plate = item('stone_pressure_plate', 1, [(stone, 2)])
iron_ingot           = item('iron_ingot', 8, [(iron_ore, 8), (coal, 1)])
netherquartz         = item('netherquartz', 1, [(netherquartz_ore, 1)])
redstone_dust        = item('redstone_dust', 5, [(redstone_ore, 1)])
plank                = item('plank', 4, [(log, 1)])
stick                = item('stick', 4, [(plank, 2)])
torch                = item('torch', 4, [(coal, 1), (stick, 1)])
redstone_torch       = item('redstone_torch', 1, [(redstone_dust, 1), (stick, 1)])
redstone_comparator  = item('redstone_comparator', 1, [(redstone_torch, 3), (netherquartz, 1), (stone, 3)])
detector_rail        = item('detector_rail', 6, [(iron_ingot, 6), (stone_pressure_plate, 1), (redstone_dust, 1)])
activator_rail       = item('activator_rail', 6, [(iron_ingot, 6), (redstone_torch, 1), (stick, 2)])
piston               = item('piston', 1, [(plank, 3), (cobblestone, 3), (iron_ingot, 1), (redstone_dust, 1)])
chest                = item('chest', 1, [(plank, 8)])
hopper               = item('hopper', 1, [(chest, 1), (iron_ingot, 5)])
minecart             = item('minecart', 1, [(iron_ingot, 5)])
minecart_with_hopper = item('minecart_with_hopper', 1,[(minecart, 1), (hopper, 1)])
paper                = item('paper', 3, [(sugarcane, 3)])
compass              = item('compass', 1, [(iron_ingot, 4), (redstone_dust, 1)])
emptymap             = item('emptymap', 1, [(paper, 8), (compass, 1)])

#item_name            = item('item_name', 1, [(,),(,),(,)(,),(,),(,),(,),(,)])

raw_materials = {
    'coal_ore' : 0,
    'cobblestone' : 0,
    'iron_ore' : 0,
    'log' : 0,
    'netherquartz_ore' : 0,
    'redstone_ore' : 0,
    'sugarcane' : 0
}

ITEM_TO_ATOMIZE = getattr(sys.modules[__name__], ITEM_NAME)
print(ITEM_TO_ATOMIZE)

def atomize(item, num=1):
    #print("Reducing {} {}".format(num, item.name))
    materials = item.materials
    num_produced = item.num_produced
    #print("num_produced for {}: {}".format(item.name, num_produced))
    for i in materials:
        #print("We need {}, {}".format(i[0].name, i[1] / num_produced * num))
        if i[0].materials == []:
            #print("{} has no materials".format(i[0].name))
            raw_materials[i[0].name] += i[1] / num_produced * num
        else:
            #print("{} has more materials...".format(i[0].name))
            atomize(i[0], i[1] / num_produced * num)
         

atomize(ITEM_TO_ATOMIZE)
for lines in sorted(raw_materials.keys()):
  print('{} {:>4} {:^1} {:^16} {:<10}'.format('|',raw_materials[lines],'|',lines,'|'))
