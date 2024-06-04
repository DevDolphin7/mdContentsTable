import os.path
import re

class md_contents_table():

    def __init__(self, file_path, remove_current_table=True):
        """Checks a valid .md file exists in order to create a contents table using create_contents_table().
        Parameters:
        - file_path (str): "path/to/file.md"
        - remove_current_table (bool, optional): Removes previously made content table if it exists."""

        if file_path[-3:] != ".md":
            raise ValueError(f"Please provide a file name ending with \".md\", not: \"{file_path}\"")
        if not os.path.isfile(file_path):
            raise ValueError(f"os.path cannot find file provided: \"{file_path}\"")
        self.file_path = file_path
        self.remove_current_table = remove_current_table


    def create_contents_table(self):
        """Creates a contents table from headings in an md file.
        Commits full file contents to memory - not recommended for large files."""

        # Open the file and read the contents
        with open(self.file_path, "r") as file:
            self.lines = file.readlines()
            file.close()

        # Look for headings in the .md file
        if not self.find_md_headings():
            raise ValueError("No headings found in md file.")
        
        # Remove the contents table if required and it exists
        if self.remove_current_table:
            self.remove_contents_table()

        # Set up variables to number the contents table
        current_heading_level = 0
        heading_list_number = {num: 0 for num in range(1,7)}
        
        # Write the contents table        
        with open(self.file_path, "w") as file:
            file.write("<a name=\"start-of-contents\" />\n# Contents\n\n")

            # Loop through all the headings
            for index, level in enumerate(self.heading_level):
                # Check if heading level has changed
                if current_heading_level != level:
                    # Check if new level is a lower number (resets the count of higher level headings)
                    if current_heading_level > level:
                        heading_list_number[current_heading_level] = 0
                    current_heading_level = level
                heading_list_number[current_heading_level] += 1

                # Add additional whitespace for every level of heading
                tabs = "".join(" " for x in range(0, current_heading_level))

                # Write the heading into the .md
                file.write(tabs + str(heading_list_number[current_heading_level]) +
                           f". {self.heading_text[index][current_heading_level + 1:]}\n")
                
            file.write("<a name=\"end-of-contents\" />\n")

            # Write the rest of the content that was origianlly in the file
            for line in self.lines:
                file.write(line)
            file.close()

        
    def find_md_headings(self):
        self.heading_text = []
        self.heading_level = []

        for line in self.lines:
            regex = re.search("^#{1,6} ", line)
            if regex: # true if regex found matches
                if not re.search("^# Contents", line):
                    self.heading_text.append(line[:-1])
                    self.heading_level.append(regex.span()[1] - 1) # -1 as regex search includes 1 whitespace
        
        if len(self.heading_text) > 0:
            return True
        return False


    def remove_contents_table(self):
        start_index, end_index = None, None

        for ref, line in enumerate(self.lines, start=1):
            if re.search("<a name=\"start-of-contents\" />", line):
                start_index = ref
            elif re.search("<a name=\"end-of-contents\" />", line):
                end_index = ref
                break
        
        new_lines = []
        if start_index != None and end_index != None:
            with open(self.file_path, "w") as file:
                for ref, line in enumerate(self.lines, start=1):
                    if ref < start_index or ref > end_index:
                        file.write(line)
                        new_lines.append(line)
                file.close()
            self.lines = new_lines


if __name__ == "__main__":
    import sys
    try:
        md_file = md_contents_table(sys.argv[1])
    except IndexError:
        raise IndexError("No file was provided. Please provide a file ending \".md\" when calling the script.")
    md_file.create_contents_table()