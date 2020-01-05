#!/usr/bin/env python

import argparse
import collections
import ctypes
import itertools
import json
import operator
import sys

VRAMMapping = collections.namedtuple('VRAMMapping', ('vrom_start', 'vrom_end', 'vram_start', 'vram_end'))

def deserialize(kls, data):
    """ Deserialize a ctypes instance. """
    inst = kls()
    fit = min(len(data), ctypes.sizeof(inst))
    ctypes.memmove(ctypes.addressof(inst), data, fit)
    success = fit == ctypes.sizeof(inst)
    return (inst, success)

class ArrayDeserializer(object):
    """ Deserializer for arrays of structures in a file. """
    def __init__(self, kls, start, end):
        self._kls = kls
        self._start = start
        self._end = end

    @property
    def kls(self):
        """ Get ctypes type. """
        return self._kls

    @property
    def start(self):
        """ Get file start offset. """
        return self._start

    @property
    def end(self):
        """ Get file end offset. """
        return self._end

    @property
    def size(self):
        """ Get size of full chunk. """
        return self.end - self.start

    @property
    def itemsize(self):
        """ Get size of an individual array item. """
        return ctypes.sizeof(self.kls())

    def generate(self, fp):
        """ Read and generate all entries from a file pointer. """
        fp.seek(self.start)
        while fp.tell() < self.end:
            data = fp.read(self.itemsize)
            inst, success = deserialize(self.kls, data)
            if not success:
                break
            yield inst

class ActorOvl(ctypes.BigEndianStructure):
    """ Actor overlay structure. """
    _fields_ = (
        ('vrom_start', ctypes.c_uint32),
        ('vrom_end',   ctypes.c_uint32),
        ('vram_start', ctypes.c_uint32),
        ('vram_end',   ctypes.c_uint32),
        ('p_ram',      ctypes.c_uint32),
        ('p_init',     ctypes.c_uint32),
        ('p_filename', ctypes.c_uint32),
        ('alloc_type', ctypes.c_uint16),
        ('loaded',     ctypes.c_uint8),
        ('padding',    ctypes.c_uint8),
    )

    @property
    def mapping(self):
        """ Get VRAMMapping. """
        return VRAMMapping(self.vrom_start, self.vrom_end, self.vram_start, self.vram_end)

class PlayerOvl(ctypes.BigEndianStructure):
    """ Player overlay structure. """
    _fields_ = (
        ('p_ram',      ctypes.c_uint32),
        ('vrom_start', ctypes.c_uint32),
        ('vrom_end',   ctypes.c_uint32),
        ('vram_start', ctypes.c_uint32),
        ('vram_end',   ctypes.c_uint32),
        ('unknown',    ctypes.c_uint32),
        ('p_filename', ctypes.c_uint32),
    )

    @property
    def mapping(self):
        """ Get VRAMMapping. """
        return VRAMMapping(self.vrom_start, self.vrom_end, self.vram_start, self.vram_end)

ACTOR_DES  = ArrayDeserializer(ActorOvl, 0x1AEFF0, 0x1B4610)
PLAYER_DES = ArrayDeserializer(PlayerOvl, 0x1D0B70, 0x1D0BA8)

def valid(mapping):
    """ Get whether or not a mapping appears valid. """
    return not (mapping.vrom_start == mapping.vrom_end == 0)

def read(fp):
    """ Read tables from a RAM dump file and return mappings. """
    def mapping(generator):
        """ Get valid mappings from a generator. """
        return tuple(x.mapping for x in generator if valid(x.mapping))
    actors = ACTOR_DES.generate(fp)
    players = PLAYER_DES.generate(fp)
    return {
        'actors': mapping(actors),
        'players': mapping(players),
    }

def print_section(name, items, outfile=sys.stdout):
    """ Print a section of mappings. """
    print('{}:'.format(name), file=outfile)
    for item in items:
        print(' {:08X} => {:08X}'.format(item.vrom_start, item.vram_start), file=outfile)

def dump_json(results, indent=2, outfile=sys.stdout):
    """ Dump as JSON to a file. """
    # Take all values (tuples of VRAMMapping) and concat into one, then sort
    values = (v for (k, v) in results.items())
    values = itertools.chain(*values)
    values = (x._asdict() for x in values)
    array = sorted(values, key=lambda x: x['vrom_start'])
    json.dump(array, outfile, indent=indent)

def get_parser():
    """ Get the argument parser. """
    parser = argparse.ArgumentParser(description="Dump RAM tables from Majora's Mask (VROM -> VRAM)")
    parser.add_argument('-j', '--to-json', action='store_true', help='Output as JSON')
    parser.add_argument('file', help='RAM dump file')
    return parser

def main():
    """ Main function. """
    args = get_parser().parse_args()
    with open(args.file, 'rb') as fp:
        results = read(fp)
        if args.to_json:
            dump_json(results)
        else:
            for name, items in results.items():
                print_section(name, items)

if __name__ == '__main__':
    main()
