"""
Copyright 2023 Malte Mechtenberg

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup

setup(name="nb_parse_headings",
      version='0.1.1',
      description="This is a module which can be used to generate a jupyter notebook"
                  "listing all headings of user selected jupyter notebooks."
                  "The heading listing will contain links to the respective notebooks",
      author="Malte Mechtenberg",
      license="Apache-2.0",
      packages=["nb_parse_headings"],
      scripts=["./nb_parse_headings/nb_parse_headings.py"],
      python_requires=">=3.0",
      install_requires=[
        "tqdm",
        "argparse"
      ])
