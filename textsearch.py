import re
from extraction_abstract import ExtractionAbstract
from component import Component
import os
import glob

""" 
This module receives data from files or folders then
extracts class names, dependencies, function names and attribute details.
For each class it creates a new Component object and places the above details
in that object. This module then outputs a dictionary containing the 
Component objects for that file/folder    

"""


class TextSearch(object):
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