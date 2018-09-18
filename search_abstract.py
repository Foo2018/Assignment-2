from abc import ABC
import re


class SearchAbstract(ABC):

    @staticmethod
    def _regex_search(regex, data):
        r = re.compile(regex)
        regex_result = r.findall(data)
        return regex_result
