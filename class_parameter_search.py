import re

"""
This module searches the initial line data and decides if there are classnames, 

"""


class ClassParameterSearch(object):
    def __init__(self):
        self.parameter_list = []

    def class_parameter_extractions(self, line):
        is_class_name = self._extract_class(line)
        is_function_name = self._extract_functions(line)
        is_attribute_name = self._extract_attributes(line)
        return is_attribute_name, is_class_name, is_function_name

    @staticmethod
    def _regex_search(regex, data):
        r = re.compile(regex)
        regex_result = r.findall(data)
        return regex_result

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

