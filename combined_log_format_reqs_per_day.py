#!/usr/bin/env python

"""
This is a simple program to count default Combined Log Format (Nginx) log requests per day (presuming default log format).


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

import sys
from collections import Counter
import datetime


def read_lines(lst):
    """Read file list"""
    lines = []
    for fname in lst:
        with open(fname) as fo:
            lines.extend(fo.readlines())
    if not lst:
        print >>sys.stderr, "Input files list empty?"
    return lines


def print_date_sorted(counter):
    """Output reqs/day sorted by date"""
    dates = counter.keys()
    dates.sort(key=lambda x: datetime.datetime.strptime(x, '%d/%b/%Y'))
    for key in dates:
        print key, counter[key]


def proc_logs(lines):
    """Count log lines per day"""
    counts = Counter()
    for line in lines:
        line_lists = line.split()
        dates = line_lists[3]
        s_date = dates.strip('[').strip(']').split()
        s_date = s_date[0].split(':')[0]
        counts[s_date] += 1
    print_date_sorted(counts)


if __name__ == '__main__':
    log_lines = read_lines(sys.argv[1:])
    proc_logs(log_lines)

