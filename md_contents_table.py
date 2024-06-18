import os.path
import re

class md_contents_table():

    def __init__(self, file_path, remove_current_table = True):
        """Checks a valid .md file exists in order to create a contents table using create_contents_table().
        Parameters:
        - file_path (str): "path/to/file.md"
        - remove_current_table (bool, optional): Removes previously made content table if it exists."""

        if file_path[-3:] != ".md":
            raise ValueError(f"Please provide a file path ending in '.md', not: {file_path}")
        
        elif not os.path.exists(file_path):
            raise ValueError(f"Please provide the path to an existing .md file, not: {file_path}")

        self.file_path = file_path
        self.remove_current_table = remove_current_table

    def read_file_contents(self):
        with open(self.file_path, "r") as file:
            self.file_contents = file.read()
        with open(self.file_path, "a") as file:
            file.write("hello")
            file.close()

if __name__ == "__main__":
    md_file = md_contents_table("./test.md")
    md_file.create_contents_table()