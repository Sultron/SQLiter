# SQLiter

## Lighter than SQLite!

In this version SQliter can perform aggregate queries. Specifically, COUNT, AVG, and MAX.

### How SQLiter performs COUNT?.

COUNT is performed by suming the number of rows in a table excluding the header.

### How SQLiter performs AVG?

AVG is performed by summing the values of a column and dividing the total number of rows excluding the header.

### How SQLiter performs MAX

MAX is performed by traversing the specified column and returns the largest value in that column.

## Requirements

Python version >= 3.10

## How to use

Run SQLiter using standard input.

```sh
python main.py < PA5_test.sql
```

Run SQLiter using editor.

```sh
python main.py
```
