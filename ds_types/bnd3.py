import os
import struct

from typing import List
from ds_types.binary_file import BinaryFile


class PackedFile:

    def __init__(self, size, data_offset, file_id, name_offset):
        self.size = size
        self.data_offset = data_offset
        self.file_id = file_id
        self.name_offset = name_offset

        self._name = ''

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name


class BND3(BinaryFile):

    TYPE = b'BND3'

    @staticmethod
    def write(packed_file: PackedFile, data):
        path, file_name = os.path.split(packed_file.get_name())
        path = os.path.splitdrive(path)[1][1:]
        file_name = os.path.join(path, file_name)

        os.makedirs(path)

        with open(file_name, 'wb') as writer:
            writer.write(data)

    def __init__(self, file):
        super(BND3, self).__init__(file)

        self.packedFiles: List[PackedFile] = []

        magic = self.file.read(4)

        if magic == BND3.TYPE:
            version = self.file.read(8)
            format = self.file.read(4).hex()

            if format[2:6] == '0101':
                self.endianness = '>'
            else:
                self.endianness = '<'

            self.fileCount = struct.unpack(self.endianness + 'i', self.file.read(4))[0]
            self.headerEnd = struct.unpack(self.endianness + 'i', self.file.read(4))[0]
            self.file.read(8)

            self._read_files_metadata()
            self._read_packed_file_name()
        else:
            raise Exception("Invalid header in bnd file")

    def _read_files_metadata(self):

        for x in range(self.fileCount):
            self.file.read(4)
            size_compressed = struct.unpack(self.endianness + 'i', self.file.read(4))[0]
            data_offset = struct.unpack(self.endianness + 'I', self.file.read(4))[0]
            file_id = struct.unpack(self.endianness + 'i', self.file.read(4))[0]
            name_offset = struct.unpack(self.endianness + 'i', self.file.read(4))[0]
            size = struct.unpack(self.endianness + 'i', self.file.read(4))[0]

            packed_file = PackedFile(size, data_offset, file_id, name_offset)
            self.packedFiles.append(packed_file)

    def _read_packed_file_name(self):
        self.file.seek(0, os.SEEK_SET)  # Set the read head to the begging of the file

        for packed_file in self.packedFiles:
            self.file.seek(packed_file.name_offset)  # Set the read head to the begging of the packed file name offset
            packed_file.set_name(self.read_string())

    def has_next(self):
        if len(self.packedFiles) > 0:
            return True
        return False

    def next(self):
        packed_file = self.packedFiles.pop(0)
        self.file.seek(packed_file.data_offset)  # Set the read head to data offset
        data = self.file.read(packed_file.size)

        return packed_file, data
