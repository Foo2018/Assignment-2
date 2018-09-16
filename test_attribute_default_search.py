import unittest
import sys
from attribute_default_search import AttributeDefaultsSearch
import io

""" 13 unit tests to test the extractor.py class providing 100% coverage """


class MainTests(unittest.TestCase):
    """Tests for attribute_default_search.py`."""

    def setUp(self):
        self.t = AttributeDefaultsSearch()

    def test_extract_defaults_data_types(self):
        """Tests the _extract_defaults_data_types function returns a dictionary when true"""
        # Arrange
        expected = "{'obj': 'Extractor()'}"
        line = "    self.e = Extractor()"
        # Act
        actual = self.t._extract_defaults_data_types(line)
        # Assert
        self.assertEqual(str(actual), expected)

    def test_extract_defaults_data_types_no_extraction(self):

        # Arrange
        expected = ''
        line = ""
        # Act
        actual = self.t._extract_defaults_data_types(line)
        # Assert
        self.assertEqual(actual, expected)

    def test_default_value_extraction(self):
        """An attribute default value can be extracted from line of code"""
        # Arrange
        expected = 'Sharp'
        line = "    self.teeth = Sharp"
        # Act
        actual = self.t._extract_attribute_defaults(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_nil_default_value_extraction(self):
        """A value will not be extracted from line of code where no default
         present"""
        # Arrange
        expected = ''
        line = "    self.teeth = "
        # Act
        actual = self.t._extract_attribute_defaults(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_object_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'obj'
        line = "Extractor()"
        # Act
        actual = self.t._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_non_attribute_extraction(self):
        """Handles data in __init__ that have are not attributes"""
        # Arrange
        expected = []
        line = '  self.setup()'
        # Act
        actual = self.t._extract_attribute_defaults(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_string_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'str'
        line = "Sharp"
        # Act
        actual = self.t._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_string_variation_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'str'
        line = "'"
        # Act
        actual = self.t._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_dictionary_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'dict'
        line = "{"
        # Act
        actual = self.t._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_list_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'list'
        line = "["
        # Act
        actual = self.t._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_tuple_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'tuple'
        line = "("
        # Act
        actual = self.t._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_integer_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'int'
        line = '2'
        # Act
        actual = self.t._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_unknown_data_type_extraction(self):
        """An error message is raised when an unknown attribute data type is extracted from line of code"""
        # Arrange
        line = '@'
        # Assert
        saved_stdout = sys.stdout
        # Act
        try:
            out = io.StringIO()
            sys.stdout = out
            self.t._extract_attribute_data_types(line)
            output = out.getvalue()
            # assert
            self.assertEqual(output, "No data type detected for '@'\n")
        finally:
            sys.stdout = saved_stdout
