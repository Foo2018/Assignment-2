""" Test Python file for file extractor - NO __INIT___ METHODS"""


class Alpha(object):
    """The A class."""

    def get_nameA(self, name):
        self.name = ""
        "Returns the name of the instance."
        return name


# instance_of_a = A('sample_instance')

class Beta(Alpha):
    """This is the B class.
    It is derived from A.
    """

    # This method is not part of A.
    def do_something(self):
        """Does some work"""
        pass

    def get_name(self, name):
        "Overrides version from A"
        return 'B(' + name + ')'
