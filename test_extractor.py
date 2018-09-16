import unittest
import sys
from extractor import Extractor
from attribute_default_search import AttributeDefaultsSearch
import io
from unittest import mock

""" 20 unit tests to test the extractor.py class providing 100% coverage """


class MainTests(unittest.TestCase):
    """Tests for extractor.py`."""

    def setUp(self):
        self.e = Extractor()
        self.t = AttributeDefaultsSearch()

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

    def test_function_extraction(self):
        """A function name can be extracted from line of code"""
        # Arrange
        expected = 'proliferates'
        line = "def proliferates(self):"
        # Act
        actual = self.e._extract_functions(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_attribute_extraction(self):
        """An attribute name can be extracted from line of code"""
        # Arrange
        expected = 'teeth'
        line = "    self.teeth = 'Sharp'"
        # Act
        actual = self.e._extract_attributes(line)
        # Assert
        self.assertEqual([expected], actual)

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
