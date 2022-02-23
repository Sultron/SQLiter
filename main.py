"""Author: Rohman Sultan
   Date:   02/20/2022
   Course: CS 457
   Programming Assignment: #1
"""

import sys # Module to read standard input
import os # Module to check directories and files
import re # Module to parse query from user


class SQLiter:
    """
    A class to represent my implementation of a database.

     Attributes
    ----------
    selected_database : str
        Current database in use.
    match_drop_or_create_database : str
        A regular expression to match user query for dropping or creating a database.
    match_select_from : str
        A regular expression to match user query for querying a table.
    match_create_table : str
        A regular expression to match user query for creating a table.
    match_drop_table : str
        A regular expression to match user query for dropping a table.
    match_alter_table : str
        A regular expression to match user query for altering a table.
    match_use_statement : str
        A regular expression to match user query for use statement.
    match_parameters : str
        A regular expression to match parameters.




    Methods
    -------
    user_prompt():
        Runs the SQLiter editor
     match_query(query):
        Finds out what the user is requesting from the query.
     does_file_exist(name):
        Checks if file (table) exists with the supplied name.
     does_directory_exist(name):
        Checks if directory (database) exists with the supplied name.
     create_database(name):
        Creates a database (directory) with the supplied name.
     create_table(name):
        Creates a table (file) with the supplied name.
     alter_table(name, clause_type, payload):
        Alters a table with the supplied name based on the clause type (add, modify, drop).
     drop_table(name):
        Deletes a table (file) with the supplied name.
     drop_database(name):
        Deletes a database (directory) with the supplied name.
     query_table(name):
        Queries a table with the supplied name.
     select_database(name):
        Sets the database with supplied name.
     run_query(query):
        Starts the process of interpreting the user's query.



    """

    def __init__(self):
        self.selected_database = None
        self.match_drop_or_create_database = r'^\s*(drop|create)\s+database\s+(\w+);?'
        self.match_select_from = r'^\s*select\s+(\*|(?:\w+\s*,?\s*)+)\s+from\s+(\w+);?'
        self.match_create_table = r'^\s*create\s+table\s+(\w+)\s*\((.+)\);?$'
        self.match_drop_table = r'^\s*drop\s+table\s+(\w+);?'
        # self.match_alter_table = r'^\s*alter\s+table\s+(\w+)\s+(\w+)\s+((\w+)\s+((?:int|float|(?:var)?char\(\d+\))))\s*;?$'
        self.match_alter_table = r'^\s*alter\s+table\s+(\w+)\s+((add)\s+((\w+)\s+((?:int|float|(?:var)?char\(\d+\))))\s*|(modify)\s+((\w+)\s+((?:int|float|(?:var)?char\(\d+\))))\s*|(drop)\s+(\w+)\s*);?$'
        self.match_use_statement = r'^\s*use\s+(\w+);?'
        self.match_parameters = r'(\w+)\s+((?:int|float|(?:var)?char\(\d+\)))'
        self.match_comments = r'\s*--.*'
        self.user_prompt()

    def match_query(self, query):
        # Checks if user wants to create to drop a database.
        case_1 = re.search(self.match_drop_or_create_database, query, re.I)
        if case_1:
            if case_1.group(1).strip().lower() == 'create':
                self.create_database(case_1.group(2))
                return
            else:
                self.drop_database(case_1.group(2))
                return

        # Checks if user wants to select a database.
        case_2 = re.search(self.match_use_statement, query, re.I)
        if case_2:
            self.select_database(case_2.group(1))
            return

        # Checks if user wants to create a table.
        case_3 = re.search(self.match_create_table, query, re.I)
        if case_3:
            if not self.selected_database:
                print('No database has been selected.')
                return

            name = case_3.group(1).strip()

            params = re.findall(self.match_parameters, case_3.group(2), re.I)
            if len(params) == 0:
                print('malformed parameters')
                return

            self.create_table(name, params)
            return

        # Checks if user wants to query a table.
        case_4 = re.search(self.match_select_from, query, re.I)
        if case_4:
            if not self.selected_database:
                print('No database has been selected.')
                return

            columns = case_4.group(1).strip()
            name = case_4.group(2).strip()
            self.query_table(name)
            return

        # Checks if user wants to drop a table.
        case_5 = re.search(self.match_drop_table, query, re.I)
        if case_5:
            if not self.selected_database:
                print('No database has been selected.')
                return

            table_name = case_5.group(1)
            self.drop_table(table_name)
            return

        # Checks if user wants to alter a table.
        case_6 = re.search(self.match_alter_table, query, re.I)
        if case_6:
            if not self.selected_database:
                print('No database has been selected.')
                return

            if case_6.group(3):
                clause = 'add'
                payload = case_6.group(4)
            elif case_6.group(7):
                clause = 'modify'
                payload = case_6.group(8)
            else:
                clause = 'drop'
                payload = case_6.group(2)
            name = case_6.group(1).strip()
            self.alter_table(name, clause, payload)
            return

        print('Bad input.') # No matches 

    @staticmethod
    def does_file_exist(name):
        return os.path.exists(f'{name}')

    @staticmethod
    def does_directory_exist(name):
        return os.path.isdir(name)

    def create_database(self, name):
        # file_exists = self.does_file_exist(name + '.sql')
        directory_exists = self.does_directory_exist(name)
        if directory_exists:
            print(f'!Failed to create database {name} because it already exists.')
            return

        os.mkdir(name)

        print(f'Database {name} created.')

    def create_table(self, name, params):
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)
        if table_exists:
            print(f'!Failed to create table {name} because it already exists.')
            return

        with open(table_path, 'w') as f:
            header = ''
            for param in params:
                header += f'{param[0].strip()} {param[1].strip()}|'
            header = header[:-1]
            f.write(header)
            print(f'Table {name} created.')

    def alter_table(self, name, clause_type, payload):
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)

        if not table_exists:
            print(f'!Failed to alter table because it does not exist.')
            return

        payload = payload.strip()
        payload = ' '.join(payload.split())

        if clause_type == 'add':
            with open(f'{self.selected_database}/{name}.csv', 'r+') as f:
                file_contents = f.readlines()
                file_contents[0] += '|' + payload
                body = ''.join(file_contents)
                f.seek(0)
                f.write(body)
                f.truncate()
            print(f'Table {name} modified.')
            return

        if clause_type == 'modify':
            print('Modify feature not implemented.')
            return

        if clause_type == 'drop':
            print('Drop feature not implemented.')
            return

        
        print('Unknown clause')

    def drop_table(self, name):
        table_path = f'{self.selected_database}/{name}.csv'
        file_exists = self.does_file_exist(table_path)

        if not file_exists:
            print(f'!Failed to delete {name} because it does not exist.')
            return

        os.remove(table_path)
        print(f'Table {name} deleted.')

    def drop_database(self, name):
        # file_exists = self.does_file_exist(name + '.sql')
        directory_exists = self.does_directory_exist(name)

        if not directory_exists:
            print(f'!Failed to delete {name} because it does not exist.')
            return

        for f in os.listdir(name):
            os.remove(os.path.join(name, f))

        os.rmdir(name)

        print(f'Database {name} deleted.')

    def query_table(self, name):
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)
        if not table_exists:
            print(f'!Failed to query table {name} because it does not exist.')
            return

        with open(table_path) as tb:
            rows = tb.readlines()
            for row in rows:
                print(row)

    def select_database(self, name):
        database_exists = self.does_directory_exist(name)
        if not database_exists:
            print(f'Failed to select database {name} because it does not exist.')
            return
        self.selected_database = name
        print(f'Using database {name}.')

    def run_query(self, query):
        """Accepts SQL query """
        self.match_query(query)

    def user_prompt(self):
        """Runs SQLiter editor."""
        print('\n--> ', end='')
        for line in sys.stdin:
            print('\n')
            if re.search(self.match_comments, line.strip(), re.I) or not line.strip(): # Ignore comments and empty lines
                continue

            if ".exit" == line.rstrip().lower():
                print('All done')
                break

            self.run_query(line.strip())
            print('\n--> ', end='')


if __name__ == '__main__':
    sql = SQLiter()
    
