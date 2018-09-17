import re


class AttributeDefaultsSearch(object):
    def __init__(self):
        pass

    def attribute_extraction(self, line):
        return self._extract_defaults_and_data_types(line)

    @staticmethod
    def _regex_search(regex, data):
        r = re.compile(regex)
        regex_result = r.findall(data)
        return regex_result

    def _extract_defaults_and_data_types(self, line):
        attr_default = self._extract_attribute_defaults(line)
        if not attr_default:
            return ''
        else:
            attr_type = self._extract_attribute_data_types(attr_default)
            def_data_types_dict = {attr_type: attr_default}
            return def_data_types_dict

    # Extracts default value(s) from an attribute and returns them
    def _extract_attribute_defaults(self, line):
        regex = '\s{2}self\.\w+\s=\s(.*)'
        attribute_default = self._regex_search(regex, line)
        if attribute_default.__len__() != 0:
            attribute_default = attribute_default[0].replace('"', "")
        return attribute_default

    # Identifies attribute data type returns it
    def _extract_attribute_data_types(self, attr_name):
        regex = '^(.)'
        regex2 = '^[A-Z].+\)$'
        extracted_type = self._regex_search(regex, attr_name)
        data_type = extracted_type[0]
        extracted_type_2 = self._regex_search(regex2, attr_name)
        if extracted_type_2:
            return 'obj'
        elif data_type.isalpha():
            return 'str'
        elif data_type.isdigit():
            return "int"
        elif data_type:
            character = {"'": "str", '{': 'dict', '[': 'list', '(': 'tuple'}
            return character[data_type][1]

        else:
            print("No data type detected for '{0}'".format(attr_name))

