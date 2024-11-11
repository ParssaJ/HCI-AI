import os
import sqlite3
from eralchemy import render_er
from tqdm import tqdm
import shutil

"""
This Script is intended for one-time use only and was 
used to generate the corresponding db.file for each 
schema found in the spiders dataset. After the generation of said 
db.file, eralchemy tries to render a corresponding image of the schema,
which we will display in the frontend.
If no schema exists or if the schema is faulty, we discard said 
dataset.
"""
if __name__ == '__main__':
    starting_directory = "../../Assets/datasets/spider_data/database/"
    subdirectories = os.listdir(starting_directory)
    subdirectories.remove(".DS_Store") # For some reason this directory pops up...
    for subdirectory in tqdm(subdirectories):
        print(f"Currently at directoy: {subdirectory}")

        schema_path_of_subdirectory = starting_directory + subdirectory + "/schema.sql"

        if not os.path.exists(schema_path_of_subdirectory):
            print(f"No schema-file found in directory: {subdirectory}, deleting and skipping...")
            shutil.rmtree(starting_directory + subdirectory)
            continue

        with open(schema_path_of_subdirectory, "r") as f:
            schema_file_content = f.read()

        db_path = starting_directory + subdirectory + f"/{subdirectory}.db"

        connection = sqlite3.connect(db_path)
        connection.executescript(schema_file_content)

        try:
            render_er("sqlite:///" + db_path, starting_directory + subdirectory + f"/{subdirectory}.png")
        except Exception as e:
            print(f"Something went wrong when rendering the schema-file of directory {subdirectory}")
            shutil.rmtree(starting_directory + subdirectory)
            continue  # Probably something wrong in the schema file

        connection.close()
