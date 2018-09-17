import re

"""


"""


class ParentExtraction(object):
    def __init__(self):
        self.dependency_list = []
        self.line_text = ""

    def extract_parent_classes(self, line):
        self.line_text = line
        self._extract_parents()
        return self.get_dependency_list()

    def _regex_search(self, regex):
        r = re.compile(regex)
        regex_result = r.findall(self.line_text)
        return regex_result

    def _extract_parents(self):
        regex = '^class\s\w+\((.*)\)'
        dependency_names = self._regex_search(regex)[0]
        regex_list = (re.split(r',', dependency_names))
        return self.add_parent_to_list(regex_list)

    def add_parent_to_list(self, regex_list):
        for item in regex_list:
            if item != 'object':
                stripped_item = item.strip()
                self.dependency_list.append(stripped_item)

    def get_dependency_list(self):
        return self.dependency_list
