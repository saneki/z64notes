#!/usr/bin/env python

import argparse
import struct

from subprocess import check_call as call

MAGIC = struct.unpack('>I', 'Yaz0'.encode('utf-8'))[0]

def find_yaz0_offsets(stream):
    """Find all Yaz0 chunk offsets."""
    while True:
        position = stream.tell()
        magic = read_uint32(stream)
        if magic is None:
            break
        if magic == MAGIC:
            yield position

def offsets_to_pairs(offsets):
    """
    Example: (1, 2, 3, 4) => ((1, 2), (2, 3), (3, 4), (4, None))
    """
    for i in range(len(offsets)):
        if i == len(offsets) - 1:
            yield offsets[i], None
        else:
            yield offsets[i], offsets[i+1]

def read_chunk(stream, start, end):
    """Read a chunk from start offset to end offset."""
    stream.seek(start)
    if end is not None:
        return stream.read(end - start)
    else:
        # Read until EOF
        return stream.read()

def read_uint32(stream):
    """Read a big-endian 32-bit integer."""
    data = stream.read(4)
    if len(data) < 4:
        return None
    else:
        return struct.unpack('>I', data)[0]

def get_parser():
    """Get the argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decompress', action='store_true', help='Decompress Yaz0 using yaztool')
    parser.add_argument('file', help='N64 ROM file')
    return parser

def main():
    """Main function."""
    args = get_parser().parse_args()

    with open(args.file, 'rb') as stream:
        print('Finding Yaz0 offsets...')
        offsets = tuple(find_yaz0_offsets(stream))
        print('Found {}'.format(len(offsets)))
        pairs = offsets_to_pairs(offsets)
        for (start, end) in pairs:
            print('Reading chunk: 0x{:08X}'.format(start))
            chunk = read_chunk(stream, start, end)
            filename = '{:08X}.yaz0'.format(start)
            with open(filename, 'wb') as yf:
                yf.write(chunk)
            if args.decompress:
                # Decompress using yaztool
                call(['yaztool', 'decompress', filename, '{}.bin'.format(filename)])

if __name__ == '__main__':
    main()
