from extractor import Extractor

""" Test Python file for file extractor. Also provides test 
if an attribute declared outside of an __init__"""


class Mammal(object):

    @staticmethod
    def feeds():
        print("milk")

    def proliferates(self):
        pass


class Marsupial(Mammal):
    def proliferates(self):
        print("poach")


class Eutherian(Mammal):
    def proliferates(self):
        print("placenta")
        self.eyeballs = 3


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
        self.eyes = 'two'
        self.genus = {}
        self.e = Extractor()
        self.spots = ()
        self.claws = []

    @staticmethod
    def proliferates():
        print("plant eater")
