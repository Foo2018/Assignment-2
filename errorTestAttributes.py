

    self.teeth = "sharp"
    self.eyes = 2

class Marsupial(Mammal):
        def proliferates(self):
            print("poach")

class Eutherian(Mammal):
        def proliferates(self):
            print("placenta")

class Carnivore(Mammal):
        def __init__(self):
            self.teeth = "sharp"
            self.eyes = 2

        def proliferates(self):
            print("meat eater")

class Herbivore(Mammal, Carnivore):
        def __init__(self):
            self.teeth = "srp"
            self.skin = "furry"
            self.genus = {}

        def proliferates(self):
            print("plant eater")

