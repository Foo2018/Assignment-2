import re
from extraction_abstract import ExtractionAbstract
from component import Component
import os
import glob
from attribute_default_search import AttributeDefaultsSearch
from line_search import LineSearch

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
        self.attribute_dictionary = None
        self.component = None

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
                is_class_name = self._extract_class(line)  # **************************
                is_function_name = self._extract_functions(line)  # **************************
                is_attribute_name = self._extract_attributes(line)  # **************************
                if is_class_name:
                    self.component = self._set_class_name(is_class_name, line)
                elif is_function_name:
                    self._place_function_name_in_component_object(is_function_name)
                elif is_attribute_name:
                    self._place_attribute_name_and_default_value_in_dict(is_attribute_name, line)

    def _set_class_name(self, class_name, line):
        component = Component()
        component.set_name(class_name[0])
        self._class_parent_name_handling(line, component)
        self.component_dict[class_name[0]] = component
        self.attribute_dictionary = {}
        return component

    def _class_parent_name_handling(self, line, comp):
        parent = self._extract_parents(line)
        for item in parent:
            parent = self.component_dict.get(item)
            self._create_new_parent_class_if_nonexistant(parent, item, comp)

    def _create_new_parent_class_if_nonexistant(self, parent, item, comp):
        if parent is None:
            parent = Component()
            parent.set_name(item)
        comp.get_parents().append(parent)

    def _place_function_name_in_component_object(self, function_name):
        try:
            function_name = function_name[0]
            self.component.get_functions().append(function_name)
        except Exception as err:
            print('Class has not been declared that contains '
                  'the "{0}" function'.format(function_name))
            print(err)
            raise

    def _place_attribute_name_and_default_value_in_dict(self, attribute_name, line):
        try:
            if self.component.get_functions() == ['__init__']:
                attr_name = attribute_name[0]
                search = AttributeDefaultsSearch()
                data_type_dict = search.attribute_extraction(line)
                self.attribute_dictionary[attr_name] = data_type_dict
                self.component.set_attributes(self.attribute_dictionary)
        except Exception as err:
            print(err)
            raise

    ##################################################################################################################

    # New class called "Text search" with following methods?
    # Performs the regular expressions search and extraction
    @staticmethod
    def _regex_search(regex, data):
        r = re.compile(regex)
        regex_result = r.findall(data)
        return regex_result

    # sends regular expressions statement to _regex_search() and returns
    #  class result

    # sends regular expressions statement to _regex_search() and returns
    # parent(s) result. Handles both Python 2 & Python 3 class declarations
    def _extract_parents(self, line):
        dependency_list = []
        regex = '^class\s\w+\((.*)\)'
        dependency_names = self._regex_search(regex, line)[0]
        regex_list = (re.split(r',', dependency_names))
        for item in regex_list:
            if item != 'object':
                stripped_item = item.strip()
                dependency_list.append(stripped_item)
        return dependency_list

    def _extract_class(self, line):
        regex = '^class\s(\w+)'
        result = self._regex_search(regex, line)
        return result

    def _extract_functions(self, line):
        regex = 'def\s(\w+)'
        return self._regex_search(regex, line)

    def _extract_attributes(self, line):
        regex = '\s{2}self\.(\w+)'
        reg1 = self._regex_search(regex, line)
        return reg1

    # allows other classes to access the component dictionary
    def get_component_dictionary(self):
        return self.component_dict



