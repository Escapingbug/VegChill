"""
mapping related functionality
"""
import six

class Mapping(object):
    """a memory mapping
    """

    def __init__(self, start, end, offset, perm, path=''):
        # type: (int, int, int, str, str)
        self.start = start
        self.end = end
        self.offset = offset
        self.perm = perm
        self.path = path


class MemoryMappings(object):
    """memory mappings, describing whole memory mappings
    """
    
    def __init__(self):
        self.mappings = [] # type: Mapping
    
    @staticmethod
    def parse_from_pid(vegchill, pid):
        """parses mapping from mapping file of some process

        Args:
            vegchill: vegchill main object
            pid: process id

        Returns:
            a MemoryMappings object describing the memory
        """
        # type: (VegChill, int) -> MemoryMappings
        map_file_path = '/proc/%d/maps' % pid
        try:
            with open(map_file_path, 'r') as f:
                map_lines = f.readlines()
        except FileNotFoundError as e:
            vegchill.err('mapping file %s not found' % map_file_path)

        return MemoryMappings.parse_from_mapping(vegchill, map_lines)

    @staticmethod
    def parse_mapping_line(vegchill, mapping_line):
        """parses a line from mapping

        Args:
            vegchill: vegchill main object
            mapping_line: a line of mapping file

        Returns:
            a Mapping object describing this mapping

        """
        parts = mapping_line.split()
        part_splits = parts[0].split('-')
        start = int(part_splits[0], 16)
        end = int(part_splits[1], 16)
        perm = parts[1]
        offset = int(parts[2], 16)
        path = parts[-1]
        return Mapping(start, end, offset, perm, path)

    @staticmethod
    def parse_from_mapping(vegchill, mapping_lines):
        """does parse from mapping file

        Args:
            vegchill: vegchill main object
            mapping_lines: lines read from mapping file

        Returns:
            a MemoryMappings object describing the memory

        """
        # type: (VegChill, str) -> MemoryMappings
        mappings = MemoryMappings()
        mappings.mappings = \
            list(map(lambda x: MemoryMappings.parse_mapping_line(vegchill, x), mapping_lines))
        return mappings
