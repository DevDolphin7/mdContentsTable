""" Aim: Use TDD in python to develop a class that returns a string of the various headings
numbered as per a contents table for an md file.
For example:
# Hello
Text
## World
Other text
# Heading
## Inner Levels Reset
###### Counts Six Levels

Would re-write the file to appear as follows (including # Contents and the table):
# Contents
 1. Hello
  1.1. World
 2. Heading
   2.1 Inner Levels Reset
      2.1.1.1.1.1 Counts Six Levels

# Hello
Text
~~~original file continues below~~~
"""

import md_contents_table as mdCT
import pytest

def test_initialisation():
  # Initialising with a file path that does not end with ".md" raises a ValueError
  with pytest.raises(ValueError):
    mdCT.md_contents_table("./test one")

  # Initialising with a file that does not exist raises a ValueError
  with pytest.raises(ValueError):
    mdCT.md_contents_table("./hello_world.md")

  # Initialising stores the file path as a class variable
  test_mdCT = mdCT.md_contents_table("./test one.md")
  assert test_mdCT.file_path == "./test one.md"

  # Initialising stores an optional bool that removes a previously generated contents table
  test_mdCT = mdCT.md_contents_table("./test one.md")
  assert test_mdCT.remove_current_table == True

  test_mdCT = mdCT.md_contents_table("./test one.md", False)
  assert test_mdCT.remove_current_table == False


# Read and store the contents of md file
def test_reading_and_storing_file_contents():
  # The contents of the file provided is read and stored
  test_mdCT = mdCT.md_contents_table("./test one.md")
  assert test_mdCT.file_contents == "Hello, world!"


# Find and store all the headings from the md file contents
## Numbered according to the number of #

# Format the contents table ready to be written

# Remove an exisitng contents table if required

# Over-write the contents table then the rest of the file back to the file.