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


def describe_initialisation():
    def test_raises_appropriate_errors():
        # Initialising with a file path that does not end with ".md" raises a ValueError
        with pytest.raises(ValueError):
            mdCT.md_contents_table("./test 1 read file")

        # Initialising with a file that does not exist raises a ValueError
        with pytest.raises(ValueError):
            mdCT.md_contents_table("./hello_world.md")

    def test_parameters():
        # Initialising stores the file path as a class variable
        test_mdCT = mdCT.md_contents_table("./test 1 read file.md")
        assert test_mdCT.file_path == "./test 1 read file.md"

        # Initialising stores an optional bool that removes a previously generated contents table
        test_mdCT = mdCT.md_contents_table("./test 1 read file.md")
        assert test_mdCT.remove_current_table == True

        test_mdCT = mdCT.md_contents_table("./test 1 read file.md", False)
        assert test_mdCT.remove_current_table == False

    def test_memory_reset():
        # Initialising resets all object properties that are not parameters
        test_mdCT = mdCT.md_contents_table("./test 1 read file.md")
        assert test_mdCT._file_contents == None
        assert test_mdCT._headings == None


# Read and store the contents of md file
def describe_read_file_contents():
    def test_input_file_is_read():
        # The contents of a simple file is read and stored
        test_mdCT = mdCT.md_contents_table("./test 1 read file.md")
        test_mdCT.read_file_contents()
        assert test_mdCT._file_contents == "Hello, world!"

    def test_input_file_is_not_mutated():
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
def describe_find_headings():
    def test_able_to_store_headings():
        ## Creates a list for headings
        test_mdCT = mdCT.md_contents_table("./test 2 no headings.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert type(test_mdCT._headings) == list

        ## Stores a list of the headings found
        test_mdCT = mdCT.md_contents_table("./test 2 no headings.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert test_mdCT._headings == []

    def test_finds_one_heading():
        ## Finds 1 top level heading
        test_mdCT = mdCT.md_contents_table("./test 3 1 top level heading.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert test_mdCT._headings == ["# Hello"]

        ## Finds 1 of each level
        test_mdCT = mdCT.md_contents_table("./test 4 1 each level heading.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert test_mdCT._headings == [
            "# Hello",
            "## World",
            "### Three",
            "#### Four",
            "##### Five",
            "###### Six",
        ]

    def test_finds_multiple_top_headings():
        ## Finds multiple top level headings
        test_mdCT = mdCT.md_contents_table("./test 5 multiple top level headings.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert test_mdCT._headings == ["# Hello", "# World", "# How are you?"]

    def test_finds_multiple_each_headings():
        ## Finds multiple of each heading
        test_mdCT = mdCT.md_contents_table(
            "./test 6 multiple of each level headings.md"
        )
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert test_mdCT._headings == [
            "# Hello",
            "## World",
            "### How",
            "#### Are",
            "##### You?",
            "## I'm",
            "###### Good",
            "# Thank",
            "### You",
            "#### For",
            "##### Asking",
        ]

    def test_doesnt_include_any_tags():
        # Doesn't confuse 1 tag
        test_mdCT = mdCT.md_contents_table("./test 7 tag included.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert test_mdCT._headings == ["# Hello"]

        ## Doesn't confuse multiple tags
        test_mdCT = mdCT.md_contents_table("./test 8 complex file.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        assert test_mdCT._headings == [
            "# Hello",
            "## World",
            "### How",
            "#### Are",
            "##### You?",
            "## I'm",
            "###### Good",
            "# Thank",
            "### You",
            "#### For",
            "##### Asking",
        ]


# Format the contents table ready to be written, numbered according to the heading level
# (number of #'s) and in what order they appear
def describe_format_headings():
    def test_able_to_store_formatted_string():
        # Creates a string
        test_mdCT = mdCT.md_contents_table("./test 2 no headings.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        test_mdCT.format_headings()
        actual = test_mdCT._formatted_contents_table
        assert actual == ""

    def test_formats_one_top_level_heading():
        # numbers a top level heading, e.g: 1. <heading>
        test_mdCT = mdCT.md_contents_table("./test 3 1 top level heading.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        test_mdCT.format_headings()
        actual = test_mdCT._formatted_contents_table
        assert actual == "\t1. Hello\n"

    def test_correctly_numbers_each_level():
        # correctly numbers a heading of each level, (e.g 4th level) = 1.1.1.1. <heading>
        test_mdCT = mdCT.md_contents_table("./test 4 1 each level heading.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        test_mdCT.format_headings()
        actual = test_mdCT._formatted_contents_table
        assert (
            actual
            == "\t1. Hello\n\t\t1.1. World\n\t\t\t1.1.1. Three\n\t\t\t\t1.1.1.1. Four\n\t\t\t\t\t1.1.1.1.1. Five\n\t\t\t\t\t\t1.1.1.1.1.1. Six\n"
        )

    def test_correctly_resets_numbering():
        # correctly resets numbering to 1 where a higher level heading interrupts from previous count
        # 1.2 <heading>
        # 2. <heading>
        # 2.1 <heading> <-- the second level heading was previously at "2."
        test_mdCT = mdCT.md_contents_table("./test 9 1 heading reset.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        test_mdCT.format_headings()
        actual = test_mdCT._formatted_contents_table
        assert (
            actual
            == "\t1. Hello\n\t\t1.1. World\n\t\t1.2. How\n\t2. Are\n\t\t2.1. You\n"
        )
    
    def test_correctly_deals_with_a_complex_file():
        test_mdCT = mdCT.md_contents_table("./test 8 complex file.md")
        test_mdCT.read_file_contents()
        test_mdCT.find_headings()
        test_mdCT.format_headings()
        actual = test_mdCT._formatted_contents_table
        assert (
            actual
            == "\t1. Hello\n\t\t1.1. World\n\t\t\t1.1.1. How\n\t\t\t\t1.1.1.1. Are\n\t\t\t\t\t1.1.1.1.1. You?\n\t\t1.2. I'm\n\t\t\t\t\t\t1.2.1.1.1.1. Good\n\t2. Thank\n\t\t\t2.1.1. You\n\t\t\t\t2.1.1.1. For\n\t\t\t\t\t2.1.1.1.1. Asking\n"
        )



# Remove an exisitng contents table if required

# Over-write the contents table then the rest of the file back to the file.
