#!/usr/bin/env python3
# Eris - File Corruption Generator.

from sys import argv
import os
import math

arg_len = len(argv)

prog_name = argv[0].split('/')[-1]

if arg_len < 3:
    print("Eris - File Corruption Generator.")
    print("Usage: %s <file> <methods...>" % prog_name)
    print("     Methods:")
    print("      - size")
    print("         ↳ Prints file size in hexadecimal.")
    print("      - set <where> <value>")
    print("         ↳ Set a byte to a value in the range of [0x00, 0xFF].")
    print("      - copy <how-much> <from> <to>")
    print("         ↳ Copies a number of bytes from one position to another.")
    print("      - swap <how-much> <from> <to>")
    print("         ↳ Swaps a number of bytes between two positions.")
    print("      - recover <from> <to>")
    print("         ↳ Returns the bytes in [from, to) to their original values.")
    print("      - save")
    print("         ↳ Saves the corrupted file.")
    print("      - export <infix>")
    print("         ↳ Exports the corrupted file with the above infix.")
    exit()


original_file = argv[1]

# Method helper functions:

def export_with_infix(buf, infix):
    split = original_file.split('.')
    corrupt_file = ".".join(split[:-1]) + "." + infix + "." + split[-1]
    with open(corrupt_file, 'wb') as corr:
        corr.write(buf)

# METHODS BEGIN

def method_size():
    def do(_, buf):
        size = len(buf)
        print(hex(size))
    return do

method_size.args = 0

def method_save():
    def do(_, buf):
        export_with_infix(buf, "eris")
    return do

method_save.args = 0

def method_export(infix):
    def do(_, buf):
        export_with_infix(buf, infix + ".eris")
    return do

method_export.args = 1

def method_set(pos, value):
    value = int(value, 0)
    pos = int(pos, 0)
    if value < 0x00 or value > 0xFF:
        print("Byte value out of range in 'set': " + hex(value))
        exit(0xFF)
    def do(_, buf):
        buf[pos] = value

    return do

method_set.args = 2


def method_copy(count, origin, destination):
    count = int(count, 0)
    origin = int(origin, 0)
    destination = int(destination, 0)
    def do(_, buf):
        buf[destination:destination+count] = buf[origin:origin+count]

    return do

method_copy.args = 3

def method_swap(count, origin, destination):
    count = int(count, 0)
    origin = int(origin, 0)
    destination = int(destination, 0)
    def do(_, buf):
        buf[destination:destination+count], buf[origin:origin+count] = buf[origin:origin+count], buf[destination:destination+count]

    return do

method_swap.args = 3

def method_recover(start, end):
    start = int(start, 0)
    end = int(end, 0)
    def do(orig, buf):
        orig.seek(start, os.SEEK_SET)
        buf[start:end] = orig.read(end-start)

    return do

method_recover.args = 2

# METHODS ENDED


def read_method_and_args(index):
    method_name = argv[index].lower() 
    # TODO: refine this into a dictionary lookup instead

    # method lookup
    if   method_name == "size":
        method_maker = method_size
    elif method_name == "save":
        method_maker = method_save
    elif method_name == "export":
        method_maker = method_export
    elif method_name == "set":
        method_maker = method_set
    elif method_name == "copy":
        method_maker = method_copy
    elif method_name == "swap":
        method_maker = method_swap
    elif method_name == "recover":
        method_maker = method_recover
    else:
        print("Unknown method:", method_name)
        exit(0xBAD)

    # gather arguments
    args = argv[index + 1 : index + method_maker.args + 1]

    # progress index
    index = index + method_maker.args + 1

    return (method_maker, args, index)
    

methods = []
index = 2
while index < len(argv):
    (method_maker, args, index) = read_method_and_args(index)
    methods.append(method_maker(*args)) # *args unpacks args for the call


# Apply methods
with open(original_file, 'rb') as orig:
    buffer = bytearray(orig.read())

    for method in methods:
        method(orig, buffer)


            
