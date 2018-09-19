from search_abstract import SearchAbstract

"""This class receives a line of text that contains an attribute name and then extracts the attribute types and
default values. It then places the result in a dictionary"""


class AttributeDefaultsSearch(SearchAbstract):
    def __init__(self):
        super().__init__()
        pass

    def attribute_extraction(self, line):
        return self._extract_defaults_and_data_types(line)

    def _extract_defaults_and_data_types(self, line):
        attr_default = self._extract_attribute_defaults(line)
        if not attr_default:
            return ''
        else:
            attr_type = self._extract_attribute_data_types(attr_default)
            def_data_types_dict = {attr_type: attr_default}
            return def_data_types_dict

    def _extract_attribute_defaults(self, line):
        regex = 'self\.\w+\s=\s(.*)'
        attribute_default = self._regex_search(regex, line)
        if attribute_default.__len__() != 0:
            attribute_default = attribute_default[0].replace('"', "")
        return attribute_default

    def _extract_attribute_data_types(self, attr_name):
        regex = '^(.)'
        regex2 = '^[A-Z].+\)$'
        extracted_type = self._regex_search(regex, attr_name)
        data_type = extracted_type[0]
        extracted_type_2 = self._regex_search(regex2, attr_name)
        if extracted_type_2:
            return 'obj'
        if data_type.isalpha():
            return 'str'
        if data_type == "'":
            return 'str'
        if data_type == '{':
            return 'dict'
        if data_type == '[':
            return 'list'
        if data_type == '(':
            return 'tuple'
        if data_type.isdigit():
            return "int"
        else:
            print("No data type detected for '{0}'".format(attr_name))
