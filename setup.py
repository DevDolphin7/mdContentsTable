from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='md_contents_table',
    version='1.0.0',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
