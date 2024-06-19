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
    mdCT.md_contents_table("./test 1 read file")

  # Initialising with a file that does not exist raises a ValueError
  with pytest.raises(ValueError):
    mdCT.md_contents_table("./hello_world.md")

  # Initialising stores the file path as a class variable
  test_mdCT = mdCT.md_contents_table("./test 1 read file.md")
  assert test_mdCT.file_path == "./test 1 read file.md"

  # Initialising stores an optional bool that removes a previously generated contents table
  test_mdCT = mdCT.md_contents_table("./test 1 read file.md")
  assert test_mdCT.remove_current_table == True

  test_mdCT = mdCT.md_contents_table("./test 1 read file.md", False)
  assert test_mdCT.remove_current_table == False


# Read and store the contents of md file
def test_reading_and_storing_file_contents():
  # The contents of a simple file is read and stored
  test_mdCT = mdCT.md_contents_table("./test 1 read file.md")
  test_mdCT.read_file_contents()
  assert test_mdCT.file_contents == "Hello, world!"

  # The file is not mutated (uses os.path.getmtime <- get time file was last modified)
  input_file_path = "./test 1 read file.md"
  with open(input_file_path, "r") as file:
    before = file.read()
    file.close()

  test_mdCT = mdCT.md_contents_table(input_file_path)
  test_mdCT.read_file_contents()

  with open(input_file_path, "r") as file:
    mutated = file.read()
    file.close()

  assert (before == mutated) == True


# Find and store all the headings from the md file contents
## Numbered according to the number of #



## Finds multiple top level headings
## Finds multiple of each heading

def test_find_and_store_headings():
  ## Stores a list of the headings found
  test_mdCT = mdCT.md_contents_table("./test 2 no headings.md")
  test_mdCT.read_file_contents()
  test_mdCT.find_headings()
  assert test_mdCT.headings == []

  ## Finds 1 top level heading
  test_mdCT = mdCT.md_contents_table("./test 3 1 top level heading.md")
  test_mdCT.read_file_contents()
  test_mdCT.find_headings()
  assert test_mdCT.headings == ["# Hello"]

  ## Finds 1 of each level
  test_mdCT = mdCT.md_contents_table("./test 4 1 each level heading.md")
  test_mdCT.read_file_contents()
  test_mdCT.find_headings()
  assert test_mdCT.headings == ["# Hello"]

# Format the contents table ready to be written

# Remove an exisitng contents table if required

# Over-write the contents table then the rest of the file back to the file.