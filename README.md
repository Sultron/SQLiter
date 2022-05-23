# SQLiter

## Lighter than SQLite!

In this version SQliter can now store, delete, insert, and query tuples.


### How SQLiter performs different joins.
A double nested for loop is need for each of the join operation. For outer left join, an addtional operation is performed to include the rest of the unmatched left table records.

### How SQLiter organizes multiple databases?

Each database has its own dedicated directory.

### How SQLiter manages multiple tables?

Each table is stored in it's own dedicated file.

### How SQLiter store tuples in the table?
Each item in a tuple is sepreated by a '|' when stored to a table.

### How SQLiter do tuple insertion?
A tuple is appended at the end of the table for insertions. 

### How SQLiter do tuple deletion?
SQLiter reads the table into memory and if a condtion is met, removes that row from the table and overwrites the file.

### How SQLiter do tuple modification?
SQLiter reads the table into memory and if a condtion is met, modifies that column from the table to the new value and overwrites the file.

### How SQLiter do tuple modification?
SQLiter reads the table into memory and if a condtion is met, modifies that column from the table to the new value and overwrites the file.

### How SQLiter do tuple query?
SQLiter reads the table into memory and prints the selected columns if a condtion is met.




## Implementation

SQliter is implemented in Python to handle major database operations such as creating databases or tables and querying tables.

## Requirements

Python version >= 3.10

## How to use

Run SQLiter using standard input.

```sh
python main.py < PA2_test.sql
```

Run SQLiter using editor.

```sh
python main.py
```
