#!/usr/bin/env python2

"""
This program converts timestamp="1234567890" to time=""


The MIT License (MIT)

Copyright (c) 2017 Marcin Krol <mrkafk@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import re
import datetime
import codecs
import os
import sys

def proc_file(lines, divide_by=1000):
    '''Replace numeric tiimestamp with datetime in list of lines.'''
    new_lines = []
    for line in lines:
        match = re.search(r'timestamp="\d+"', line, re.IGNORECASE)
        if match:
            tstamp_str = match.group()
            tstamp = tstamp_str.replace('timestamp', '').replace(
                '"', '').replace("'", '').replace('=', '')
            try:
                tstamp = int(tstamp) / divide_by
                line = line.replace(tstamp_str, 'timestamp="{}"'.format(
                    datetime.datetime.fromtimestamp(tstamp).strftime('%Y/%m/%d %H:%M:%S')))
            except ValueError:
                pass
        new_lines.append(line)
    return new_lines

def proc_files(files):
    """Read file list"""
    lines = []
    for fname in files:
        print 'Processing ', fname,
        try:
            with codecs.open(fname, 'r', encoding='utf-8', errors='replace')  as fobj:
                lines = proc_file(fobj.readlines())
                with codecs.open(fname, 'wb', encoding='utf-8', errors='replace') as fobj:
                    fobj.write(os.sep.join(lines))
        except IOError as e:
            print e,
        print
    if not files:
        print >>sys.stderr, "Input files list empty?"
    return lines


def parse_opts():
    '''Parse cmdline.'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inplace", action="store_true")
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    CMDLINE_ARGS = parse_opts()
    if not CMDLINE_ARGS.inplace:
        print >>sys.stderr, "Confirm rewriting in place by adding -i option."
        sys.exit(1)
    FNAMES = CMDLINE_ARGS.files
    if not FNAMES:
        print >>sys.stderr, "List of files to process is empty."
        sys.exit(1)
    proc_files(FNAMES)
