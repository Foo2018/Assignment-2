"""
This module handles the command line input and help messages for Umlify
"""

from cmd import Cmd
from shelf import Shelf
from database import Database
from umlify_component_viewer import UmlifyComponentViewer


class CommandLine(Cmd):
    """
    CommandLine class that uses Cmd
    Instead of a single command with multiple options (eg `umlify -d ./myclasses/ -o image.png`
    it will have multiple commands to set each value
    """
    db = Database()
    db.create_connection("uml_components.db")

    def __init__(self):
        """
        Testing default values are correctly assigned when CommandLine object is
        created
        >>> c = CommandLine()
        >>> print (c.prompt)
        Umlify>
        >>> print(c.input_path)
        None
        >>> print(c.output_path)
        None
        >>> print(c.allowed_types)
        ['dot', 'png', 'pdf']
        >>> print(c.output_file_type)
        dot
        >>> print(c.run)
        False
        >>> print(c.intro)
        Welcome to Umlify. Use "help" for help.
        """
        Cmd.__init__(self)
        self.prompt = "Umlify>"
        self.input_path = None
        self.output_path = None
        self.allowed_types = ["dot", "png", "pdf"]
        # default output file type .dot (first in allowed types)
        self.output_file_type = self.allowed_types[0]
        self.run = False
        self.intro = "Welcome to Umlify. Use \"help\" for help."
        self.cv = None

    def do_run(self, line):
        """
        Runs Umlify with the current file settings. Other commands are used to change them
        Press enter to activate

        """
        if not self.input_path:
            print("Please select an input path with \"file\" or \"directory\"")
            return
        self.cv = UmlifyComponentViewer(self.input_path, self.output_path)
        self.cv.generate_class_diagram()
        self.run = True
        print("Running Umlify...")

    def _check_input(self):
        """
        Check if an input has been set, if not then return a message and false
        :return: True if an input file or directory has been set, False if not
        """
        # removes duplication of this message in code
        if not self.input_path:
            print("Please select an input path with \"file\" or \"directory\"")
            return False
        else:
            return True

    def _check_run(self):
        """
        Check if the Umlify has been run, if not then return a message and false
        :return: True if run has been used, False if not
        """
        # removes duplication of this message in code
        if not self.run:
            print("Please use \"run\" before trying to create a chart")
            return False
        else:
            return True

    def do_pie(self, params):
        """
        Makes a chart about a class
        :param comp_name: the name of the class to make a chart of
        :param output_file_name: the file name for the chart to output to
        :return:
        >>> c = CommandLine()
        >>> c.do_pie('Herbivore')
        Please use "run" before trying to create a chart

        """
        if not self._check_run():
            return
        if not params:
            print("Generating pie charts for all components")
            self.cv.generate_pie_charts()
            return
        if " " in params:
            # split params into component name and output file
            comp_name, output_file_name = params.split(' ')
        else:
            comp_name = params
            output_file_name = None

            # example of comp_name: "Herbivore"
        print("Generating a pie chart for component: {comp_name}".format(comp_name=comp_name))
        self.cv.generate_pie_chart(comp_name, output_file_name)

    def do_bar(self, output_file_name):
        """
        Makes a bar chart of the current file comparing the attribute
        to function ratio of each class within that file
        :param output_file_name: the file name for the chart to output to
        :return:
        >>> c = CommandLine()
        >>> c.do_bar('mammals')
        Please use "run" before trying to create a chart

        """
        if not self._check_run():
            return
        if not output_file_name:
            output_file_name = None

        self.cv.generate_bar_chart(output_file_name)

    def do_line(self, params):
        """
        Makes a line chart of the current file comparing the attribute
        to function ratio of each class within that file
        :param output_file_name: the file name for the chart to output to
        :return:
        >>> c = CommandLine()
        >>> c.do_bar('mammals')
        Please use "run" before trying to create a chart
        """
        output_file_name = None
        if self._check_input() and params:
            output_file_name = params
        self.cv.generate_line_chart(output_file_name)

    def do_validate(self, line):
        """
        Validates a file without passing it to be drawn
        :return: None
        """
        # TODO connect to validator
        return

    def do_file(self, file):
        """
        Selects a file as input to Umlify
        :param file: the name of the file to be used as input
        :return: None
        >>> c = CommandLine()
        >>> c.do_file('test.py')
        >>> print(c.input_path)
        test.py
        >>> c.do_file('')
        Please enter 'file' or 'f' followed by a file name to use as input
        """
        if not file:
            print("Please enter 'file' or 'f' followed by a file name to use as input")
            return

        self.input_path = file

    def do_directory(self, directory):
        """
        Selects a directory as input to Umlify
        :param directory: the name of the directory holding files to be used as input
        :return: None
        >>> c = CommandLine()
        >>> c.do_directory('directory1')
        >>> print(c.input_path)
        directory1
        >>> c.do_directory('')
        Please enter 'directory' or 'd' followed by a directory name to use as input
        """
        if not directory:
            print("Please enter 'directory' or 'd' followed"
                  " by a directory name to use as input")
            return

        self.input_path = directory

    def do_location(self, location):
        """
        Selects a destination location for the output files
        :param: location
        :return: None
        >>> c = CommandLine()
        >>> c.do_location('')
        Please enter a location for output files to be saved
        """
        if not location:
            print("Please enter a location for output files to be saved")
            return

    def do_type(self, file_type):
        """
        Allows the user to define the type of file that they want the output
        to be saved as
        :param file type: type of file to be saved as
        :return:

        >>> c = CommandLine()
        >>> c.do_type("")
        Please enter a file type
        >>> c.output_file_type = 'png'
        >>> c.do_type('.png')
        The output file type is already png
        >>> c.do_type('.pdf')
        Output file type has been set to pdf
        >>> c.do_type('.jpg')
        That file type is not supported, please pick one from: dot, png, pdf
        """
        if not file_type:
            # no file type was provided
            print("Please enter a file type")
            return

        file_type = file_type.lower()  # convert to all lowercase

        # remove leading . if given (eg .png instead of png)
        if file_type[0] == ".":
            file_type = file_type[1:]

        if file_type == self.output_file_type:
            print("The output file type is already {file_type}"
                  .format(file_type=file_type))
        elif file_type in self.allowed_types:
            self.output_file_type = file_type
            print("Output file type has been set to {file_type}".format(file_type=file_type))
        else:
            # input provided was not in the list of allowed types
            print("That file type is not supported, please pick one from: {file_types}".format(
                file_types=', '.join(self.allowed_types)))

    def do_shelf(self, flag):
        """
        Writes and reads Component objects extracted from the currently selected file to [filename].shelve

        Syntax: shelf [flag] OR s [flag]
        shelf -w: writes the class components of selected file to [filename].shelve
                  User will be prompted to give a name for shelve file
        shelf -r: reads the contents of shelve file
                  User will be prompted to input name of shelve file
        :param flag: -w, -r
        :return: By default (without flag), prompted with whether user would like to write or read
        >>> c = CommandLine()
        >>> c.input_path = ""
        >>> c.do_shelf('-w')
        Please select an input path with "file" or "directory"

        """
        if not self._check_input():
            return

        shelf = Shelf(self.input_path)

        try:
            if flag == '-w':
                try:
                    shelf_name = input("Enter a name for shelve file: ")
                    if not shelf_name:
                        raise ValueError("You did not enter a name")
                    else:
                        shelf.write_shelf(shelf_name)
                except Exception:
                    raise Exception("You did not enter a name")

            elif flag == '-r':
                try:
                    shelf_name = input("Enter the name of shelve file you would like to open: ")
                    if not shelf_name:
                        raise ValueError("You did not enter a name")
                    else:
                        shelf.read_shelf(shelf_name)
                except Exception:
                    raise Exception("You did not enter a name")
            else:
                raise Exception("Not a valid flag")
        except Exception as err:
            print("The exception is: ", err)
        return

    def do_database(self, flag):
        """
        Save and read class component data with a database.

        Syntax: database [flag] OR db [flag]
        db: displays all data and the number of components stored in the database
        db -i: inserts the class components of currently selected file to the database
        db -v: displays the class components of a certain filename within the database
               User will be prompted to enter a filename
        db -d: drops the table which deletes all the class components stored
        db -c: creates a table called 'classes' to hold a filename and the component objects

        :param flag: -i, -v, -d, -c
        :return: db values
        >>> c = CommandLine()
        >>> c.input_path = ""
        >>> c.do_database('-w')
        Please select an input path with "file" or "directory"
        >>> c.input_path = "test.py"
        >>> c.do_database('-g')
        The exception is:  Not a valid flag

        """
        if not self._check_input():
            return

        try:
            if flag == "-i":
                self.db.insert_data(self.input_path)
            elif flag == "-v":
                filename = input("Enter a filename you would like to see the classes of: ")
                print(self.db.get_specific(filename))
            elif flag == "":
                print(self.db.get_all())
            else:
                raise Exception("Not a valid flag")
        except Exception as err:
            print("The exception is: ", err)
        return

    def do_quit(self, line):
        """
        Quit Umlify
        :return: True
        >>> c = CommandLine()
        >>> c.do_quit("")
        Quitting Umlify.
        True
        """
        print("Quitting Umlify.")
        return True

    # command aliases
    do_r = do_run
    do_p = do_pie
    do_b = do_bar
    do_li = do_line
    do_v = do_validate
    do_f = do_file
    do_d = do_directory
    do_l = do_location
    do_t = do_type
    do_s = do_shelf
    do_db = do_database
    do_q = do_quit


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=2)
    command_line = CommandLine()
    command_line.cmdloop()
