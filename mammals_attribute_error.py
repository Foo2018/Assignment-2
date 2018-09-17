from extractor import Extractor


class Mammal(object):
    """ Test Python file for file extractor"""

    def feeds(self):
        print("milk")

    def proliferates(self):
        pass


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
        self.nose = ""
        self.genus = {}
        self.e = Extractor()
        self.spots = ()
        self.fur = @
        self.tail

    def proliferates(self):
        print("plant eater")
