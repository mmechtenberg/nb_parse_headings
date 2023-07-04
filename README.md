[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
# nb-parse-headings
This tool generates a jupyter notebook which lists the headings and their structure
based on a list of jupyter notebook file paths.
These generated heading list contains links to the respective notebooks.
You can also use the generated heading notebook to navigate to the respective 
sections within the target notebook.

# Install

install via pulling and executing
```bash
pip install .
```
in the repository root.
Or via the pip install using the git repo as package source.

```bash
pip install git+https://github.com/mmechtenberg/nb_parse_headings.git
```

# Use

After installation, the provided script ```nb-parse-headings``` should 
be within your ```PATH```.
By default, the script waits for a new line separated file list on stdin.
This way, you can use this script by piping a file list to the script's stdin.
For example:

```bash
find ./ -name "*.ipynb" | nb-parse-headings -o headings.ipynb
```
The output file provided by ```-o``` is always ignored.

You can also provide the file list as command line argument.
For example:

```bash
nb-parse-headings -o headings.ipynb "./*.ipynb"
```

