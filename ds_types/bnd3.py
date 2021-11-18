import struct

class BND3:
    TYPE = b'BND3'

    def __init__(self, file):
        self.bndFile = open(file, 'rb')
        self.packedFiles = []

        magic = self.bndFile.read(4)

        if magic == BND3.TYPE:
            version = self.bndFile.read(8)
            format = self.bndFile.read(4).hex()

            if format[2:6] == '0101':
                self.endianness = '>'
            else:
                self.endianness = '<'

            self.fileCount = struct.unpack(self.endianness + 'i', self.bndFile.read(4))[0]
            self.headerEnd = struct.unpack(self.endianness + 'i', self.bndFile.read(4))[0]
            self.bndFile.read(8)

            self.readFilesMetadata()
        else:
            raise Exception("Invalid header in bnd file")

    def readFilesMetadata(self):
        print("\n")
        for x in range(self.fileCount):
            self.bndFile.read(4)
            sizeCompressed = struct.unpack(self.endianness + 'i', self.bndFile.read(4))[0]
            dataOffset = struct.unpack(self.endianness + 'I', self.bndFile.read(4))[0]
            id = struct.unpack(self.endianness + 'i', self.bndFile.read(4))[0]
            pathOffset = struct.unpack(self.endianness + 'i', self.bndFile.read(4))[0]
            size = struct.unpack(self.endianness + 'i', self.bndFile.read(4))[0]
            print(size)

    def hasNext(self):
        if self.fileCount > 0:
            return True
        else:
            return False

    def readFile(self):
        print()