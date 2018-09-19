""" Test Python file for file extractor - NO __INIT___ METHODS"""


class Alpha(object):
    """The A class."""

    def get_nameA(self, name):
        self.name = ""
        return name


class Beta(Alpha):
    """This is the B class.
    It is derived from A.
    """

    def do_something(self):
        pass

    def get_name(self, name):
        return 'B(' + name + ')'
