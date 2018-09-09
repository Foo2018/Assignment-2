import re
from extraction_abstract import ExtractionAbstract
from component import Component
import os
import glob
import sys

""" 
This module receives data from files or folders then
extracts class names, dependencies, function names and attribute details.
For each class it creates a new Component object and places the above details
in that object. This module then outputs a dictionary containing the 
Component objects for that file/folder    

"""


class Extractor(ExtractionAbstract):

    def __init__(self):
        """
        Testing default values are correctly assigned when
        new Extractor object is
        created
        >>> e = Extractor()
        >>> print(e.file)
        <BLANKLINE>
        >>> print(e.component_dict)
        {}
        """
        super().__init__()
        self.file = ''
        self.component_dict = {}

    # imports file name and sets it into variable self.file
    def set_file(self, file_path):
        file_string = file_path
        if os.path.isfile(file_string):
            self._data_extraction(file_string)
        elif os.path.isdir(file_string):
            files = glob.glob(file_string + '/**/*.py', recursive=True)
            for item in files:
                self._data_extraction(item)
        else:
            print("File or directory not found")

    # Takes file name, reads the file, calls extraction methods and
    #  places results into dictionary
    def _data_extraction(self, file_path):
        with open(file_path, 'r') as source_file:
            for line in source_file:
                class_name = self._extract_class(line)
                function_name = self._extract_functions(line)
                attribute_name = self._extract_attributes(line)
                if class_name:
                    comp = self.component_dict.get(class_name[0])
                    if comp is None:
                        comp = Component()
                    comp.set_name(class_name[0])
                    parent = self._extract_parents(line)
                    for item in parent:
                        if item != 'object':
                            parent = self.component_dict.get(item)
                            if parent is None:
                                parent = Component()
                                parent.set_name(item)
                        comp.get_parents().append(parent)
                    self.component_dict[class_name[0]] = comp
                    attribute_dictionary = {}
                elif function_name:
                    try:
                        function_name = function_name[0]
                        comp.get_functions().append(function_name)
                    except UnboundLocalError as err:
                        print('Class has not been declared that contains '
                              'the "{0}" function'.format(function_name))
                        print(err)
                        return
                elif attribute_name:
                    try:
                        if comp.get_functions() == ['__init__']:
                            attr_name = attribute_name[0]
                            data_type_dict = self._extract_defaults_data_types(line)
                            attribute_dictionary[attr_name] = data_type_dict
                            comp.set_attributes(attribute_dictionary)
                    except UnboundLocalError as err:
                        print('Class has not been declared for '
                              '"{0}" attribute'.format(attr_name))
                        print(err)
                        return

    # Performs the regular expressions search and extraction
    @staticmethod
    def _regex_search(regex, data):
        r = re.compile(regex)
        regex_result = r.findall(data)
        return regex_result

    # sends regular expressions statement to _regex_search() and returns
    #  class result
    def _extract_class(self, line):
        regex = '^class\s(\w+)'
        result = self._regex_search(regex, line)
        return result

    # sends regular expressions statement to _regex_search() and returns
    # parent(s) result. Handles both Python 2 & Python 3 class declarations
    def _extract_parents(self, line):
        dependency_list = []
        regex = '^class\s\w+\((.*)\)'
        if not self._regex_search(regex, line):
            return ""
        else:
            dependency_names = self._regex_search(regex, line)[0]
            regex_list = (re.split(r',', dependency_names))
            for item in regex_list:
                if item != 'object':
                    stripped_item = item.strip()
                    dependency_list.append(stripped_item)
            return dependency_list

    # sends regular expressions statement to _regex_search() and returns
    # function result.
    def _extract_functions(self, line):
        regex = 'def\s(\w+)'
        return self._regex_search(regex, line)

    # sends regular expressions statement to _regex_search() and returns
    # attribute(s) result.
    def _extract_attributes(self, line):
        regex = '\s{2}self\.(\w+)'
        regex2 = '\s{2}self\.\w+(\(\))'
        reg1 = self._regex_search(regex, line)
        reg2 = self._regex_search(regex2, line)
        if reg2:
            return
        else:
            return reg1

    # Used to place attribute default values & data types in a dict
    def _extract_defaults_data_types(self, line):
        attr_default = self._extract_attribute_defaults(line)
        if not attr_default:
            return ''
        else:
            attr_type = self._extract_attribute_data_types(attr_default)
            def_data_types_dict = {attr_type: attr_default}
            return def_data_types_dict

    # Extracts default value(s) from an attribute and returns them
    def _extract_attribute_defaults(self, line):
        regex = '\s{2}self\.\w+\s=\s(.*)'
        attribute_default = self._regex_search(regex, line)
        if attribute_default.__len__() != 0:
            attribute_default = attribute_default[0].replace('"', "")
        return attribute_default

    # Identifies attribute data type returns it
    def _extract_attribute_data_types(self, attr_name):
        regex = '^(.)'
        regex2 = '^[A-Z].+\)$'
        extracted_type = self._regex_search(regex, attr_name)
        data_type = extracted_type[0]
        extracted_type_2 = self._regex_search(regex2, attr_name)
        if extracted_type_2:
            return 'obj'
        elif data_type.isalpha():
            return 'str'
        elif data_type == "'":
            return 'str'
        elif data_type == '{':
            return 'dict'
        elif data_type == '[':
            return 'list'
        elif data_type == '(':
            return 'tuple'
        elif data_type.isdigit():
            return "int"
        else:
            print("No data type detected for '{0}'".format(attr_name))
            #sys.exit(1)

    # allows other classes to access the component dictionary
    def get_component_dictionary(self):
        return self.component_dict


# prints output code to see if methods functioning ok
if __name__ == "__main__":
    import doctest

    doctest.testmod()
    e = Extractor()
    e.set_file('mammals.py')
    f = e.get_component_dictionary()
    for obj in f:
        print("Object {0} variables are: {1}".format(obj, vars(f[obj])))
