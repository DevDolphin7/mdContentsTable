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


Would re-write the file to appear as below, including # Contents and the table.
The headings should link to the relevant sections.

# Contents
1. Hello
    1. World
2. Heading
    1. Inner Levels Reset
                        1. Counts Six Levels

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
            mdCT.MdContentsTable("./test_files/test 1 read file")

        # Initialising with a file that does not exist raises a ValueError
        with pytest.raises(ValueError):
            mdCT.MdContentsTable("./test_files/hello_world.md")

    def test_parameters():
        # Initialising stores the file path as a class variable
        test_mdCT = mdCT.MdContentsTable("./test_files/test 1 read file.md")
        assert test_mdCT.file_path == "./test_files/test 1 read file.md"

    def test_memory_reset():
        # Initialising resets all object properties that are not parameters
        test_mdCT = mdCT.MdContentsTable("./test_files/test 1 read file.md")
        assert test_mdCT._file_contents == None
        assert test_mdCT._pre_table_file_contents == ""
        assert test_mdCT._headings == None
        assert test_mdCT._formatted_contents_table == ""
        assert test_mdCT._levels == None


# Read and store the contents of md file
def describe__read_file_contents():
    def test_input_file_is_read():
        # The contents of a simple file is read and stored
        test_mdCT = mdCT.MdContentsTable("./test_files/test 1 read file.md")
        test_mdCT._read_file_contents()
        assert test_mdCT._file_contents == "Hello, world!"

    def test_input_file_is_not_mutated():
        # The file is not mutated (uses os.path.getmtime <- get time file was last modified)
        input_file_path = "./test_files/test 1 read file.md"
        with open(input_file_path, "r") as file:
            before = file.read()
            file.close()

        test_mdCT = mdCT.MdContentsTable(input_file_path)
        test_mdCT._read_file_contents()

        with open(input_file_path, "r") as file:
            mutated = file.read()
            file.close()

        assert (before == mutated) == True


def describe__if_current_table_then_remove():
    def test_removes_existing_contents_table_from_file_contents():
        test_mdCT = mdCT.MdContentsTable("./test_files/test 10 simple output.md")
        test_mdCT._read_file_contents()
        test_mdCT._if_current_table_then_remove()
        actual = test_mdCT._file_contents
        assert actual == "# Hello\n\nWorld!"

    def test_does_not_remove_content_above_current_table():
        input_file_path = "./test_files/test 13 contents above content table.md"

        mdCT.CreateContentsTable(input_file_path)

        with open(input_file_path, "r") as file:
            actual = file.read()
            file.close()

        assert (
            actual
            == '# Title \n\nContent above the contents table, not included in the contents table\n<a name="start-of-contents" />\n\n# Contents\n1. [Hello](#hello)  \n<a name="end-of-contents" />\n\n# Hello\n\nWorld!'
        )


