from pylint import run_pyreverse
from component_viewer import ComponentViewer


class PyreverseComponentViewer(ComponentViewer):

    def __init__(self):
        super().__init__()

    def generate_class_diagram(self):
        try:
            run_pyreverse()
        finally:
            self._write_dot_to_png("classes.dot", "classes.png")
            self._write_dot_to_png("packages.dot")
            return "pyreverse has been run"

    def generate_pie_charts(self):
        raise NotImplementedError('generate_pie_charts has not been implemented in the PyreverseComponentViewer class')

    def generate_pie_chart(self, class_name):
        raise NotImplementedError('generate_pie_chart has not been implemented in the PyreverseComponentViewer class')
        pass

    def generate_bar_chart(self):
        raise NotImplementedError('generate_bar_chart has not been implemented in the PyreverseComponentViewer class')
        pass

    def _write_dot_to_png(self, dot_file, output=None):
        return super().write_dot_to_png(dot_file, output)


if __name__ == "__main__":
    pcv = PyreverseComponentViewer()
    pcv.generate_class_diagram()
    try:
        pcv.generate_bar_chart()
    except NotImplementedError as err:
        print(err)
