import os.path, re


class md_contents_table:

    def __init__(self, file_path, remove_current_table=True):
        """Checks a valid .md file exists in order to create a contents table using create_contents_table().
        Parameters:
        - file_path (str): "path/to/file.md"
        - remove_current_table (bool, optional): Removes previously made content table if it exists.
        """

        self._file_contents = None
        self._headings = None
        self._formatted_contents_table = ""

        if file_path[-3:] != ".md":
            raise ValueError(
                f"Please provide a file path ending in '.md', not: {file_path}"
            )

        elif not os.path.exists(file_path):
            raise ValueError(
                f"Please provide the path to an existing .md file, not: {file_path}"
            )

        self.file_path = file_path
        self.remove_current_table = remove_current_table

    def read_file_contents(self):
        with open(self.file_path, "r") as file:
            self._file_contents = file.read()

    def find_headings(self, contents=None):
        # Initialise recursion
        if self._headings == None:
            self._headings = []
        if contents == None:
            contents = self._file_contents.split("\n")

        # Recursive base case
        if len(contents) == 0:
            return

        if re.search("^#{1,6} ", contents[0]) != None:
            self._headings.append(contents[0])

        # Recursive step
        contents.pop(0)
        self.find_headings(contents=contents)

    def format_headings(self, headings=None, previous_level=0):
        # Initialise recursion
        if headings == None:
            headings = self._headings

        # Recursion base case
        if len(headings) == 0:
            return

        # .search returns an object, .group returns the match
        heading_level = re.search("^#{1,6} ", headings[0]).group()
        # [:-1] removes the ending whitespace, len() converts # to number (heading level)
        heading_level = len(heading_level[:-1])

        if heading_level > previous_level:
            heading_text = headings[0][heading_level + 1 :]
            self._formatted_contents_table += f"\t{heading_level}. {heading_text}\n"

        # Recursion step
        headings.pop(0)
        self.format_headings(headings=headings, previous_level=heading_level)
