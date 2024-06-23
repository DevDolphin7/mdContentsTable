""" This module can be used to create a contents table in a markdown (.md) file.

Try calling: md_contents_table.CreateContentsTable("path/to/<file_name>.md")"""

import os.path
import re


class CreateContentsTable:
    """Checks a valid .md file exists in order to create a contents table.
    Parameters:
    - file_path (str): "path/to/file.md"
    - remove_current_table=True (bool, optional): Removes previously made content table if it exists.
    """

    def __init__(self, file_path, remove_current_table=True):
        mdCT = MdContentsTable(file_path)
        mdCT._read_file_contents()
        if remove_current_table:
            mdCT._if_current_table_then_remove()
        mdCT._find_headings()
        mdCT._format_headings()
        mdCT._write_output()


class MdContentsTable:
    """Checks a valid .md file exists in order to create a contents table using create_contents_table().
    Parameters:
    - file_path (str): "path/to/file.md"
    """

    def __init__(self, file_path=""):
        self._file_contents = None
        self._pre_table_file_contents = ""
        self._headings = None
        self._formatted_contents_table = ""
        self._levels = None

        if file_path[-3:] != ".md":
            raise ValueError(
                f"Please provide a file path ending in '.md', not: {file_path}"
            )

        elif not os.path.exists(file_path):
            raise ValueError(
                f"Please provide the path to an existing .md file, not: {file_path}"
            )

        self.file_path = file_path

    def _read_file_contents(self):
        with open(self.file_path, "r") as file:
            self._file_contents = file.read()

    def _if_current_table_then_remove(self):
        current_table_start = re.search(
            '<a name="start-of-contents" />\n', self._file_contents
        )
        if current_table_start != None:
            current_table_end = re.search(
                '<a name="end-of-contents" />\n', self._file_contents
            )
            if current_table_end == None:
                raise ValueError(
                    'The end of content tag <a name="end-of-contents" /> has been removed. Please replace this tag inside the .md file.'
                )

            first_contents_index = current_table_start.span()[0]
            self._pre_table_file_contents = self._file_contents[0:first_contents_index]

            final_contents_index = current_table_end.span()[1] + 1
            self._file_contents = self._file_contents[final_contents_index:]

    def _find_headings(self, contents=None):
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
        self._find_headings(contents=contents)

    def _format_headings(self, headings=None, prior_level=1):
        # Initialise recursion
        if headings == None:
            headings = self._headings
            self._levels = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        # Recursion base case
        if len(headings) == 0:
            return

        heading_hashtags = re.search("^#{1,6} ", headings[0]).group()[:-1]
        heading_text = headings[0][len(heading_hashtags) + 1 :]

        level = len(heading_hashtags)
        if prior_level < level:
            self._reset_levels(prior_level, level)
        self._levels[level] += 1

        self._format_a_heading(heading_hashtags, heading_text)

        # Recursion step - headings[1:]
        self._format_headings(headings=headings[1:], prior_level=level)

    def _format_a_heading(self, hashtags, text, index=0, formatted_heading=""):
        # Recursion base case
        if len(hashtags) == 0:
            self._formatted_contents_table += f"{formatted_heading}{self._levels[index]}. [{text}](#{text.lower()})  \n"[
                1:
            ]
            return

        formatted_heading = f"\t{formatted_heading}"

        # Recursion step
        self._format_a_heading(hashtags[1:], text, index + 1, formatted_heading)

    def _reset_levels(self, prior_level, level):
        # Recursive base case
        if prior_level == level:
            self._levels[level] = 0
            return

        self._levels[prior_level + 1] = 1

        # Recursive step - prior_level + 1
        self._reset_levels(prior_level + 1, level)

    def _write_output(self):
        with open(self.file_path, "w") as file:
            file.write(
                f"""{self._pre_table_file_contents}<a name="start-of-contents" />

# Contents
{self._formatted_contents_table}<a name=\"end-of-contents\" />

{self._file_contents}"""
            )
