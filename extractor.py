from extraction_abstract import ExtractionAbstract
from component import Component
import os
import glob
from attribute_default_search import AttributeDefaultsSearch
from class_parameter_search import ClassParameterSearch
from parent_extraction import ParentExtraction

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

    def _data_extraction(self, file_path):
        with open(file_path, 'r') as source_file:
            search = ClassParameterSearch()
            for line in source_file:
                is_attribute_name, is_class_name, is_function_name = search.class_parameter_extractions(line)
                if is_class_name:
                    self.component = self._set_class_name(is_class_name, line)
                elif is_function_name:
                    self._place_function_name_in_component_object(is_function_name)
                elif is_attribute_name:
                    self._place_attribute_name_and_default_value_in_dictionary(is_attribute_name, line)

    def _set_class_name(self, class_name, line):
        component = Component()
        component.set_name(class_name[0])
        self._class_parent_name_handling(line, component)
        self.component_dict[class_name[0]] = component
        self.attribute_dictionary = {}
        return component

    def _class_parent_name_handling(self, line, comp):
        parent_search = ParentExtraction()
        parent = parent_search.extract_parent_classes(line)
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

    def _place_attribute_name_and_default_value_in_dictionary(self, attribute_name, line):
        try:
            if self.component.get_functions() == ['__init__']:
                attr_name = attribute_name[0]
                search = AttributeDefaultsSearch()
                self.attribute_dictionary[attr_name] = search.attribute_extraction(line)
                self.component.set_attributes(self.attribute_dictionary)
        except Exception as err:
            print(err)
            raise

    def get_component_dictionary(self):
        return self.component_dict