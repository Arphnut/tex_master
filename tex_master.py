#!/usr/bin/python3
"""
Author: Etienne

Name:
-----
tex_master.py

Description:
------------
A script to add or remove a tex master from all .tex files in a folder (using AUCTeX format)
"""

import os
import argparse


def totex(filename):
    """
    If the name of the file provided does not contain the .tex format at the end, add it.
    """
    try:
        if filename[-4:] != ".tex":
            return filename + ".tex"
        else:
            return filename
    except IndexError:
        return filename


parser = argparse.ArgumentParser(
    description=
    """Add a comment in all tex files to give a new master for the compilation.
    Used for Emacs with AUCTeX""")
parser.add_argument('mainfile', type=str, help='The name of the main file.')
parser.add_argument(
    '-n',
    '--nomaster',
    nargs='+',
    type=str,
    help="Do not add the new master comment to files listed after --nomaster.")
parser.add_argument(
    '-r',
    '--remove',
    action="store_true",
    help="Remove the comment on master file instead of adding it.")
parser.add_argument('-v', '--verbose', action="store_true")
args = parser.parse_args()

# Add the main file to nomaster, and preprocess all the files.
if args.nomaster is None:
    args.nomaster = []
args.nomaster.append(args.mainfile)
for ind in range(len(args.nomaster)):
    args.nomaster[ind] = totex(args.nomaster[ind])

text_newmaster = """\n%%% Local Variables:
%%% mode: latex
%%% TeX-master: "{}"
%%% End:""".format(args.mainfile)

if args.remove:
    if args.verbose:
        print("File to which the master was removed:")
    for filename in os.listdir():
        if filename[-4:] == ".tex" and filename not in args.nomaster:
            if args.verbose:
                print(filename)
            with open(filename, 'r') as filer:
                content = filer.readlines()
            contenttext = "".join(content)
            contenttext = contenttext.replace(
                text_newmaster, '')  # Remove text_newmaster from contenttext
            with open(filename, 'w') as filew:
                filew.write(contenttext)
else:
    if args.verbose:
        print("File to which the master was added:")
    for filename in os.listdir():
        if filename[-4:] == ".tex" and filename not in args.nomaster:
            if args.verbose:
                print(filename)
            with open(filename, 'r') as filer:
                content = filer.readlines()
            contenttext = "".join(content)
            if "%%% Local Variables:" not in contenttext:
                contenttext += text_newmaster
            with open(filename, 'w') as filew:
                filew.write(contenttext)
