import shelve
from extractor import Extractor
from collections import OrderedDict

"""This module consists of functions that serializes and de-serializes 
    the data of Component objects and storing them into a database known as a shelf. 
    The shelf is accessed by using keys, just like a dictionary. 
    The shelve module provides object persistence and object serialization by using the pickle module.
    """


class Shelf(object):
    def __init__(self, filename):
        """
        Testing default values are correctly assigned when new Extractor object is
        created
        >>> s = Shelf('filename.py')
        >>> print(s.selected_file)
        filename.py
        >>> print(s.selected_key)
        filename
        """
        self.selected_file = filename
        self.selected_key = filename.strip('.py')

    def write_shelf(self, shelf_name):
        """Add component data dictionary to shelf file"""
        e = Extractor()
        e.set_file(self.selected_file)
        dict_item = e.get_component_dictionary()
        with shelve.open(shelf_name, "c") as shelf:
            try:
                shelf[self.selected_key] = dict_item
            finally:
                print("Class components of [{}] serialized and stored to database successfully".format(
                    self.selected_file))

    def read_shelf(self, shelf_name):
        with shelve.open(shelf_name) as shelf:
            if self.selected_key in shelf:
                dict_items = shelf[self.selected_key]
                print(dict_items)
            else:
                print("Components of {} cannot be found in the database".format(self.selected_key))

            # dict_item = OrderedDict(sorted(db[self.selected_key].items(), key=lambda x: x[0]))

        # possible output for when reading from the database
        for class_name, class_data in dict_items.items():
            print("Class Name:", class_data.name)
            for attr in class_data.attributes:
                print("\tAttribute:", attr)
            for func in class_data.functions:
                print("\tFunction:", func)
            for parent in class_data.parents:
                print("\tParent:", parent.name)

    def del_shelf(self, shelf_name):
        """Removes the components of selected file stored within the database"""
        with shelve.open(shelf_name) as shelf:
            del shelf[self.selected_key]

    def clear_shelf(self, shelf_name):
        """ Removes all Component objects stored within the database"""
        with shelve.open(shelf_name) as shelf:
            shelf.clear()

    def show_shelf(self, shelf_name):
        """Displays all components and counts the number of them stored in the database"""
        count = 0
        with shelve.open(shelf_name) as shelf:
            if len(shelf) != 0:
                for filename, classes in shelf.items():
                    for class_name, class_data in classes.items():
                        print(class_name)
                        count += 1
                print("The number of components in the database:", count)
            else:
                print("The database is empty")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    s = Shelf('filename.py')
