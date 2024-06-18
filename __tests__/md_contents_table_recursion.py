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

# Initialise a class
## Raise error if file path ends with .md
## Raise error if the file does not exist
## Store the file path
## Optionally store a bool to remove an existing contents table

def test_initialisation():
  # Initialising with a file path that does not end with ".md" raises a ValueError
  with pytest.raises(ValueError):
    mdCT.md_contents_table("./test")

  # Initialising with a file that does not exist raises a ValueError
  with pytest.raises(ValueError):
    mdCT.md_contents_table("./hello_world.md")

  # Initialising stores the file path as a class variable
  test_mdCT = mdCT.md_contents_table("./test.md")
  assert test_mdCT.file_path == "./test.md"