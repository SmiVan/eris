#!/usr/bin/env python3
# Whiff - Visual diff.

from sys import argv
import os
import math

GUD = '░' # 'O' '░'
BAD = '╳' # 'X' '█'

def whiff(orig, corr, display_units):
            # go to ends of files
            orig.seek(0, os.SEEK_END)                      
            corr.seek(0, os.SEEK_END)

            # get file sizes
            size_orig, size_corr = orig.tell(), corr.tell()

            # rewind files
            orig.seek(0, os.SEEK_SET)
            corr.seek(0, os.SEEK_SET)

            # figure out chunk size per display unit
            max_size = max(size_orig, size_corr)

            if max_size < display_units:
                display_units = max_size
            
            chunk_size = math.floor(max_size / display_units)

            # compare
            for unit in range(0, display_units):
                orig_chunk, corr_chunk = orig.read(chunk_size), corr.read(chunk_size)

                # print(orig_chunk, "==", corr_chunk)
                # print("=", orig_chunk == corr_chunk)

                print("%c" % (GUD if orig_chunk == corr_chunk else BAD), end="")
            
            # newline
            print()

def main():
    arg_len = len(argv) 

    name = argv[0].split('/')[-1]

    if arg_len < 3:
        print("Whiff - Visual diff.")
        print("Usage: %s <original> <corrupt> [display_units]" % name)
        exit()

    original_file = argv[1]
    corrupt_file  = argv[2]
    display_units = 60 if arg_len < 4 else int(argv[3])
    
    with open(original_file, 'rb') as orig:
        with open(corrupt_file, 'rb') as corr:
            whiff(orig, corr, display_units)

main()
            
