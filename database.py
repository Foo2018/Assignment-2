import sqlite3 as sql
import pickle
from extractor import Extractor
from sqlite3 import Error


class Database:
    def __init__(self):
        self._conn = None
        self._cursor = None
        self.db_name = None

    def create_connection(self, db_name):
        """Create a connection to SQLite Database"""
        self.db_name = db_name
        try:
            self._conn = sql.connect(db_name)
            self._cursor = self._conn.cursor()
            print("Connected to database")
            print("Database created")
            self.drop_table()
            self.create_table()
            self._conn.commit()
        except NameError:
            print("Name Error: Invalid file format for db name")
        except Error as e:
            print(e)
        finally:
            if self._conn is not None:
                self._conn.close()

    @classmethod
    def extract_data(cls, file):
        """"Uses extraction method from Extractor class"""
        ext = Extractor()
        ext.set_file(file)
        return ext.get_component_dictionary()

    def drop_table(self):
        """Drop a table called classes in the database"""
        try:
            self._cursor.execute("""DROP TABLE IF EXISTS classes;""")
            print("table dropped")
        except Error as e:
            print(e)

    def create_table(self):
        """Create a table called classes to the database"""
        sql_command = """
            CREATE TABLE IF NOT EXISTS classes (
            filename VARCHAR(20) PRIMARY KEY,
            pickled_dict BLOB);"""
        try:
            self._cursor.execute(sql_command)
            print("table created")
        except Error as e:
            print(e)

    def insert_data(self, selected_file):
        """Add pickled component data to database"""
        filename = selected_file.strip('.py')
        comp_dict = self.extract_data(selected_file)
        pickled_file = pickle.dumps(comp_dict, pickle.HIGHEST_PROTOCOL)
        conn = None
        try:
            conn = sql.connect(self.db_name)
            cursor = conn.cursor()
            sql_command = "INSERT INTO classes(filename, pickled_dict) VALUES(?, ?)"
            cursor.execute(sql_command, (filename, sql.Binary(pickled_file)))
            conn.commit()
        except Error as err:
            print("\nCannot add ", filename, " to database")
            print("The exception is: ", err)
        finally:
            if conn is not None:
                conn.close()

    def get_specific(self, selected_file):
        """Display component data of selected filename from dataabase"""
        _conn = None
        unpickled_dict = {}

        if '.py' in selected_file:
            filename = selected_file.strip('.py')
        else:
            filename = selected_file

        # return value
        output = ""
        space = "\n\t"
        format_str = "SELECT filename, pickled_dict from classes where filename='{filename}';"
        sql_command = format_str.format(filename=filename)

        try:
            _conn = sql.connect(self.db_name)
            _cursor = _conn.cursor()
            _cursor.execute(sql_command)
            result = _cursor.fetchall()
            for filename, pickled_dict in result:
                unpickled_dict = pickle.loads(pickled_dict)

        except (sql.ProgrammingError, sql.Error) as e:
            output = e
        except sql.Error as err:
            output = "Database error: " + str(err)
        except Exception as e:
            output = e
        finally:
            if _conn is not None:
                _conn.close()

        for class_name, class_data in unpickled_dict.items():
            output += "Class Name:" + class_data.name + space
            output += "Attribute:" + str(class_data.get_attributes()) + space
            output += "Function:" + str(class_data.get_functions()) + space
            output += "Parent:" + str(class_data.get_parents()) + "\n"

        return output

    def get_all(self):
        """Display all component data from database"""
        _conn = None
        unpickled_dict = {}
        # return value
        output = ""
        count = 0
        space = "\n\t"
        sql_command = "SELECT filename, pickled_dict from classes;"
        try:
            _conn = sql.connect(self.db_name)
            _cursor = _conn.cursor()
            _cursor.execute(sql_command)
            result = _cursor.fetchall()
            for filename, pickled_dict in result:
                unpickled_dict = pickle.loads(pickled_dict)
        except (sql.ProgrammingError, sql.Error) as err:
            output = "SQL Error: " + str(err)
        except sql.Error as err:
            output = "Database error: " + str(err)
        except Exception as e:
            output = str(e)
        finally:
            if _conn is not None:
                _conn.close()
        for class_name, class_data in unpickled_dict.items():
            output += "Class Name:" + class_data.name + space
            output += "Attribute:" + str(class_data.get_attributes()) + space
            output += "Function:" + str(class_data.get_functions()) + space
            output += "Parent:" + str(class_data.get_parents()) + "\n"
            count += 1
        output += "The number of components in the database: " + str(count)
        return output
