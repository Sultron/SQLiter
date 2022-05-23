# SQLiter

## Lighter than SQLite!

In this version SQliter can now perform transactions.


### How SQLiter handles transactions?
When a transaction is started, tables are locked if they are not already and if they are locked and a commit 
is performed, the transction will abort. Follows the "all-or-nothing" property. SQLiter tracks and mantains locks through the use of files.



## Requirements

Python version >= 3.10

## How to use

Run SQLiter using standard input.

```sh
python main.py < PA4_test.sql
```

Run SQLiter using editor.

```sh
python main.py
```
