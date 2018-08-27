"""simple elf header parse

Mostly copied from gef (https://github.com/hugsy/gef).
"""
import os
import struct

class ElfConstants(object):
    """elf constants
    """
    BIG_ENDIAN = 0
    LITTLE_ENDIAN = 1

    ELF_32_BITS = 0x1
    ELF_64_BITS = 0x2

    # architecture flags
    X86_64 = 0x3e
    X86_32 = 0x03
    ARM = 0x28
    MIPS = 0x08
    POWERPC = 0x14
    POWERPC64 = 0x15
    SPARC = 0x02
    SPARC64 = 0x2b
    AARCH64 = 0xb7

    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4

    ARCH_NAME_TABLE = {
        X86_64: 'x86_64',
        X86_32: 'x86',
        ARM: 'arm',
        MIPS: 'mips',
        POWERPC: 'powerpc',
        POWERPC64: 'powerpc64',
        SPARC: 'sparc',
        SPARC64: 'sparc64',
        AARCH64: 'aarch64',
    }


class Elf(object):
    e_magic = b'\x7fELF'
    e_class = ElfConstants.ELF_32_BITS
    e_endianness = ElfConstants.LITTLE_ENDIAN
    e_eiversion = None
    e_osabi = None
    e_abiversion = None
    e_pad = None
    e_type = ElfConstants.ET_EXEC
    e_machine = ElfConstants.X86_32
    e_version = None
    e_entry = 0x0
    e_phoff = None
    e_shoff = None
    e_flags = None
    e_ehsize = None
    e_phentsize = None
    e_phnum = None
    e_shentsize = None
    e_shnum = None
    e_shstrndx = None

    def __init__(self, vegchill, elf=''):
        """
        Args:
            vegchill: VegChill main object
            elf: elf path

        """
        if not os.access(elf, os.R_OK):
            vegchill.err("'{} not found/readable'".format(elf))
            return

        with open(elf, 'rb') as f:
            # off 0x0
            self.e_magic, self.e_class, self.e_endianness, self.e_eiversion = struct.unpack('>IBBB', f.read(7))

            endian = '<' if self.e_endianness == ElfConstants.LITTLE_ENDIAN else '>'

            # off 0x7
            self.e_osabi, self.e_abiversion = struct.unpack('%sBB' % endian, f.read(2))
            # off 0x9
            self.e_pad = f.read(7)
            # off 0x10
            self.e_type, self.e_machine, self.e_version = struct.unpack('%sHHI' % endian, f.read(8))
            # off 0x18
            if self.e_class == ElfConstants.ELF_64_BITS:
                self.e_entry, self.e_phoff, self.e_shoff = struct.unpack('%sQQQ' % endian, f.read(24))
            else:
                # arch 32 bits
                self.e_entry, self.e_phoff, self.e_shoff = struct.unpack('%sIII' % endian, f.read(12))

            self.e_flags, self.e_shsize, self.e_phentsize, self.e_phnum = struct.unpack('%sHHHH' % endian, f.read(8))
            self.e_shentsize, self.e_shnum, self.e_shstrndx = struct.unpack('%sHHH' % endian, f.read(6))

    def arch_name(self):
        """gets architecture name in string
        """
        return ElfConstants.ARCH_NAME_TABLE[self.e_machine]
