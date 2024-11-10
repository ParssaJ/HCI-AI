from eralchemy import render_er
import sqlite3

if __name__ == '__main__':
    connection = sqlite3.connect("meine_erste_datenbank.db")

    with open("../../Assets/datasets/spider_data/database/academic/schema.sql") as f:
        schema_input = f.read()

    connection.executescript(schema_input)
    render_er("sqlite:///./meine_erste_datenbank.db", 'erd_from_sqlite.png')