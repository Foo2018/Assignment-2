    self.teeth = "sharp"


class Mammal(object):
    """ inserts out of place attribute code above. This tests that if an attribute has made it into the code
     without being declared as belonging to a class it will be picked up"""

    @staticmethod
    def feeds():
        print("milk")


class Marsupial(Mammal):
    @staticmethod
    def proliferates():
        print("poach")


class Eutherian(Mammal):
    @staticmethod
    def proliferates():
        print("placenta")


class Carnivore(Mammal):
    def __init__(self):
        self.teeth = "sharp"
        self.eyes = 2

    @staticmethod
    def proliferates():
        print("meat eater")


class Herbivore(Mammal, Carnivore):
    def __init__(self):
        self.teeth = "srp"
        self.skin = "furry"
        self.genus = {}

    @staticmethod
    def proliferates():
        print("plant eater")
