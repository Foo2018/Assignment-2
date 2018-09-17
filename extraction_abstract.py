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

    @abstractmethod
    def get_component_dictionary(self):
        pass
