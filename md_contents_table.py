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
        self.remove_current_table = remove_current_table

    def _read_file_contents(self):
        with open(self.file_path, "r") as file:
            self._file_contents = file.read()

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

    def _format_a_heading(self, hashtags, text, index=1, formatted_heading=""):
        # Recursion base case
        if len(hashtags) == 0:
            self._formatted_contents_table += f"{formatted_heading} {text}\n"
            return

        formatted_heading = f"\t{formatted_heading}{self._levels[index]}."

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
            file.write(f"""<a name="start-of-contents" />
# Contents
{self._formatted_contents_table}<a name=\"end-of-contents\" />

{self._file_contents}""")


# <a name=\"start-of-contents\" />
# <a name=\"end-of-contents\" />
