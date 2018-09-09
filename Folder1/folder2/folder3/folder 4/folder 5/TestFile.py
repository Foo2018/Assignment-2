""" Test Python file for file extractor"""
class Alpha(object):
    """The A class."""
    def __init__(self, nameA, carA):
        self.name = nameA
        self.car = carA

    def get_nameA(self):
        "Returns the name of the instance."
        return self.name

#instance_of_a = A('sample_instance')

class Beta(Alpha):
    """This is the B class.
    It is derived from A.
    """
    def __init__(self, houseB, addressB):
        self.house = houseB
        self.address = addressB
    # This method is not part of A.
    def do_something(self):
        """Does some work"""
        pass

    def get_name(self):
        "Overrides version from A"
        return 'B(' + self.name + ')'