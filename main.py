"""Author: Rohman Sultan
   Date:   05/05/2022
   Course: CS 457
   Programming Assignment: #4
"""

import sys
import os
import re


class SQLiter:
    """
    A class to represent my implementation of a database.

     Attributes
    ----------
    selected_database : str
        Current database in use.
    is_table_locked : bool

    match_drop_or_create_database : str
        A regular expression to match user query for dropping or creating a database.
    match_select_from : str
        A regular expression to match user query for querying table.
    match_modification : str
        A regular expression to match write operation queries.
    match_join : str
        A regular expression to match join operations
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
    match_insert : str
        A regular expression to match user query for inserting a record into a table.
    match_parameter_values : str
        A regular expression to match values from query.
    match_parameter_values : str
        A regular expression to match parameter values from query.
    match_update : str
        A regular expression to match user query for updating a record from a table.
    match_delete : str
        A regular expression to match user query for deleting a record from a table.
    match_where : str
        A regular expression to match user query for where statement.
    op : dict
        Map operators to functions.









    Methods
    -------
    user_prompt():
        Runs the SQLiter editor
     match_query(query):
        Finds out what the user is requesting from the query.
    query_join(names, where_statement, join_type, columns)
        Perfroms join operations.
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
    delete_record(name, where_statement):
        Deletes the record with the supplied name and where statement.
    insert_record(name, where_statement):
        Inserts the record with the supplied name and where statement.
    update_record(self, name, set_identifier, set_value, where_statement):
        Updates a record with the supplied name set identifier, set value and where statement.
    selected_columns(rows, indices):
        Prints the columns selected
    util_func(param):
        Converts value type to the appropriate type
    """

    def __init__(self):
        self.selected_database = None
        self.is_table_locked = ('', False)
        self.match_drop_or_create_database = r'^\s*(drop|create)\s+database\s+(\w+);?'
        self.match_select_from = r'^\s*select\s+(\*|(?:\w+\s*,?\s*)+)\s+from\s+(\w+)\s*(.*);?'
        self.match_join = r'^\s*select\s+(\*|(?:\w+\s*,?\s*)+)\s+from\s+(\w+)\s*(\w+)(\s+inner\s+join\s+|\s+left\s+outer\s+join\s+|\s*,)\s*(\w+)\s+(\w+)\s+((where|on)\s+(\w+\.\w+)\s*(!?=|>=?|<=?)\s*(\w+\.\w+))\s*;?'
        self.match_create_table = r'^\s*create\s+table\s+(\w+)\s*\((.+)\);?$'
        self.match_drop_table = r'^\s*drop\s+table\s+(\w+);?'
        # self.match_alter_table = r'^\s*alter\s+table\s+(\w+)\s+(\w+)\s+((\w+)\s+((?:int|float|(?:var)?char\(\d+\))))\s*;?$'
        self.match_alter_table = r'^\s*alter\s+table\s+(\w+)\s+((add)\s+((\w+)\s+((?:int|float|(?:var)?char\(\d+\))))\s*|(modify)\s+((\w+)\s+((?:int|float|(?:var)?char\(\d+\))))\s*|(drop)\s+(\w+)\s*);?$'
        self.match_use_statement = r'^\s*use\s+(\w+);?'
        self.match_parameters = r'(\w+)\s+((?:int|float|(?:var)?char\(\d+\)))'
        self.match_insert = r'^\s*insert\s+into\s+(\w+)\s+values\s*\((.+)\)\s*;?'
        self.match_parameter_values = r'\s*([^,]+)\s*'
        self.match_modification = r'update\s+(\w+)|delete\s+from\s+(\w+)|insert\s+into\s+(\w+)|alter\s+table\s+(\w+)|drop\s+table\s+(\w+)'
        self.match_update = r'^\s*update\s+(.+)\s+set\s+(\w+)\s*=\s*([^;][\w.-_\'\"]+)\s*(.*)\s*(?:;)'
        self.match_delete = r'^\s*delete\s+from\s+(\w+)\s*(;|\s+where\s+(.*)\s*;)'
        self.match_where = r'^\s*where\s+(.+)\s+(!?=|>=?|<=?)\s+(.+)\s*;?'
        self.op = {  # where statement operators, maps a string operator to a function.
            '<': lambda x, y: x < y,
            '<=': lambda x, y: x <= y,
            '>': lambda x, y: x > y,
            '>=': lambda x, y: x >= y,
            '=': lambda x, y: x == y,
            '!=': lambda x, y: x != y
        }
        self.user_prompt()  # Prompts the SQL CLI

    def match_query(self, query):
        query1 = re.search(self.match_drop_or_create_database, query, re.I)
        if query1:  # Is user wanting to create or drop a database?
            if query1.group(1).strip().lower() == 'create':  # Check if user wanting to create a database.
                self.create_database(query1.group(2))
                return
            else:
                self.drop_database(query1.group(2))  # Otherwise, user is wanting to drop a database.
                return

        query2 = re.search(self.match_use_statement, query, re.I)
        if query2:  # Is user wanting to select a database?
            # print(query2.group(1))
            self.select_database(query2.group(1))  # Select the database user is requesting if it exists.
            return

        query3 = re.search(self.match_create_table, query, re.I)
        if query3:  # Is user wanting to create a table?
            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know a database has not been selected.
                return
            name = query3.group(1).strip()  # Get the name of the table.

            params = re.findall(self.match_parameters, query3.group(2), re.I)  # Get the metadata table parameters
            if len(params) == 0:  # Are there any metadata table parameters?
                print(f'malformed parameters')  # Let the user know there are malformed parameters in the table.
                return

            self.create_table(name, params)  # create the table.
            return

        query10 = re.search(self.match_join, query, re.I)
        if query10:  # Is user wanting to perform a join operation?
            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know that no database has been selected.
                return
            t1 = query10.group(2).strip()  # Get the name of left table.
            t1_alias = query10.group(3).strip()  # Get the alias of the left table name.
            t2 = query10.group(5).strip()  # The the name of right table.
            t2_alias = query10.group(6).strip()  # Get the alias of the right table name.
            join_type = query10.group(4).strip()  # Get the type of join operation.
            join_type = re.sub(r'\s+', ' ', join_type)  # Remove excess spaces.
            names = [(t1, t1_alias), (t2, t2_alias)]  # Store each table with their aliases.
            where_statement = query10.group(7).strip()  # Get the where clause.
            columns = query10.group(1).strip()  # The the column names.
            columns = columns.split(',')  # Get each token
            columns = list(map(lambda x: x.strip(), columns))  # Remove trailing and leading spaces
            for name in names:
                if name[1]:
                    where_statement = where_statement.replace(f'{name[1]}.',
                                                              f'{name[0]}.')  # Replace alias with the actual table name if present.
            where_statement = re.sub(r'\s+', ' ', where_statement).split(' ')  # Remove excess spaces.
            where_statement.pop(0)  # Remove 'where' from list.
            self.query_join(names, where_statement, join_type, columns)  # Perform the join operation.
            return

        query4 = re.search(self.match_select_from, query, re.I)
        if query4:  # Is the user wanting to query a table?
            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know that no database has been selected.
                return
            # print(query4.groups())
            columns = query4.group(1).strip()
            columns = columns.split(',')
            columns = list(map(lambda x: x.strip(), columns))
            name = query4.group(2).strip()  # Get the table name.
            where_statement = re.search(self.match_where, query4.group(3).strip(), re.I)
            self.query_table(name, columns, where_statement)  # Query the table.
            return

        query5 = re.search(self.match_drop_table, query, re.I)
        if query5:  # Is user wanting to drop a table?
            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know that no database has been selected.
                return
            table_name = query5.group(1)  # Get the table name.
            self.drop_table(table_name)  # Drop the table if it exists.
            return

        query6 = re.search(self.match_alter_table, query, re.I)
        if query6:  # Is user wanting to alter a table?
            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know that no database has been selected.
                return

            # Find what type of altering user is requesting.
            if query6.group(3):
                clause = 'add'
                payload = query6.group(4)
            elif query6.group(7):
                clause = 'modify'
                payload = query6.group(8)
            else:
                clause = 'drop'
                payload = query6.group(2)
            name = query6.group(1).strip()  # Get table name.
            self.alter_table(name, clause, payload)  # alter the table.
            return

        query7 = re.search(self.match_insert, query, re.I)

        if query7:  # Is user wanting to insert a record to a table?
            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know that no database has been selected.
                return
            name = query7.group(1).strip()  # Get the name of the table.
            params = re.findall(self.match_parameter_values, query7.group(2), re.I)  # Get the parameter values.
            params = list(map(lambda x: x[1:len(x) - 1] if x[0] == '\'' else x, params))

            self.insert_record(name, params)  # Insert the record to the table.
            return

        query8 = re.search(self.match_update, query, re.I)

        if query8:  # Is user wanting to update a record?

            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know that no database has been selected.
                return
            name = query8.group(1).strip()  # Get the table name.
            set_identifier = query8.group(2).strip()  # Get the set clause column identifier.
            set_value = query8.group(3).strip().split('\'')[1] if len(
                query8.group(3).strip().split('\'')) > 1 else query8.group(
                3).strip()  # Get the value from the set clause.
            where_statement = re.search(self.match_where, query8.group(4), re.I)
            self.update_record(name, set_identifier, set_value, where_statement)  # Update the record.
            return

        query9 = re.search(self.match_delete, query, re.I)

        if query9:  # Is user wanting to delete a record?
            if not self.selected_database:  # Has the user selected a database?
                print(f'No database has been selected.')  # Let the user know that no database has been selected.
                return

            table_name = query9.group(1).strip()  # Get the table name.
            where_statement = re.search(self.match_where, query9.group(2), re.I)  # Get where statement.

            self.delete_record(table_name, where_statement)  # Delete record.
            return

        print('bad input')  # No matches found if reached here.

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

        os.mkdir(name)  # Create the directory if it doesn't exist.

        print(f'Database {name} created.')

    def create_table(self, name, params):
        # Creates a table by generating a file within the selected database.
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)
        if table_exists:
            print(f'!Failed to create table {name} because it already exists.')
            return

        with open(table_path, 'w') as f:
            header = ''
            for param in params:
                header += f'{param[0].strip()} {param[1].strip()}|'  # Header content
            header = header[:-1]  # Removes trailing a '|'
            f.write(header)  # Writes to file
            print(f'Table {name} created.')

    @staticmethod
    def util_func(param):
        try:  # Try if the parameter is an integer
            return int(param)
        except ValueError:
            try:  # Try if the parameter is a float
                return float(param)
            except ValueError:  # if not an int or float then it has to be string.
                return param.replace('\'', '').replace('"', '')
                # return val.group(1) if val.group(1) else val.group(2)   # Get value except for quotes.

    def insert_record(self, name, values):
        # Inserts a record to a table
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)

        if not table_exists:
            print(f'!Failed to insert values into table because {name} table does not exist.')
            return

        # with open(f'{self.selected_database}/{name}.csv', 'r') as f:
        # header = f.readline()

        # values = list(map(self.util_func, values))  # Apply type coercion

        values = '|'.join(map(str, values))  # join method only works for list with string type

        with open(f'{self.selected_database}/{name}.csv', 'a+') as f:
            if len(f.read().split('\n')) > 1:
                f.write('\n')  # Add new line to prevent appending to the same line
            f.write('\n')
            f.write(values)

        print('1 new record inserted.')

    def update_record(self, name, set_identifier, set_value, where_statement):
        # Updates a record from the given table.
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)
        if not table_exists:
            print(f'!Failed to alter table because it does not exist.')
            return

        # else:
        # with open(f'{name}-locked.txt'):
        # pass

        where_identifier = where_statement.group(1)
        operator = where_statement.group(2)
        where_value = where_statement.group(3)
        print(where_identifier, operator, where_value)
        with open(f'{self.selected_database}/{name}.csv', 'r+') as f:
            file_contents = f.read().rstrip().splitlines()
            header = file_contents[0].split('|')  # Split each item in the line to create the tuple.
            column_set_curser = None  # The column to modify the value.
            column_where_curser = None  # The column for the condition to meet.
            modified_count = 0  # The number of modifications.
            for i, col in enumerate(header):
                ident = re.search(r'^(\w+)', col, re.I)
                if ident and ident.group(1).strip() == where_identifier.strip():  # Is this the column to be modified?
                    column_where_curser = i  # Save the column index.

                if ident and ident.group(1) == set_identifier:  # Is this the column to run the condition?
                    column_set_curser = i  # Save the column index.

            for i, row in enumerate(file_contents):
                columns = row.split('|')
                if self.op[operator](self.util_func(columns[column_where_curser]),
                                     self.util_func(where_value)):  # Run the condition.
                    columns[column_set_curser] = set_value  # Modify the field.
                    file_contents[i] = '|'.join(columns)
                    modified_count += 1

            f.seek(0)
            updated_content = map(lambda el: f'{el}\n', file_contents)
            f.writelines(updated_content)
            f.truncate()
            print(f'{modified_count} record modified.') if modified_count == 1 else print(
                f'{modified_count} records modified.')

    def delete_record(self, name, where_statement):
        # Deletes the record with the supplied name and where statement.
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)
        if where_statement:  # Is the statement included in the query?
            where_identifier = where_statement.group(1)
            operator = where_statement.group(2)
            where_value = where_statement.group(3)
        if not table_exists:
            print(f'!Failed to alter table because it does not exist.')
            return

        with open(f'{self.selected_database}/{name}.csv', 'r+') as f:
            file_contents = f.read().rstrip().splitlines()
            header = file_contents[0].split('|')
            column_curser = None
            if where_statement:  # Delete record according to where statement.
                for i, col in enumerate(header):
                    ident = re.search(r'^(\w+)', col, re.I)
                    if ident and ident.group(1) == where_identifier:
                        column_curser = i
                        break

                if not column_curser:
                    print('Failed to find record')
                    return
                delete_count = 0
                for i, row in enumerate(file_contents):
                    if i == 0:
                        continue
                    columns = row.split('|')
                    if self.op[operator](self.util_func(columns[column_curser]),
                                         self.util_func(where_value.replace('\'', '').replace(';', ''))):
                        file_contents.pop(i)
                        delete_count += 1
            else:  # Delete all records if where statement is not present
                delete_count = len(file_contents[1:])
                file_contents = file_contents[0:1]

            f.seek(0)
            updated_content = map(lambda el: f'{el}\n', file_contents)
            f.writelines(updated_content)
            f.truncate()
            print(f'{delete_count} record deleted.') if delete_count == 1 else print(f'{delete_count} records deleted.')

    def alter_table(self, name, clause_type, payload):
        # Alters the table with the supplied name, clause_type and payload.
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)

        if not table_exists:
            print(f'!Failed to alter table because it does not exist.')
            return

        payload = payload.strip()  # Remove leading and trailing whitespaces.
        payload = ' '.join(payload.split())

        if clause_type == 'add':  # Adds a column to a table.
            with open(f'{self.selected_database}/{name}.csv', 'r+') as f:
                file_contents = f.readlines()
                file_contents[0] += '|' + payload
                body = ''.join(file_contents)
                f.seek(0)
                print(body)
                f.write(body)
                f.truncate()
        elif clause_type == 'modify':
            print('Modify feature not implemented')

        else:
            print('Drop feature not implemented')

    def drop_table(self, name):
        # Drops a table from the given name.
        table_path = f'{self.selected_database}/{name}.csv'
        file_exists = self.does_file_exist(table_path)

        if not file_exists:
            print(f'!Failed to delete {name} because it does not exist.')
            return

        os.remove(table_path)  # Removes the table (file).
        print(f'Table {name} deleted.')

    def drop_database(self, name):
        # file_exists = self.does_file_exist(name + '.sql')
        directory_exists = self.does_directory_exist(name)

        if not directory_exists:
            print(f'!Failed to delete {name} because it does not exist.')
            return

        for f in os.listdir(name):
            os.remove(os.path.join(name, f))

        os.rmdir(name)  # deletes database (directory).

        print(f'Database {name} deleted.')

    @staticmethod
    def selected_columns(rows, indices):
        # Returns the selected columns
        record = ''
        for row in rows:  # Go through each line of the file
            for i, field in enumerate(row):  # Go through each column
                if i in indices:  # Is the column in the selected columns?
                    record += f'{field}|'  # Add to the record
                elif not indices:
                    record += f'{field}|'
            record = f'{record[:-1]}\n'
        return record

    def compute_where(self, where_statement, indices, rows, table):
        # Algorithm to handle where statement.
        record = ''

        if where_statement:
            key = where_statement.group(1)
            operator = where_statement.group(2)
            value = where_statement.group(3).replace(';', '')

            res = [self.op[operator](self.util_func(value), self.util_func(item)) for i, item in
                   enumerate(table[key])]
            new_rows = [row.strip().split('|') for i, row in enumerate(rows[1:]) if res[i]]
            record = self.selected_columns(new_rows, indices)
        else:
            new_rows = [row.strip().split('|') for i, row in enumerate(rows[1:])]
            record = self.selected_columns(new_rows, indices)

        return record

    def query_join(self, names, where_statement, join_type, columns):
        # Queries multiple tables for join operation.
        indices = []
        tables = {}
        for name in names:  # Go through each table
            table_path = f'{self.selected_database}/{name[0]}.csv'
            table_exists = self.does_file_exist(table_path)
            if not table_exists:
                print(f'!Failed to query table {name[0]} because it does not exist.')
                return

            with open(table_path) as tb:
                rows = tb.readlines()
                headers = rows[0].split('|')
                headers = [re.search(r'^(\w+)', col, re.I).group(1) for col in headers]
                table = {key: [val.split('|')[i].strip() for j, val in enumerate(rows[1:])] for i, key in
                         enumerate(headers)}
                indices.append([i for i, v in enumerate(headers) if v in columns])
                tables[name[0]] = table

        t1 = where_statement[0].split('.')
        t2 = where_statement[2].split('.')
        operat = where_statement[1]
        records = ''
        s = set()
        for i, n1 in enumerate(tables[t1[0]][t1[1]]):  # Traverse first table.
            for j, n2 in enumerate(tables[t2[0]][t2[1]]):  # Traverse second table.
                if self.op[operat](self.util_func(n1), self.util_func(n2)):
                    row_n1 = [v[i] for k, v in tables[t1[0]].items()]
                    row_n2 = [v[j] for k, v in tables[t2[0]].items()]
                    records += '|'.join(row_n1) + '|' + '|'.join(row_n2) + '\n'
                    s.add(n1)

            if join_type == 'left outer join' and n1 not in s:  # include left table record if performing left outer join operation.
                row_n1 = [v[i] for k, v in tables[t1[0]].items()]

                records += '|'.join(row_n1) + '\n'

        print(records)

    def query_table(self, name, columns, where_statement):
        # Queries a table from the given name and conditions.
        table_path = f'{self.selected_database}/{name}.csv'
        table_exists = self.does_file_exist(table_path)
        if not table_exists:
            print(f'!Failed to query table {name} because it does not exist.')
            return

        with open(table_path) as tb:
            rows = tb.readlines()
            headers = rows[0].split('|')
            headers = [re.search(r'^(\w+)', col, re.I).group(1) for col in headers]
            table = {key: [val.split('|')[i].strip() for j, val in enumerate(rows[1:])] for i, key in
                     enumerate(headers)}
            indices = [i for i, v in enumerate(headers) if v in columns]
            record = self.compute_where(where_statement, indices, rows, table)
            print(record)

    def select_database(self, name):
        # Selects a database
        database_exists = self.does_directory_exist(name)
        if not database_exists:
            print(f'Failed to select database {name} because it does not exist.')
            return
        self.selected_database = name
        print(f'Using database {name}.')

    def lockable_table(self, table, opt):
        # Locks or removes a lock if opt is 1
        if opt == 1:
            os.remove(f'{table}-locked.txt')
            return
        if self.does_file_exist(f'{table}-locked.txt'):
            self.is_table_locked = (table, True)
            return

        with open(f'{table}-locked.txt', 'w') as fp:
            self.is_table_locked = (table, False)

    def run_query(self, query):
        """Accepts SQL query """
        self.match_query(query)

    def begin_transaction(self):
        """Starts accepting transaction block."""
        sys.stdin.flush() # Clear standard input
        trans_query = []
        for line2 in sys.stdin:
            if bool(re.match(r'\s*commit\s*;?', line2)):
                if self.is_table_locked[1]:
                    print(f'Error: Table {self.is_table_locked[0]} is locked!')
                    return
                if self.selected_database is None:
                    print(f'Error: No database has beenselected!')
                    return

                list(map(self.run_query, trans_query))
                self.lockable_table(self.is_table_locked[0], 1)
                print('Transaction committed.')
                return
            print(re.match(self.match_modification, line2))
            table = re.match(self.match_modification, line2)
            if bool(table):
                print(table.groups())
                table_name = ''.join(filter(lambda x: x is not None, table.groups()))
                self.lockable_table(table_name, 0)
            trans_query.append(line2.rstrip())

    def user_prompt(self):
        # Prompt shown for the user.
        print('--> ', end='')
        query = ''  # User query to store.
        for line in sys.stdin:
            if "--" in line.strip():
                continue
            if ".exit" == line.rstrip().lower():  # Exit program when user inputs ".exit".
                print('All done')
                break
            if bool(re.match(r'\s*begin\s+transaction\s*;?', line)):
                self.begin_transaction()
                continue

            if line.count(";"):  # Does the line contain a semicolon for end of command?
                query += line.rstrip()  # Concatenate to the rest of the command
                self.run_query(query)  # Run the query
                query = ''
            else:  # Otherwise, not end of command yet. Keep accepting user input.
                query += ' ' + line

            print('--> ', end='') if line.count(';') else print('\t',
                                                                end='')  # End of command prints -->, otherwise indents curser.


if __name__ == '__main__':  # Run program automatically if program is called directly
    sql = SQLiter()  # Creates an instance of SQLiter and starts the program
