class Item:
    def __init__(self, name, num_produced, materials=[]):
        self.name = name
        self.num_produced = num_produced
        self.materials = materials


    def print_item(self):
        print("{}, yields: {}, materials: {}".format(self.name, self.num_produced, self.materials))
