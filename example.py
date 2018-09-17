class Aframe(House):
    """The A class."""

    def __init__(self):
        self.name = "Bob"
        self.car = "Ford"

    def get_name(self):
        "Returns the name of the instance."
        return self.name


# instance_of_a = A('sample_instance')

class Bungalow(Aframe):

    def __init__(self):
        self.house = "Villa"
        self.street = "nowhere"

    # This method is not part of A.
    def do_something(self):
        """Does some work"""
        pass

    def get_name(self):
        "Overrides version from A"
        return 'B(' + self.house + ')'
