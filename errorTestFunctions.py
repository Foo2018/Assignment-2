def feeds(self):
    print("milk")


def proliferates(self):
    pass


class Mammal(object):
    """ inserts out of place functions in code above. This tests that if a function has made it into the code
     without being declared as belonging to a class it will be picked up"""

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

    @staticmethod
    def proliferates():
        print("plant eater")
