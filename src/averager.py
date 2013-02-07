#!/usr/bin/env python
from optparse import OptionParser
import sys
import csv
from itertools import groupby
import copy

import homework_02.src.common as common
import homework_02.src.cut as cut
import homework_02.src.reformat as reformat
import homework_02.src.timeopen as timeopen


def main():
    r"""
    DESCRIPTION
    -----------
    Gets average for specified column[s], where the data is grouped by the
    value in some column[s].  Specification is done using header values.

    NOTES
    -----
    Assumes the first row is a header and that the file is sorted by the keys.
    Works by converting entries to float.  If an entry cannot be converted an
    exception will be raised
    
    EXAMPLES
    ---------
    Get the average of weight and height for men/women of different age
    $ python averager.py -k sex,age  -f weight,height

    Average a three line string (that we produce with echo)
    $ echo -e "a,b\n1,11\n1,22\n2,33" | python averager.py -k a -f b
    """
    usage = "usage: %prog [options] dataset"
    usage += '\n'+main.__doc__
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-k", "--key",
        help="Comma separated column names from which to make the grouping "
        "key.  [default: %default]. ",
        action="store", dest='key', default=None)
    parser.add_option(
        "-f", "--fieldnames",
        help ="Comma separated list of fields to get an average of.  "
        "[default: %default]. ",
        action="store", dest='fieldnames', default=None)
    parser.add_option(
        "-d", "--delimiter",
        help="Use DELIMITER as the column delimiter.  [default: %default]",
        action="store", dest='delimiter', default=',')
    parser.add_option(
        "-o", "--outfilename",
        help="Write to this file rather than stdout.  [default: %default]",
        action="store", dest='outfilename', default=None)

    (options, args) = parser.parse_args()

    ### Parse args
    # Only deal with the case of one or no infiles
    assert len(args) <= 1
    infilename = args[0] if args else None

    # Deal with tabs
    if options.delimiter in ['t', '\\t', '\t', 'tab']:
        options.delimiter = '\t'

    # Replace some options with a real Python list
    fieldnames = options.fieldnames.split(',')
    key = options.key.split(',')

    ## Get the infile/outfile
    infile, outfile = common.get_inout_files(infilename, options.outfilename)

    ### Call the function that does the real work
    average(infile, outfile, delimiter=options.delimiter, key=key,
        fieldnames=fieldnames)

    ## Close the files iff not stdin, stdout
    common.close_files(infile, outfile)


def average(infile, outfile, delimiter=',', key=None, fieldnames=None):
    """
    Write later, if module interface is needed.
    """
    ## Note, I suggest using python groupby function, which is part of the
    ## itertools module.  

    # Get the csv reader and writer.  Use these to read/write the files.

    ## Compute the average for each group and print


def _get_group_ave(group, field_idx):
    """
    Returns the average of the group at indices in field_idx.

    Parameters
    ----------
    group : itertools._grouper object
        Behaves like a an iterator over a list of lists...sort of
    field_idx : List of indices
        Corresponding the fields we wish to compute averages for
    """
    # The goal is to populate this list then use it to compute the average
    group_sums = [0] * len(field_idx)

    # Loop through the group, keeping track of how many members there are
    for member_count, member in enumerate(group):
        pass
        # Add this group's values to the appropriate index of group_sums
    


if __name__=='__main__':
    main()
