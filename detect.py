from screen import Screen

import os
import os.path
import sys
from glob import glob

__author__ = 'Konst Kolesnichenko'

if __name__ == '__main__':
    fnames = "../data/roadsign.jpg" if len(sys.argv) <= 1 else sys.argv[1]
    out_format = "png" if len(sys.argv) <= 2 else sys.argv[2]
    out_dir = "../data/processed/"

    sheets = []
    # Here we are processing all files one by one and also generating
    # index sheet for it
    for fname in glob(fnames):
        sheet_name = os.path.splitext(os.path.basename(fname))[0]

        print("Processing file %s" % fname)
        sheet = Screen(fname, sheet_name, out_dir, out_format)

