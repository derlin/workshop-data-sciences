#!/bin/env python3

# -*- coding: utf-8 -*-

# This little command line script transforms the BBC dataset
# available at http://mlg.ucd.ie/datasets/bbc.html 
# into single CSV or JSON files. Duplicates are removed.
#
# For each article, the following informations are exported:
# 
# * filename: the relative file to the original file, for example 
#     /business/001.txt
# * category: the article category, for example business
# * title: the title of the article (first line of an article file)
# * content: the content of the article (all except the first line of an article file)

import sys, os, glob
import os.path as path
import csv, json
import argparse

encoding = "latin1"


def write_csv(entries, output_file, encoding="utf8"):
    """ write the entries into a CSV file (with headers)

    :param entries: the dictionary of entries 
    :param output_file: path of the output file 
    :param encoding: the encoding to use, default to utf8
    """ 
    with open(output_file, 'w', encoding=encoding) as f:
        dict_writer = csv.DictWriter(f, entries[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(entries)

def write_json_array(entries, output_file, encoding="utf8"):
    """ write the entries into a json file (regular json array)

    :param entries: the dictionary of entries 
    :param output_file: path of the output file 
    :param encoding: the encoding to use, default to utf8
    """ 
    with open(output_file, 'w', encoding=encoding) as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def write_json_entries(entries, output_file, encoding="utf8"):
    """ write the entries as json into file, one json entry per line.
    This is the right format to use with `spark.read.json`.

    :param entries: the dictionary of entries 
    :param output_file: path of the output file 
    :param encoding: the encoding to use, default to utf8
    """ 
    with open(output_file, 'w', encoding=encoding) as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False))
            f.write("\n")


if __name__ == "__main__":

    # parse command line arguments
    parser = argparse.ArgumentParser(description='Gather bbc folders into a json or csv file.')
    parser.add_argument('--csv', help='export as csv', action="store_true")
    parser.add_argument('--json', help='export as json', action="store_true")
    parser.add_argument('--verbose', help='be verbose', action="store_true")
    parser.add_argument('--root', default='.', help='root of the downloaded bbc folder')

    args = parser.parse_args()

    if not (args.csv or args.json):
        print("I don't know what you want. ")
        print("Use --json, --csv or both to specify the output file format")
        exit()

    root_dir = path.abspath(args.root)
    output_file = "bbc"

    entries = []    # the entries to export
    all_titles = {} # store already processed titles to avoid duplicats
    duplicates = 0  # count duplicates to print a summary at the end.

    # read all the files into the subfolders and create an entry for each.
    # skip duplicates.
    for filename in glob.iglob(path.join(root_dir, '**/*.txt'), recursive=True):
        entry = {}
        entry['filename'] = filename.replace(root_dir, "")
        entry['category'] = entry['filename'].split("/")[-2]

        try:
            with open(filename, 'r', encoding=encoding) as f:
                lines = [ l for l in f if l.strip() != "" ]

                entry['title'] = lines[0].strip()
                entry['content'] = "".join(lines[1:])
        except:
            print(filename)

        if entry['title'] not in all_titles:
            # avoid adding duplicates
            all_titles[entry['title']] = filename
            entries.append(entry)
        else:
            duplicates+=1
            if args.verbose:
                print("found a duplicate '%s'\n  -> %s\n  -> %s" % 
                    (entry['title'], filename, all_titles[entry['title']]))

    # we have the entries, the only thing to do is to write them into files
    if len(entries) == 0:
        print("no entry found in %s." % root_dir)

    else:
        if args.json:
            write_json_entries(entries, "%s.json" % output_file, encoding)
            print("exported %d entries to %s.json" % (len(entries), output_file))
        if args.csv:
            write_csv(entries, "%s.csv" % output_file, encoding)
            print("exported %d entries to %s.csv" % (len(entries), output_file))

        print("skipped %d duplicates." % duplicates)
