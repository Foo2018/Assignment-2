class Component(object):

    def __init__(self):
        """
        Tests to ensure that all default values are set for attributes
        when new instance of Component object is created
        >>> c = Component()
        >>> print(c.parents)
        []
        >>> print(c.name)
        <BLANKLINE>
        >>> print(c.functions)
        []
        >>> print(c.attributes)
        []
        """
        self.parents = []
        self.name = ''
        self.functions = []
        self.attributes = []

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_functions(self, functions):
        self.functions = functions

    def get_functions(self):
        return self.functions

    def get_attributes(self):
        return self.attributes

    def set_parents(self, parents):
        self.parents = parents

    def get_parents(self):
        return self.parents


if __name__ == "__main__":
    import doctest

    doctest.testmod()
