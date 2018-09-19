import re
from search_abstract import SearchAbstract

"""
This class receives a line containing a class name and extracts parent classes, if there are any to extract

"""


class ParentExtraction(SearchAbstract):
    def __init__(self):
        self.dependency_list = []

    def extract_parent_classes(self, line):
        self._extract_parents(line)
        return self.get_dependency_list()

    def _extract_parents(self, line):
        regex = '^class\s\w+\((.*)\)'
        dependency_names = self._regex_search(regex, line)[0]
        regex_list = (re.split(r',', dependency_names))
        return self.add_parent_to_list(regex_list)

    def add_parent_to_list(self, regex_list):
        for item in regex_list:
            if item != 'object':
                stripped_item = item.strip()
                self.dependency_list.append(stripped_item)

    def get_dependency_list(self):
        return self.dependency_list
