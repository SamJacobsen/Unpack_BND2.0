import os.path
import zlib, struct

from ds_types.binary_file import BinaryFile


class DCX(BinaryFile):

    HEADER = b'DCX'
    FIXED_HEADER_SIZE = 76

    def __init__(self, file):
        super(DCX, self).__init__(file)
        self._header = self.file.read(DCX.FIXED_HEADER_SIZE)

        magic = self._header[0:3]
        if magic == DCX.HEADER:
            self._name = os.path.basename(self.file.name.removesuffix('.dcx'))
            self._format_method = self._header[40:44].decode('utf-8')

            match self._format_method:
                case 'EDGE':
                    self._format = EDGE(self.file)
                case 'DFLT':
                    print('deflate format')
        else:
            raise Exception("Invalid header in dcx file")

    def has_next(self) -> bool:
        return self._format.has_next()

    def next(self):
        return self._name, self._format.decompress()


class EDGE:

    HEADER = b'EgdT'
    FIXED_HEADER_SIZE = 36

    def __init__(self, file):
        self._file = file
        self._header = self._file.read(EDGE.FIXED_HEADER_SIZE)
        self._has_next = True

        magic = self._header[0:4]
        if magic == EDGE.HEADER:
            self._edge_size = struct.unpack('>i', self._header[24:28])[0]
            self._block_count = struct.unpack('>i', self._header[28:32])[0]

            self._blocks = []
            while len(self._blocks) < self._block_count:
                self._blocks.append(self._read_struct_block())
        else:
            raise Exception("Invalid header in edge")

    def _read_struct_block(self):
        self._file.read(4)
        data_offset = struct.unpack('>i', self._file.read(4))[0] + self._edge_size + DCX.FIXED_HEADER_SIZE
        data_size = struct.unpack('>i', self._file.read(4))[0]
        self._file.read(4)
        return data_offset, data_size

    def has_next(self) -> bool:
        return self._has_next

    def decompress(self) -> bytes:
        decompressed = bytearray()
        for offset, size in self._blocks:
            self._file.seek(offset)
            decompressed += zlib.decompress(self._file.read(size), -zlib.MAX_WBITS)

        self._has_next = False
        return bytes(decompressed)
