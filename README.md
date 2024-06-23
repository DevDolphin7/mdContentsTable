# md_contents_table
This module can be used to create a contents table in a markdown (.md) file.

Try:
```python
import md_contents_table as mdCT

mdCT.CreateContentsTable("path/to/<file_name>.md")
```
If a contents table was previouly generated, it updates it. Text above the contents table is unaffected by updating, but also not included in the update.

---

# Aim
Use TDD in python to develop a class that returns a string of the various headings numbered as per a contents table for an md file.
For example:

```markdown
# Hello
Text
## World
Other text
# Heading
## Inner Levels Reset
###### Counts Six Levels
```

Would re-write the file to appear as below, including # Contents and the contents table.
The headings link to the relevant sections.

```
# Contents
1. [Hello](#hello)  
    1. [World](#world)  
2. [Heading](#heading)  
    1. [Inner Levels Reset](#inner-levels-reset)  
                        1. [Counts Six Levels](#counts-six-levels)  

# Hello
Text
~~~original file continues below~~~
```

---

# Testing
Tests are run through pytest, and utilise the describe-style plugin for pytest.

`pip install pytest-describe`

# Contact
If you have any feedback or ideas for improvement, please get in touch!  
Github: https://github.com/DevDolphin7/mdContentsTable  
PyPI: https://pypi.org/project/md_contents_table/  
Email: DevDolphin7@outlook.com  
