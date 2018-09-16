from abc import ABCMeta
from abc import ABC
from abc import abstractmethod


class ExtractionAbstract(ABC):

    def __init__(self):
        self.id = None

    @abstractmethod
    def set_file(self, file_path):
        pass

    @abstractmethod
    def _data_extraction(self, file_path):
        pass

    @staticmethod
    @abstractmethod
    def _regex_search(regex, data):
        pass

    @abstractmethod
    def _extract_parents(self, line):
        pass

    @abstractmethod
    def _extract_attributes(self, line):
        pass

    @abstractmethod
    def _extract_defaults_data_types(self, line):
        pass

    @abstractmethod
    def _extract_attribute_defaults(self, line):
        pass

    @abstractmethod
    def _extract_attribute_data_types(self, attr_name):
        pass

    @abstractmethod
    def get_component_dictionary(self):
        pass
