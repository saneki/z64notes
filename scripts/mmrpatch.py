#!/usr/bin/env python

import argparse
import collections
import csv
import hexdump
import struct
import sys

""" VROM file info. """
VRomFile = collections.namedtuple('VRomFile', ('start', 'end', 'name'))

""" Patch data. """
PatchData = collections.namedtuple('PatchData', ('address', 'offset', 'data'))

class CsvInfo(object):
    """ Handles parsing VRomFile info from a specific CSV file. """
    def __init__(self, vrom_files=tuple()):
        self._vrom_files = vrom_files

    @staticmethod
    def from_file(csvfile):
        """ Construct by parsing VRomFile entries from a CSV file. """
        vrom_files = tuple(CsvInfo.generate_files(csvfile))
        return CsvInfo(vrom_files)

    @staticmethod
    def generate_files(csvfile):
        """
        Parse CSV file with VRomFile list information.

        Reference: "The Ultimate MM Spreadsheet - File List (US) 1.0.csv"
        """
        reader = csv.reader(csvfile)
        for row in reader:
            # Ignore first row of headers
            if row[0] != '#':
                yield VRomFile(start=int(row[1]), end=int(row[2]), name=row[10])

    @property
    def vrom_files(self):
        """ Get the VRomFile entries. """
        return self._vrom_files

    def find(self, address):
        """ Find the VRomFile which contains the given address. """
        for vfile in self.vrom_files:
            if vfile.start <= address < vfile.end:
                return vfile

class InfoWriter(object):
    """ Writes info for PatchData entries. """
    def __init__(self, csv_info=None):
        self._csv_info = csv_info

    @staticmethod
    def from_csv(csvfile):
        """ Construct by parsing VRomFile entries from a CSV file. """
        csv_info = CsvInfo.from_file(csvfile)
        return InfoWriter(csv_info=csv_info)

    @property
    def csv_info(self):
        """ Get the CsvInfo. """
        return self._csv_info

    def print_patch(self, patch, outfile=sys.stdout):
        """ Print patch entry. """
        if self.csv_info:
            vfile = self.csv_info.find(patch.address)
            if vfile is not None:
                offset = patch.address - vfile.start
                print('VRom File:    {:08X}, VRom Offset:  {:08X} >> {}'.format(vfile.start, offset, vfile.name), file=outfile)
        print('VRom Address: {:08X}, Patch Offset: {:08X}'.format(patch.address, patch.offset), file=outfile)
        hex = hexdump.hexdump(patch.data, result='return')
        print('{}'.format(hex), file=outfile)
        print(file=outfile)

    def write(self, patches, outfile=sys.stdout):
        """ Write info about each PatchData to outfile. """
        for patch in patches:
            self.print_patch(patch, outfile=outfile)

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

    writer = None
    if args.vrom_csv is not None:
        with open(args.vrom_csv, 'r') as csvfile:
            writer = InfoWriter.from_csv(csvfile)
    else:
        writer = InfoWriter()

    with open(args.file, 'rb') as f:
        entries = read_patch(f)
        writer.write(entries)

if __name__ == '__main__':
    main()
