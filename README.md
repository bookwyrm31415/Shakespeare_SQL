# Shakespeare_SQL
A little Flask app to play around with SQLite FTS

The shakespeare.db is created by running the init_db.py file, where I put everything into a table (with some cleaning) and a virtual table for the full text search.
The rest is a simple django app to fetch lines that match an input and display them.
