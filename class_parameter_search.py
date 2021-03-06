from search_abstract import SearchAbstract

"""
This class searches the initial line data and extracts class parameters within those lines 
(class, names, function names and attribute names)

"""


class ClassParameterSearch(SearchAbstract):
    def __init__(self):
        super().__init__()
        self.parameter_list = []

    def class_parameter_extractions(self, line):
        is_class_name = self._extract_class(line)
        is_function_name = self._extract_functions(line)
        is_attribute_name = self._extract_attributes(line)
        return is_attribute_name, is_class_name, is_function_name

    def _extract_class(self, line):
        regex = '^class\s(\w+)'
        result = self._regex_search(regex, line)
        return result

    def _extract_functions(self, line):
        regex = 'def\s(\w+)'
        return self._regex_search(regex, line)

    def _extract_attributes(self, line):
        regex = 'self\.(\w+)'
        reg1 = self._regex_search(regex, line)
        return reg1
