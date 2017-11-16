#
#  Copyright (c) 2017 nexB Inc. and others. All rights reserved.
#
from __future__ import absolute_import

import csv
import json

import click

from deltacode import DeltaCode


def generate_csv(data, result_file):
    """
    Using the OrderedDict generated by DeltaCode.to_dict(), create a .csv file
    containing the primary information from the Delta objects.
    """
    category, new, new_filename, new_sha1, new_size, new_type, new_orig, old,\
        old_filename, old_sha1, old_size, old_type, old_orig = '', '', '', '',\
        '', '', '', '', '', '', '', '', ''
    tuple = ()
    tuple_list = []
    deltas = data

    for delta in deltas:
        category = delta
        for f in deltas[delta]:
            new = '' if delta == 'removed' else f['new']['path']
            new_filename = '' if delta == 'removed' else f['new']['name']
            new_sha1 = '' if delta == 'removed' else f['new']['sha1']
            new_size = '' if delta == 'removed' else f['new']['size']
            new_type = '' if delta == 'removed' else f['new']['type']
            new_orig = '' if delta == 'removed' else f['new']['original_path']
            old = '' if delta == 'added' else f['old']['path']
            old_filename = '' if delta == 'added' else f['old']['name']
            old_sha1 = '' if delta == 'added' else f['old']['sha1']
            old_size = '' if delta == 'added' else f['old']['size']
            old_type = '' if delta == 'added' else f['old']['type']
            old_orig = '' if delta == 'added' else f['old']['original_path']

            tuple = (category, new, old, new_filename, old_filename, new_sha1,
                     old_sha1, new_size, old_size, new_type, old_type, new_orig, old_orig)
            tuple_list.append(tuple)

    with open(result_file, 'wb') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Type of delta', 'New scan path', 'Old scan path',
                          'new_filename', 'old_filename', 'new_sha1', 'old_sha1', 'new_size',
                          'old_size', 'new_type', 'old_type', 'new_original_path', 'old_original_path'])

        for row in tuple_list:
            csv_out.writerow(row)


def generate_json(data, result_file):
    """
    Using the OrderedDict generated by DeltaCode.to_dict(), create a .json file
    containing the primary information from the Delta objects.
    """
    with open(result_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)


@click.command()
@click.help_option('-h', '--help')
@click.option('-n', '--new', required=True, prompt=False, type=click.Path(exists=True, readable=True), help='Identify the path to the "new" scan file')
@click.option('-o', '--old', required=True, prompt=False, type=click.Path(exists=True, readable=True), help='Identify the path to the "old" scan file')
@click.option('-c', '--csv-file', prompt=False, type=click.Path(exists=False), help='Identify the path to the .csv output file')
@click.option('-j', '--json-file', prompt=False, type=click.Path(exists=False), help='Identify the path to the .json output file')
def cli(new, old, csv_file, json_file):
    """
    This script identifies the changes that need to be made to the 'old'
    scan file (-o or -old) in order to generate the 'new' scan file (-n or
    -new).  The results are written to a .csv file (-c or -csv-file) or a
    .json file (-j or -json-file) at a user-designated location.  If no file
    option is selected, the JSON results are printed to the console.
    """

    # do the delta
    delta = DeltaCode(new, old)
    data = delta.to_dict()

    # output to csv
    if csv_file:
        generate_csv(data, csv_file)
    # generate JSON output
    elif json_file:
        generate_json(data, json_file)
    # print to stdout
    else:
        print(json.dumps(data, indent=4))
