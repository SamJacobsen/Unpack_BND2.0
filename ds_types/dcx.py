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
            self._name = [self.file.name.removesuffix('.dcx')]
            self._format_method = self._header[40:44].decode('utf-8')

            match self._format_method:
                case 'EDGE':
                    self._format = EDGE(self.file)
                case 'DFLT':
                    print('deflate format')
        else:
            raise Exception("Invalid header in dcx file")

    def has_next(self):
        pass
        # if len(self.name) > 0:
        #     return True
        # return False

    def next(self):
        pass
        # file_path: str = self.name.pop(0)
        # decompressed_data = zlib.decompress(self.file.read())
        # return file_path, decompressed_data


class EDGE:

    HEADER = b'EgdT'
    FIXED_HEADER_SIZE = 36

    def __init__(self, file):
        self._file = file
        self._header = self._file.read(EDGE.FIXED_HEADER_SIZE)

        magic = self._header[0:4]
        if magic == EDGE.HEADER:
            self._edge_size = struct.unpack('>i', self._header[24:28])[0]
            self._block_count = struct.unpack('>i', self._header[28:32])[0]

            offset, size = self._read_struct_block()
            self._file.seek(offset)
            block = zlib.decompress(self._file.read(size), -zlib.MAX_WBITS)
            print(block)
        else:
            raise Exception("Invalid header in edge")

    def _read_struct_block(self):
        self._file.read(4)
        data_offset = struct.unpack('>i', self._file.read(4))[0] + self._edge_size + DCX.FIXED_HEADER_SIZE
        data_size = struct.unpack('>i', self._file.read(4))[0]
        self._file.read(4)
        return data_offset, data_size
