#!/usr/bin/env python
from optparse import OptionParser
import sys
import csv
import homework_02.src.common as common

# pdb.set_trace()


def main():
    r"""
    Reads a comma delimited file, reformats, prints to stdout.  
    
    The reformat actions are:
    1) Converts header to lowercase
    2) Converts spaces to underscores in the header
    3) If a row has different number of items than the header
       (empty items still count as items), do not reformat+print it,
       instead print an error message to stderr.
    4) Remove pipes from the body
    5) Converts comma delimiters (NOT quoted commas e.g. "NY, NY.") to pipes.

    Examples
    ---------
    Read a comma delimited csv file, data.csv, reformat,
    print to stdout
    $ python cleanheader.py test/commafile.csv

    Use a tab delimited dataset 
    $ python cleanheader.py -d \t test/tabfile.csv
    Note that -dt  -dtab -d\t -d'\t' -d\\t  also work
    """
    usage = "usage: %prog [options] dataset"
    usage += '\n'+main.__doc__
    parser = OptionParser(usage=usage)
    # Note that delimiter is not given as an option because delimiter choices
    # are "hard coded" into the functionality of this utility
    parser.add_option(
        "-o", "--outfilename",
        help="Write to this file rather than stdout.  [default: %default]",
        action="store", dest='outfilename', default=None)

    (options, args) = parser.parse_args()

    ### Parse args
    # Only deal with the case of one or no infiles
    assert len(args) <= 1
    infilename = args[0] if args else None

    ## Get the infile/outfile
    infile, outfile = common.get_inout_files(infilename, options.outfilename)

    ### Call the function that does the real work
    reformat(infile, outfile)

    ## Close the files iff not stdin, stdout
    common.close_files(infile, outfile)


def reformat(infile, outfile, errfile=sys.stderr):
    """
    Write later, if module interface is needed.
    """
    # Get the csv reader and writer.  Use these to read/write the files.
    reader = csv.reader(infile, delimiter=',')
    writer = csv.writer(outfile, delimiter='|', quotechar = '"')

    # Extract the first row of the file
    header = reader.next()

    ## Reformat and write the header
    header_new = _reformat_header(header)
    len_header = len(header_new)
    writer.writerow(header_new)

    ## Reformat and write the body
    for row_index, row in enumerate(reader):
        # Ca
        try:
            # Call _checkrowlength, get a new_row, write it
            _checkrowlength(row, row_index, len_header)
            
            # chance wrtier to _reformate_item
            new_row = [_reformat_item(item) for item in row]
            writer.writerow(new_row)
            pass
        except common.BadDataError as e:
            errfile.write(e.message)
            pass


def _checkrowlength(row, row_index, len_header):
    """
    Does nothing iff the row length is the same as the header length.
    If not, raise a BadDataError with an appropriate message.

    Parameters
    ----------
    row : List
        One row of the file
    row_index : Integer
        The index in the file corresponding to this row
    len_header : Integer
        The length of the header
    """
    # Your stderr message should be:
    # message = 'BadDataError. %d items in row %d.  Should have been %d. '\
    # 'Row = %s\n' % (len(row), row_index, len_header, row)
    if len(row) != len_header:
        message = 'BadDataError. %d items in row %d.  Should have been %d. '\
                'Row = %s\n' % (len(row), row_index, len_header, row)
        raise common.BadDataError(message)
        

def _reformat_item(item):
    """
    Reformat an item in a row in the body of the file:

    1) Replaces pipes with nothing ''

    Parameters
    ----------
    item : String
        Does NOT contain newlines.  One row of the file

    Returns
    -------
    The reformatted item
    """
    # Comma delimiters are replaced by pipes courtesy of the reader/writer
    #  delimiter choices.
    #
    # double quotes are replaced by the reader/writer (default) choice of
    # quote character

    # Replace pipes in the text body with nothing '' (no space)
    new_item = item.replace("|", "")
    return new_item


def _reformat_header(header):
    """
    Returns a reformatted header:

    1) Replaces spaces with underscores
    2) Converts upper to lower case

    Parameters
    ----------
    header : List of Strings
        Header from infile, as read by a csv reader
    """
    new_header = []
    for hd in header:
        hd = hd.lower()
        hd = hd.replace(' ', '_')
        new_header.append(hd)

    # Loop through the header and populate new_header
        # Replace spaces with underscores
        # Change to lower case

    return new_header



if __name__=='__main__':
    main()


