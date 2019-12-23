#!/usr/bin/env python

import argparse
import collections
import csv
import hexdump
import struct

""" VROM file info. """
VRomFile = collections.namedtuple('VRomFile', ('start', 'end', 'name'))

""" Patch data. """
PatchData = collections.namedtuple('PatchData', ('address', 'offset', 'data'))

def generate_vrom_file_list_csv(csvfile):
    """
    Parse CSV file with VRom file list information.

    Reference: "The Ultimate MM Spreadsheet - File List (US) 1.0.csv"
    """
    reader = csv.reader(csvfile)
    for row in reader:
        # Ignore first row of headers
        if row[0] != '#':
            yield VRomFile(start=int(row[1]), end=int(row[2]), name=row[10])

def find_file_for_address(address, vrom_files):
    """ Find the VRom file which contains the given address. """
    for vfile in vrom_files:
        if vfile.start <= address < vfile.end:
            return vfile

def print_patch(data, vrom_files):
    """ Print patch entry. """
    if vrom_files is not None:
        vfile = find_file_for_address(data.address, vrom_files)
        if vfile is not None:
            offset = data.address - vfile.start
            print('VRom File:    {:08X}, VRom Offset:  {:08X} >> {}'.format(vfile.start, offset, vfile.name))
    print('VRom Address: {:08X}, Patch Offset: {:08X}'.format(data.address, data.offset))
    hexdump.hexdump(data.data)
    print()

def read_patch(f):
    """ Read all patch entries in a given file. """
    patches = []

    while True:
        pos = f.tell()
        if f.read(1) == b'\xFF':
            return tuple(patches)
        f.seek(pos)

        header = f.read(8)
        if len(header) < 8:
            raise Exception('Incomplete patch header at entry: 0x{:08X}'.format(pos))
        (address, length) = struct.unpack('>II', header)
        data = f.read(length)
        if len(data) != length:
            raise Exception('Incomplete patch data at entry: 0x{:08X}'.format(pos))
        patches.append(PatchData(address, pos, data))

    return tuple(patches)

def get_parser():
    """ Get the argument parser. """
    parser = argparse.ArgumentParser(description='MMR Patch Parser')
    parser.add_argument('-c', '--vrom-csv', help='CSV file with VROM file addresses and names')
    parser.add_argument('file', help='Patch file')
    return parser

def main():
    """ Main function. """
    args = get_parser().parse_args()

    vrom_files = None
    if args.vrom_csv is not None:
        with open(args.vrom_csv, 'r') as csvfile:
            vrom_files = tuple(generate_vrom_file_list_csv(csvfile))

    with open(args.file, 'rb') as f:
        entries = read_patch(f)
        for entry in entries:
            print_patch(entry, vrom_files)

if __name__ == '__main__':
    main()
