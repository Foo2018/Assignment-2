""" Tests for stub creation (House)"""


class Aframe(House):

    def __init__(self):
        self.name = "Bob"
        self.car = "Ford"

    def get_name(self):
        return self.name


class Bungalow(Aframe):

    def __init__(self):
        super().__init__()
        self.name = "Villa"
        self.car = "nowhere"

    # This method is not part of A.
    def do_something(self):
        """Does some work"""
        pass

    def get_name(self):
        """Overrides version from A"""
        return 'B(' + self.house + ')'
