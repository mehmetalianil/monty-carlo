from setuptools import setup, find_packages

setup(
    name = "Monty Carlo",
    version = "0.1.0 dev",
    packages = find_packages(),
    # scripts = ['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Mehmet Ali Anil",
    author_email = "mehmet.ali.anil@ieee.org",
    description = "Monty Carlo is a modular Monte Carlo engine, suitable for statistical systems.",
    license = "LICENSE.txt",
    keywords = "monte carlo simulation statistical physics",
    url = "http://github.com/monty-carlo/monty-carlo/",    
    # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)