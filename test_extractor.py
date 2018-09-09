import unittest
from extractor import Extractor
from component import Component

"""Ten unit tests to test the extractor.py class, primarily the regex extractions"""


class MainTests(unittest.TestCase):
    """Tests for extractor.py`."""

    def setUp(self):
        self.e = Extractor()

    @unittest.skip('This is not functioning yet.')
    def test_unknown_file_entered(self):
        """Returns error if unknown file entered"""
        # Arrange
        expected = 'File not found'
        line = "wrongfile.py"
        # Act
        actual = self.e.set_file(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_class_extraction(self):
        """A class name can be extracted from line of code"""
        # Arrange
        expected = 'Marsupial'
        line = "class Marsupial(Mammal):"
        # Act
        actual = self.e._extract_class(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_class_extraction_without_dependency(self):
        """A class name can be extracted from line of code where no parameters
         are set i.e. Python3 style"""
        # Arrange
        expected = 'Marsupial'
        line = "class Marsupial:"
        # Act
        actual = self.e._extract_class(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_nil_class_extraction(self):
        """A name will not be extracted from line of code where no class present"""
        # Arrange
        expected = []
        line = "class(Mammal):"
        # Act
        actual = self.e._extract_class(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_function_extraction(self):
        """A function name can be extracted from line of code"""
        # Arrange
        expected = 'proliferates'
        line = "def proliferates(self):"
        # Act
        actual = self.e._extract_functions(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_nil_function_extraction(self):
        """A name will not be extracted from line of code where no function present"""
        # Arrange
        expected = []
        line = "    teeth = 'Sharp'"
        # Act
        actual = self.e._extract_class(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_attribute_extraction(self):
        """An attribute name can be extracted from line of code"""
        # Arrange
        expected = 'teeth'
        line = "    self.teeth = 'Sharp'"
        # Act
        actual = self.e._extract_attributes(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_nil_attribute_extraction(self):
        """A name will not be extracted from line of code where no attribute present"""
        # Arrange
        expected = []
        line = "    self.= 'Sharp'"
        # Act
        actual = self.e._extract_class(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_default_value_extraction(self):
        """An attribute default value can be extracted from line of code"""
        # Arrange
        expected = 'Sharp'
        line = "    self.teeth = Sharp"
        # Act
        actual = self.e._extract_attribute_defaults(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_nil_default_value_extraction(self):
        """A value will not be extracted from line of code where no default
         present"""
        # Arrange
        expected = ''
        line = "    self.teeth = "
        # Act
        actual = self.e._extract_attribute_defaults(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_object_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'obj'
        line = "Extractor()"
        # Act
        actual = self.e._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_non_attribute_extraction(self):
        """Handles data in __init__ that have are not attributes"""
        # Arrange
        expected = []
        line = '  self.setup()'
        # Act
        actual = self.e._extract_attribute_defaults(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_string_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'str'
        line = "Sharp"
        # Act
        actual = self.e._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_dictionary_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'dict'
        line = "{"
        # Act
        actual = self.e._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_list_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'list'
        line = "["
        # Act
        actual = self.e._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_tuple_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'tuple'
        line = "("
        # Act
        actual = self.e._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_integer_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'int'
        line = '2'
        # Act
        actual = self.e._extract_attribute_data_types(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_unknown_data_type_extraction(self):
        """An error message is raised when an unknown attribute data type is extracted from line of code"""
        # Arrange
        line = '@'
        # Assert
        with self.assertRaises(Exception):
            self.e._extract_attribute_data_types(line)

    def test_single_dependency_extraction(self):
        """Extracts a single object that class inherits from"""
        # Arrange
        expected = ["Test1"]
        line = 'class Example(Test1)'
        # Act
        actual = self.e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_multiple_dependency_extraction(self):
        """Does not extract 'object' if it is only dependency"""
        # Arrange
        expected = []
        line = 'class Example(object)'
        # Act
        actual = self.e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_object_dependency_(self):
        # Arrange
        expected = ["Test1", "Test2", "Test3"]
        line = 'class Example(Test1, Test2, Test3)'
        # Act
        actual = self.e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    @unittest.skip('This is not functioning yet.')
    def test_no_class_defined_exception(self):
        """An error message is raised when an function is defined before its class
        due to poor coding"""
        # Arrange
        file = 'errortest.py'
        # Act
        self.assertRaises(Exception, self.e._data_extraction, file)

    @unittest.skip('This is not functioning yet.')
    def test_name_attribute_set(self):
        # Arrange
        c = Component()
        self.e.set_file('Component.py')
        expected = 'Component'
        # Act
        actual = c.get_name()
        print("########actual = %s" % actual)
        # Assert
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
