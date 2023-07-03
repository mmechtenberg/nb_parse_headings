#!python3
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


import json
import re
from typing import List
from typing import Tuple

import sys
import os
import errno

import tqdm

import argparse


def extract_headings(strMdSource : List[str]) -> List[Tuple[str, int, str]]:
    listOfHeadings = []
    for line in strMdSource:
        if mo := re.match(pattern=r" *#+", string=line ):
            n_level = mo.group().count(r"#")
            heading = line[mo.end():]
            listOfHeadings.append((line[0:mo.end()], n_level, heading))

    return listOfHeadings

class nb_SectionTree():
    def __init__(self, strFile) -> None:
        self.strFile = strFile
        self.read_dom()
        self.read_headings()

    def read_dom(self)->None:
        with open(self.strFile, "r") as f:
            self.nb_dom = json.load(f)

    def read_headings(self)->None:
        cells = self.nb_dom["cells"]

        self.listOfHeadings = []
        for cell in cells:
            if str(cell["cell_type"]) == "markdown":
                self.listOfHeadings += extract_headings(cell["source"])

    def raise_section_level(self) -> None:
        for idx in range(0, len(self.listOfHeadings)):
            tup = self.listOfHeadings[idx]

            str_level :str = "#" + tup[0].replace(" ", "")
            n_level   :int = tup[1]+1
            str_title :str = tup[2]

            self.listOfHeadings[idx] = (str_level, n_level, str_title) 


class genJPnotebook():

    def __init__(self, sts : List['nb_SectionTree'], outputFile :str):
        self.nb_dict = {
            "cells" : []
            ,"nbformat": 4
            ,"nbformat_minor": 0
            , "metadata": {
              "kernelspec": {
               "display_name": "",
               "name": ""
              },
              "language_info": {
               "name": ""
              }
            },
        }

        self.outputFile = outputFile

        self.sts = sts

        self.add_titles()

        self.export()

    def add_titles(self):
        for st in self.sts:
            st.raise_section_level()
            self.add_cell("# {} [goto]({})".format(st.strFile, st.strFile))
            for h in st.listOfHeadings:
                self.add_cell(h[0] + " " + h[2])

    def export(self):
        with open(self.outputFile, "w") as f:
            json.dump(self.nb_dict, f)

    def add_cell(self, listStrCode):
        self.nb_dict['cells'].append(
            {  "cell_type": "markdown",
               "metadata": {
                "jp-MarkdownHeadingCollapsed": True,
               },
               "source": listStrCode
            }
        )

def getArgParse() :
    parser = argparse.ArgumentParser(
        prog = 'Jupyter Notebook parse headings v0.1.0'
    )

    parser.add_argument(
        'in files'
        , nargs = '*'
        , help = """A list of notebooks to scan.\n
        if this list is empty the sdtin is read and interpreted
        as \\n seperated list of files.
        """
    )
    parser.add_argument('-o', '--output', nargs = 1)

    return parser

def removeOutFileFromInList(outfile:str, inList:List[str]) -> List[str]:
    return [ file for file in inList if (not os.path.samefile(outfile, file)) ]

def readFilesFromStdin():
    fileList = sys.stdin.read().splitlines()

    for file in fileList:
        if not os.access(file, os.F_OK):
            raise FileNotFoundError(
                errno.ENOENT
                , os.strerror(errno.ENOENT)
                , file)

    return fileList




if __name__ == "__main__":
    args = getArgParse().parse_args()
    arg_dict = args.__dict__

    if len(arg_dict['in files']) == 0:
        arg_dict['in files'] = readFilesFromStdin()

    InFiles = removeOutFileFromInList(
        arg_dict['output'][0], arg_dict['in files'])

    if len(InFiles) < len(arg_dict['in files']):
        print("Warning: Output file was removed from input file list.")

    nbts = []
    for file_l in tqdm.tqdm(InFiles):
        nbts.append(nb_SectionTree(file_l))

    genJPnotebook(nbts, outputFile = arg_dict['output'][0])
