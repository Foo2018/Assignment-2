import unittest
from commandline import CommandLine



"""Ten unit tests to test the extractor.py class, primarily the regex extractions"""


class MainTests(unittest.TestCase):
    """Tests for commandline.py`."""

    def setUp(self):
        self.c = CommandLine()

    def test_class_extraction(self):
        """A class name can be extracted from line of code"""
        # Arrange
        expected = 'Marsupial'
        line = "class Marsupial(Mammal):"
        # Act
        actual = self.e._extract_class(line)
        # Assert
        self.assertEqual([expected], actual)