import sqlite3
import streamlit as st


@st.cache_resource
def _load_connection(connection_path="../Assets/static/database/hunde_database.db"):
    return sqlite3.connect(connection_path, check_same_thread=False)


class DatabaseConnectionProvider:
    def __init__(self):
        self.connection = _load_connection()

    def execute_query(self, query_string):
        try:
            with self.connection:
                return self.connection.execute(query_string).fetchall()
        except sqlite3.Error as error:
            print("Something went wrong with the following query: \n")
            print(query_string)
            print("Stacktrace: \n")
            print(error)
            return -1

