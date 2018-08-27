class Register(object):
    """register of an architecture
    """
    def __init__(self, group={}, name=''):
        """
        initializes a register or a register group.

        A register group is a set of registers which shares
        a common register, but with different name when using
        as different size. This is quite common in x86 or x86-64
        architecture.

        For example, eax and ax belong to the same register group.
        
        If a register is not a group, pass a keyword argument says its name.

        Kwargs:
            group: a dictionary describing a register group, key is the name
                   of a register, value is the size in bytes. If a register
                   cannot be used as a register group, ignore this argument.

            name: a string describing the name of this register, if a register
                  cannot be used as a register group, this field is required.

            argn: argument number, if a register 

        """
        if group != {}:
            self.is_group = False
            self.name = name
        else:
            self.is_group = True
            self.group = group

    def __eq__(self, other):
        if self.is_group:
            return other in self.group
        else:
            return self.name == other
    

class Arch(object):
    """architecture object
    """

    ENDIAN_BE = 0
    ENDIAN_LE = 1

    def __init__(self, is_gdb):
        self.is_gdb = is_gdb
        if is_gdb:
            import gdb
            self.gdb = gdb

    @property
    def name(self):
        """architecture name
        """
        return ''

    @property
    def pc(self):
        if is_gdb:
            return long(self.gdb.parse_and_eval('$pc'))
        else:
            raise NotImplemented('architecture not implemented pc value')

    @property
    def sp(self):
        if is_gdb:
            return long(self.gdb.parse_and_eval('$sp'))
        raise NotImplemented('architecture not implemented sp value')

    @property
    def fp(self):
        if is_gdb:
            return long(self.gdb.parse_and_eval('$fp'))
        raise NotImplemented('architecture not implemented fp value')

    def register_value(self, register):
        """gets register value

        Args:
            register: register to get value

        """
        if is_gdb:
            if register.is_group:
                register_name = \
                    max(register.group.iteritems(), key=operator.itemgetter(1))[0]
                return long(self.gdb.parse_and_eval(register_name))
            else:
                return long(self.gdb.parse_and_eval(register))

    @property
    def registers(self):
        """registers of this architecture
        """
        return []

    @property
    def pointer_size(self):
        return 0

    @property
    def endianness(self):
        raise NotImplemented('endianness not defined')

    # TODO add more architecture dependent information


class ArchX86(Arch):
    """x86 architecture
    """

    @property
    def name(self):
        return 'x86'

    @property
    def registers(self):
        return [
            Register(group={'eax': 4, 'ax': 2, 'al': 1, 'ah': 1}),
            Register(group={'ebx': 4, 'bx': 2, 'bl': 1, 'bh': 1}),
            Register(group={'ecx': 4, 'cx': 2, 'cl': 1, 'ch': 1}),
            Register(group={'edx': 4, 'cx': 2, 'dl': 1, 'dh': 1}),
            Register(group={'edi': 4, 'di': 2}),
            Register(group={'esi': 4, 'si': 2}),
            Register(group={'ebp': 4, 'bp': 2}),
            Register(group={'esp': 4, 'sp': 2}),
            Register(group={'eip': 4}),
            Register(group={'eflags': 4}),
            Register(group={'ss': 1}),
            Register(group={'cs': 1}),
            Register(group={'ds': 1}),
            Register(group={'es': 1}),
            Register(group={'fs': 1}),
            Register(group={'gs': 1}),
        ]

    @property
    def endianess(self):
        return Arch.ENDIAN_LE

    def register_value(self, register):
        unable_table = self.registers[-2:]
        if register in unable_table:
            # TODO fix this
            return None
        else:
            return Arch.register_value(self, register)

class ArchX86_64(Arch):
    """x86_64 architecture
    """

    @property
    def name(self):
        return 'x86_64'

    @property
    def registers(self):
        return [
            Register(group={'rax': 8, 'eax': 4, 'ax': 2, 'ah': 1, 'al': 1}),
            Register(group={'rbx': 8, 'ebx': 4, 'bx': 2, 'bh': 1, 'bl': 1}),
            Register(group={'rcx': 8, 'ecx': 4, 'cx': 2, 'ch': 1, 'cl': 1}),
            Register(group={'rdx': 8, 'edx': 4, 'dx': 2, 'dh': 1, 'dl': 1}),
            Register(group={'rsp': 8, 'esp': 4, 'sp': 2, 'spl': 1}),
            Register(group={'rbp': 8, 'ebp': 4, 'bp': 2, 'bpl': 1}),
            Register(group={'rsi': 8, 'esi': 4, 'si': 2, 'sil': 1}),
            Register(group={'rdi': 8, 'edi': 4, 'di': 2, 'dil': 1}),
            Register(group={'r8': 8, 'r8d': 4, 'r8w': 2, 'r8b': 1}),
            Register(group={'r9': 8, 'r9d': 4, 'r9w': 2, 'r9b': 1}),
            Register(group={'r10': 8, 'r10d': 4, 'r10w': 2, 'r10b': 1}),
            Register(group={'r11': 8, 'r11d': 4, 'r11w': 2, 'r11b': 1}),
            Register(group={'r12': 8, 'r12d': 4, 'r12w': 2, 'r12b': 1}),
            Register(group={'r13': 8, 'r13d': 4, 'r13w': 2, 'r13b': 1}),
            Register(group={'r14': 8, 'r14d': 4, 'r14w': 2, 'r14b': 1}),
            Register(group={'r15': 8, 'r15d': 4, 'r15w': 2, 'r15b': 1}),
            Register(group={'eflags': 8}), # rflags so called
            Register(group={'ss': 2}),
            Register(group={'cs': 2}),
            Register(group={'ds': 2}),
            Register(group={'es': 2}),
            Register(group={'fs': 2}),
            Register(group={'gs': 2}),
        ]

    @property
    def endianness(self):
        return Arch.ENDIAN_LE

    def register_value(self, register):
        unable_table = self.registers[-2:]
        if register in unable_table:
            # TODO fix this
            return None
        else:
            return Arch.register_value(self, register)
