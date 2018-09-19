import unittest
import sys
from extractor import Extractor
import io
from unittest import mock

""" 10 unit tests to test the extractor.py class providing 100% coverage """


class MainTests(unittest.TestCase):
    """Tests for extractor.py`."""

    def setUp(self):
        self.e = Extractor()

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

    def test_master(self):
        """Tests the happy day scenario of an error free file being presented to the program"""
        expected = True
        self.e.set_file("mammals.py")
        if len(self.e.component_dict) > 0:
            actual = True
        else:
            actual = False
        self.assertEqual(expected, actual)

    def test_master_error(self):
        """Tests the bad day scenario of a file with syntax errors being presented"""
        expected = True
        self.e.set_file("mammals_attribute_error.py")
        if len(self.e.component_dict) > 0:
            actual = True
        else:
            actual = False
        self.assertEqual(expected, actual)

    def test_file_entered(self):
        """ Tests if a correct FILE is entered that the _data_extraction method is called"""
        # Arrange
        patcher = mock.patch.object(self.e, '_data_extraction')
        patched = patcher.start()
        # Act
        self.e.set_file('Mammals.py')
        # Assert
        assert patched.call_count == 1
        patched.assert_called_with('Mammals.py')

    def test_folder_entered(self):
        """ Tests if a correct FOLDER is entered that the _data_extraction
         method is called for each file found within that folder file tree"""
        # Arrange
        patcher = mock.patch.object(self.e, '_data_extraction')
        patched = patcher.start()
        # Act
        self.e.set_file('Folder1')
        # Assert
        assert patched.call_count == 4
        patched.assert_called_with('Folder1\\folder2\\folder3\\folder 4\\folder 5'
                                   '\\TestFile.py')

    def test_stub_creation(self):
        """ Tests that a stub class is created if a parent class is found that does not have a concrete
        class created within the known file"""
        expected = True
        self.e.set_file("example.py")
        dict_method = self.e.get_component_dictionary()
        dictionary = vars(dict_method['Aframe'])
        if dictionary['parents']:
            actual = True
        else:
            actual = False
        self.assertEqual(expected, actual)

    def test_attribute_extraction_when_no_init(self):
        """Test to ensure only attributes declared in an __init__ method are extracted"""
        expected = True
        self.e.set_file("no_init.py")
        dict_method = self.e.get_component_dictionary()
        dictionary = vars(dict_method['Alpha'])
        if not dictionary['attributes']:
            actual = True
        else:
            actual = False
        self.assertEqual(expected, actual)

    def test_no_class_defined_function_exception(self):
        """An error message is raised when an function is defined before its class
        due to poor coding"""
        # Arrange Act Assert
        self.assertRaises(Exception, self.e.set_file, "errorTestFunctions.py")

    def test_no_class_defined_attribute_exception(self):
        """An error message is raised when an attribute is defined before its class
        due to poor coding"""
        # Arrange Act Assert
        self.assertRaises(Exception, self.e.set_file, "errorTestAttributes.py")

    def test_extractor_class_get_function(self):
        """Ensure that getter can retrieve a dictionary"""
        self.e.set_file("mammals.py")
        dictionary = self.e.get_component_dictionary()
        self.assertTrue(dictionary)


if __name__ == '__main__':
    unittest.main(verbosity=2)
