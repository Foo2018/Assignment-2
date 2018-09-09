from component_viewer import ComponentViewer
from extractor import Extractor
import matplotlib.pyplot as plt
from numpy import arange
from graphviz import Digraph
from subprocess import CalledProcessError
from graphviz import ExecutableNotFound
from os import path, remove, makedirs


class UmlifyComponentViewer(ComponentViewer):
    def __init__(self, input_file=None, output_file=None, input_dir=None, output_dir=None):
        """
        Testing default values are correctly assigned when new Extractor object is
        created
        >>> u = UmlifyComponentViewer('mammal.py', 'mammals', 'Folder1', 'folder')
        >>> print(u.input_file)
        mammal.py
        >>> print(u.output_file)
        mammals
        >>> print(u.input_dir)
        Folder1
        >>> print(u.output_dir)
        folder
        >>> print(u.output_class_diagram)
        class-diagram
        >>> print(u.output_bar_chart)
        bar-chart
        >>> print(u.output_line_chart)
        line-chart
        >>> print(u.output_pie_chart)
        pie-chart
        >>> print(u.uml_file_output)
        <BLANKLINE>
        >>> print(u.path_provided)
        True
        """
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_class_diagram = "class-diagram"
        self.output_bar_chart = "bar-chart"
        self.output_line_chart = "line-chart"
        self.output_pie_chart = "pie-chart"
        self.uml_file_output = ""
        self.e = Extractor()
        self.path_provided = False

        if input_file is not None:
            self.e.set_file(input_file)
            self.path_provided = True

        if input_dir is not None:
            self.e.set_file(input_dir)
            self.path_provided = True

        if self.e.get_component_dictionary() is not None:
            self.components = list(self.e.get_component_dictionary().values())
        else:
            self.components = []

    def generate_class_diagram(self, output_file_name=None):
        if output_file_name is None:
            output_file_name = self.output_class_diagram
        try:
            dot = Digraph(comment='UML Class Diagram')
            dot.node_attr['shape'] = "record"
            dot.format = "dot"
            if len(self.components) > 0:
                for comp in self.components:
                    attributes = self._build_attributes_string(comp.get_attributes())
                    functions = ""
                    for funct in comp.get_functions():
                        functions += funct + "\\n"
                    record = "{"
                    record += "{name} | {attribs} |{functs}".format(name=comp.get_name(), attribs=attributes,
                                                                    functs=functions)
                    record += "}"
                    dot.node(comp.get_name(), record)
                    for parent in comp.get_parents():
                        dot.edge(parent.get_name(), comp.get_name())
                        dot.edge_attr.update(dir="back")
                        dot.edge_attr.update(arrowtail='empty')
                dot.render(output_file_name, view=False)
                self.write_dot_to_png(dot_file=output_file_name)
                if path.exists(output_file_name):
                    remove(output_file_name)
                if path.exists(output_file_name + ".dot"):
                    remove(output_file_name + ".dot")
            else:
                print("no components were found")
        except ExecutableNotFound:
            print("Graphviz executable not found, please check it is properly installed.")
        except (CalledProcessError, RuntimeError) as err:
            print("An unexpected error occurred")
            print(err)

    def generate_pie_charts(self):
        for comp in self.e.get_component_dictionary().keys():
            self.generate_pie_chart(comp)

    def generate_pie_chart(self, comp_name, output_file_name=None):
        if not path.exists(self.output_path):
            makedirs(self.output_path)
        comp_name = comp_name[0].upper() + comp_name[1:]
        if output_file_name is None:
            output_file_name = comp_name + '-' + self.output_pie_chart

        the_component = self.e.get_component_dictionary().get(comp_name)
        att_types = self._get_attribute_types(the_component)
        removable = []
        for k, v in att_types.items():
            if v == 0:
                removable.append(k)
        for r in removable:
            att_types = self._remove_by_key(att_types, r)

        if len(att_types) > 0:
            labels = att_types.keys()
            sizes = att_types.values()
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title("Percentage of variable data types")
            plt.axis('equal')
            plt.savefig(self.output_path + output_file_name + ".png")
            plt.gcf().clear()
        else:
            print("No attributes found for class: " + comp_name)

    def generate_bar_chart(self, output_file_name=None):
        if not path.exists(self.output_path):
            makedirs(self.output_path)
        if output_file_name is None:
            output_file_name = self.output_bar_chart
        bar_width = 0.35
        opacity = 0.8
        objects = tuple(self.e.get_component_dictionary().keys())
        no_of_attributes = []
        no_of_functions = []
        for key in objects:
            component = self.e.get_component_dictionary().get(key)
            no_of_attributes.append(len(component.get_attributes()))
            no_of_functions.append(len(component.get_functions()))
        y_pos = arange(len(objects))

        plt.bar(y_pos, no_of_attributes, bar_width, alpha=opacity, color='b', label='attributes')
        plt.bar(y_pos + bar_width, no_of_functions, bar_width, alpha=opacity, color='g', label='functions')
        plt.xticks(y_pos + bar_width, objects, rotation=90)
        plt.subplots_adjust(bottom=0.30)
        plt.ylabel('Count')
        plt.xlabel('Class Name')
        plt.title('Number of Functions and Attributes per Class')
        plt.legend()

        plt.savefig(self.output_path + output_file_name + ".png")
        plt.gca().clear()

    def generate_line_chart(self, output_file_name=None):
        if not path.exists(self.output_path):
            makedirs(self.output_path)
        if output_file_name is None:
            output_file_name = self.output_line_chart
        line_width = 2.0
        opacity = 0.8
        objects = tuple(self.e.get_component_dictionary().keys())
        no_of_attributes = []
        no_of_functions = []
        for key in objects:
            component = self.e.get_component_dictionary().get(key)
            no_of_attributes.append(len(component.get_attributes()))
            no_of_functions.append(len(component.get_functions()))
        y_pos = arange(len(objects))

        plt.plot(y_pos, no_of_attributes, line_width, alpha=opacity, color='b', label='attributes')
        plt.plot(y_pos, no_of_functions, line_width, alpha=opacity, color='r', label='functions')
        plt.xticks(y_pos, objects, rotation=90)
        plt.subplots_adjust(bottom=0.30)
        plt.grid()
        plt.ylabel('Count')
        plt.xlabel('Class Name')
        plt.title('Number of Functions and Attributes per Class')
        plt.legend(loc=9)

        plt.savefig(self.output_path + output_file_name + ".png")
        plt.gca().clear()

    def _get_attribute_types(self, component):
        att_types = {"int": 0, "str": 0, "dict": 0, "list": 0, "tuple": 0, "object": 0}
        attributes = component.get_attributes()
        if len(attributes) > 0:
            for attrib in attributes:
                for a in attributes[attrib]:
                    att_types[a] = att_types[a] + 1
        return att_types

    def _remove_by_key(self, dictionary, key):
        r = dict(dictionary)
        del r[key]
        return r

    def _build_attributes_string(self, attributes):
        attribute_string = ""
        for attrib in attributes:
            attribute_string += attrib
            for a in attributes[attrib]:
                attribute_string += " : " + a
            attribute_string += "\\n"
        return attribute_string


if __name__ == "__main__":
    import doctest
    doctest.testmod()
