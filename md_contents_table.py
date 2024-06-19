import os.path

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


    def find_headings(self, headings=[], contents=None):
        self.headings = headings
        print(self.headings, "<--- headings")

        # Initialise recursion
        if contents == None: contents = self.file_contents.split("\n")

        print(contents, "<--- contents")
        # Recursive base case
        if len(contents) == 0: return

        if len(contents[0]) != 0:
            if contents[0][0] == "#": self.headings.append(contents[0])
        

        # Recursive step
        contents.pop(0)
        self.find_headings(headings=self.headings, contents=contents)