# Find and store all the headings from the md file contents
def describe__find_headings():
    def test_able_to_store_headings():
        ## Creates a list for headings
        test_mdCT = mdCT.MdContentsTable("./test_files/test 2 no headings.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        assert type(test_mdCT._headings) == list

        ## Stores a list of the headings found
        test_mdCT = mdCT.MdContentsTable("./test_files/test 2 no headings.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        assert test_mdCT._headings == []

    def test_finds_one_heading():
        ## Finds 1 top level heading
        test_mdCT = mdCT.MdContentsTable("./test_files/test 3 1 top level heading.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        assert test_mdCT._headings == ["# Hello"]

        ## Finds 1 of each level
        test_mdCT = mdCT.MdContentsTable("./test_files/test 4 1 each level heading.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
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
        test_mdCT = mdCT.MdContentsTable(
            "./test_files/test 5 multiple top level headings.md"
        )
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        assert test_mdCT._headings == ["# Hello", "# World", "# How are you?"]

    def test_finds_multiple_each_headings():
        ## Finds multiple of each heading
        test_mdCT = mdCT.MdContentsTable(
            "./test_files/test 6 multiple of each level headings.md"
        )
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
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
        test_mdCT = mdCT.MdContentsTable("./test_files/test 7 tag included.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        assert test_mdCT._headings == ["# Hello"]

        ## Doesn't confuse multiple tags
        test_mdCT = mdCT.MdContentsTable("./test_files/test 8 complex file.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
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
def describe__format_headings():
    def test_able_to_store_formatted_string():
        # Creates a string
        test_mdCT = mdCT.MdContentsTable("./test_files/test 2 no headings.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        test_mdCT._format_headings()
        actual = test_mdCT._formatted_contents_table
        assert actual == ""

    def test_formats_one_top_level_heading():
        # numbers a top level heading, e.g: 1. <heading>
        test_mdCT = mdCT.MdContentsTable("./test_files/test 3 1 top level heading.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        test_mdCT._format_headings()
        actual = test_mdCT._formatted_contents_table
        assert actual == "1. [Hello](#hello)  \n"

    def test_correctly_numbers_each_level():
        # correctly numbers a heading of each level, (e.g 4th level) = 1.1.1.1. <heading>
        test_mdCT = mdCT.MdContentsTable("./test_files/test 4 1 each level heading.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        test_mdCT._format_headings()
        actual = test_mdCT._formatted_contents_table
        assert (
            actual
            == "1. [Hello](#hello)  \n\t1. [World](#world)  \n\t\t1. [Three](#three)  \n\t\t\t1. [Four](#four)  \n\t\t\t\t1. [Five](#five)  \n\t\t\t\t\t1. [Six](#six)  \n"
        )

    def test_correctly_resets_numbering():
        # correctly resets numbering to 1 where a higher level heading interrupts from previous count
        # 1.2 <heading>
        # 2. <heading>
        # 2.1 <heading> <-- the second level heading was previously at "2."
        test_mdCT = mdCT.MdContentsTable("./test_files/test 9 1 heading reset.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        test_mdCT._format_headings()
        actual = test_mdCT._formatted_contents_table
        assert (
            actual
            == "1. [Hello](#hello)  \n\t1. [World](#world)  \n\t2. [How](#how)  \n2. [Are](#are)  \n\t1. [You](#you)  \n"
        )

    def test_correctly_deals_with_a_complex_file():
        test_mdCT = mdCT.MdContentsTable("./test_files/test 8 complex file.md")
        test_mdCT._read_file_contents()
        test_mdCT._find_headings()
        test_mdCT._format_headings()
        actual = test_mdCT._formatted_contents_table
        assert (
            actual
            == "1. [Hello](#hello)  \n\t1. [World](#world)  \n\t\t1. [How](#how)  \n\t\t\t1. [Are](#are)  \n\t\t\t\t1. [You?](#you?)  \n\t2. [I'm](#i'm)  \n\t\t\t\t\t1. [Good](#good)  \n2. [Thank](#thank)  \n\t\t1. [You](#you)  \n\t\t\t1. [For](#for)  \n\t\t\t\t1. [Asking](#asking)  \n"
        )


# Write the contents table then the rest of the file back to the file.
def describe__write_output():
    def test_adds_a_content_table_to_a_simple_file():
        input_file_path = "./test_files/test 10 simple output.md"

        test_mdCT = mdCT.MdContentsTable(input_file_path)
        test_mdCT._read_file_contents()
        test_mdCT._if_current_table_then_remove()
        test_mdCT._find_headings()
        test_mdCT._format_headings()
        test_mdCT._write_output()

        with open(input_file_path, "r") as file:
            actual = file.read()
            file.close()

        assert (
            actual
            == '<a name="start-of-contents" />\n\n# Contents\n1. [Hello](#hello)  \n<a name="end-of-contents" />\n\n# Hello\n\nWorld!'
        )

    def test_adds_a_content_table_to_a_complex_file():
        input_file_path = "./test_files/test 11 complex file output.md"

        test_mdCT = mdCT.MdContentsTable(input_file_path)
        test_mdCT._read_file_contents()
        test_mdCT._if_current_table_then_remove()
        test_mdCT._find_headings()
        test_mdCT._format_headings()
        test_mdCT._write_output()

        with open(input_file_path, "r") as file:
            actual = file.read()
            file.close()

        assert (
            actual
            == '<a name="start-of-contents" />\n\n# Contents\n1. [Hello](#hello)  \n\t1. [World](#world)  \n\t\t1. [How](#how)  \n\t\t\t1. [Are](#are)  \n\t\t\t\t1. [You?](#you?)  \n\t2. [I\'m](#i\'m)  \n\t\t\t\t\t1. [Good](#good)  \n2. [Thank](#thank)  \n\t\t1. [You](#you)  \n\t\t\t1. [For](#for)  \n\t\t\t\t1. [Asking](#asking)  \n<a name="end-of-contents" />\n\n# Hello\n**Hello text!**\n\n## World\nText with a paragraph\n\nAnother paragraph\n\n### How\n```js\nfunction thisIsHow() {\n    console.log("we do it")\n}\n```\n\n#### Are\n> Othr forms of text formatting are available\n##### You?\n\n## I\'m\n#trees\n###### Good\n#seas\n# Thank\nText and then a #tag, why not?\n### You\n`random code snippets` that aren\'t long enough for a big box\n#### For\n##### Asking\n'
        )


# Make it convenient for user to interact with
def describe_CreateContentsTable():
    def test_user_convinient_way_functions_correctly():
        input_file_path = "./test_files/test 12 convenient user interface.md"

        mdCT.CreateContentsTable(input_file_path)

        with open(input_file_path, "r") as file:
            actual = file.read()
            file.close()

        assert (
            actual
            == '<a name="start-of-contents" />\n\n# Contents\n1. [Hello](#hello)  \n\t1. [World](#world)  \n\t\t1. [How](#how)  \n\t\t\t1. [Are](#are)  \n\t\t\t\t1. [You?](#you?)  \n\t2. [I\'m](#i\'m)  \n\t\t\t\t\t1. [Good](#good)  \n2. [Thank](#thank)  \n\t\t1. [You](#you)  \n\t\t\t1. [For](#for)  \n\t\t\t\t1. [Asking](#asking)  \n<a name="end-of-contents" />\n\n# Hello\n**Hello text!**\n\n## World\nText with a paragraph\n\nAnother paragraph\n\n### How\n```js\nfunction thisIsHow() {\n    console.log("we do it")\n}\n```\n\n#### Are\n> Othr forms of text formatting are available\n##### You?\n\n## I\'m\n#trees\n###### Good\n#seas\n# Thank\nText and then a #tag, why not?\n### You\n`random code snippets` that aren\'t long enough for a big box\n#### For\n##### Asking\n'
        )

    def test_links_to_headings():
        input_file_path = "./test_files/test 12 convenient user interface.md"

        mdCT.CreateContentsTable(input_file_path)

        with open(input_file_path, "r") as file:
            actual = file.read()
            file.close()

        assert (
            actual
            == '<a name="start-of-contents" />\n\n# Contents\n1. [Hello](#hello)  \n\t1. [World](#world)  \n\t\t1. [How](#how)  \n\t\t\t1. [Are](#are)  \n\t\t\t\t1. [You?](#you?)  \n\t2. [I\'m](#i\'m)  \n\t\t\t\t\t1. [Good](#good)  \n2. [Thank](#thank)  \n\t\t1. [You](#you)  \n\t\t\t1. [For](#for)  \n\t\t\t\t1. [Asking](#asking)  \n<a name="end-of-contents" />\n\n# Hello\n**Hello text!**\n\n## World\nText with a paragraph\n\nAnother paragraph\n\n### How\n```js\nfunction thisIsHow() {\n    console.log("we do it")\n}\n```\n\n#### Are\n> Othr forms of text formatting are available\n##### You?\n\n## I\'m\n#trees\n###### Good\n#seas\n# Thank\nText and then a #tag, why not?\n### You\n`random code snippets` that aren\'t long enough for a big box\n#### For\n##### Asking\n'
        )
