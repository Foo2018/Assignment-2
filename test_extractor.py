import unittest
import sys
from extractor import Extractor
from textsearch import TextSearch
import io
from unittest import mock

""" 33 unit tests to test the extractor.py class providing 100% coverage """


class MainTests(unittest.TestCase):
    """Tests for extractor.py`."""

    def setUp(self):
        self.e = Extractor()
        self.t = TextSearch()

    def test_unknown_file_entered(self):
        """Returns error if unknown file entered"""
        # Arrange
        saved_stdout = sys.stdout
        # Act
        try:
            out = io.StringIO()
            sys.stdout = out
            self.e.set_file("WrongFile.py")
            output = out.getvalue()
            # assert
            self.assertEqual(output, "File or directory not found\n")

        finally:
            sys.stdout = saved_stdout

    def test_file_entered(self):
        """ Tests if a correct file is entered that the _data_extraction method is called"""
        # Arrange
        patcher = mock.patch.object(self.e, '_data_extraction')
        patched = patcher.start()
        # Act
        self.e.set_file('Mammals.py')
        # Assert
        assert patched.call_count == 1
        patched.assert_called_with('Mammals.py')

    def test_folder_entered(self):
        """ Tests if a correct folder is entered that the _data_extraction
         method is called for each file found within that file tree"""
        # Arrange
        patcher = mock.patch.object(self.e, '_data_extraction')
        patched = patcher.start()
        # Act
        self.e.set_file('Folder1')
        # Assert
        assert patched.call_count == 4
        patched.assert_called_with('Folder1\\folder2\\folder3\\folder 4\\folder 5'
                                   '\\TestFile.py')

    def test_class_extraction(self):
        """A class name can be extracted from line of code"""
        # Arrange
        expected = 'Marsupial'
        line = "class Marsupial(Mammal):"
        # Act
        actual = self.t._extract_class(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_class_extraction_without_dependency(self):
        """A class name can be extracted from line of code where no parameters
         are set i.e. Python3 style"""
        # Arrange
        expected = 'Marsupial'
        line = "class Marsupial:"
        # Act
        actual = self.t._extract_class(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_nil_class_extraction(self):
        """A name will not be extracted from line of code where no class present"""
        # Arrange
        expected = []
        line = "class(Mammal):"
        # Act
        actual = self.t._extract_class(line)
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
        actual = self.t._extract_class(line)
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

    def test_extract_defaults_data_types(self):
        """Tests the _extract_defaults_data_types function returns a dictionary when true"""
        # Arrange
        expected = "{'obj': 'Extractor()'}"
        line = "    self.e = Extractor()"
        # Act
        actual = self.e._extract_defaults_data_types(line)
        # Assert
        self.assertEqual(str(actual), expected)

    def test_extract_defaults_data_types_no_extraction(self):
        """Tests the _extract_defaults_data_types function returns a dictionary when true"""
        # Arrange
        expected = ''
        line = ""
        # Act
        actual = self.e._extract_defaults_data_types(line)
        # Assert
        self.assertEqual(actual, expected)

    def test_nil_attribute_extraction(self):
        """A name will not be extracted from line of code where no attribute present"""
        # Arrange
        expected = []
        line = "    self.= 'Sharp'"
        # Act
        actual = self.t._extract_class(line)
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

    def test_data_type_string_variation_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        expected = 'str'
        line = "'"
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
        saved_stdout = sys.stdout
        # Act
        try:
            out = io.StringIO()
            sys.stdout = out
            self.e._extract_attribute_data_types(line)
            output = out.getvalue()
            # assert
            self.assertEqual(output, "No data type detected for '@'\n")
        finally:
            sys.stdout = saved_stdout

    def test_single_dependency_extraction(self):
        """Extracts a single object that class inherits from"""
        # Arrange
        expected = ["Test1"]
        line = 'class Example(Test1)'
        # Act
        actual = self.e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_object_only_dependency_(self):
        """Does not extract 'object' if it is only dependency"""
        # Arrange
        expected = []
        line = 'class Example(object)'
        # Act
        actual = self.e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_multiple_dependency_extraction(self):
        # Arrange
        expected = ["Test1", "Test2", "Test3"]
        line = 'class Example(Test1, Test2, Test3)'
        # Act
        actual = self.e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_no_class_defined_function_exception(self):
        """An error message is raised when an function is defined before its class
        due to poor coding"""
        # Arrange Act Assert
        self.assertRaises(Exception, self.e._data_extraction, "errorTestFunctions.py")

    def test_no_class_defined_attribute_exception(self):
        """An error message is raised when an attribute is defined before its class
        due to poor coding"""
        # Arrange Act Assert
        self.assertRaises(Exception, self.e._data_extraction, "errorTestAttributes.py")

    def test_class_name(self):
        expected = True
        self.e._data_extraction("mammals.py")
        if self.e.component_dict:
            actual = True
        else:
            actual = False
        self.assertEqual(actual, expected)

    def test_extractor_class_get_function(self):
        """Ensure that getter can retrieve a dictionary"""
        self.e._data_extraction("mammals.py")
        dictionary = self.e.get_component_dictionary()
        self.assertTrue(dictionary)

    def test_stub_creation(self):
        expected = True
        self.e._data_extraction("example.py")
        if self.e.component_dict:
            actual = True
        else:
            actual = False
        self.assertEqual(actual, expected)

    def test_attribute_extraction_when_no_init(self):
        expected = True
        self.e._data_extraction("NoInit.py")
        if self.e.component_dict:
            actual = True
        else:
            actual = False
        self.assertEqual(actual, expected)

    def test_attribute_declared(self):
        # Arrange
        expected = True
        # Act
        self.e._data_extraction("component.py")
        if self.e.component_dict:
            actual = True
        else:
            actual = False
        # Assert
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
