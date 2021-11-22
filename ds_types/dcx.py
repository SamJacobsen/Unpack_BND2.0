import zlib, struct

from ds_types.binary_file import BinaryFile


class DCX(BinaryFile):

    HEADER = b'DCX'

    def __init__(self, file):
        super(DCX, self).__init__(file)

        magic = self.file.read(4)[:-1]
        if magic == DCX.HEADER:

            self.name = [self.file.name.removesuffix('.dcx')]
            # todo: Read the full header, and check if the file is DEFLATE or EDGE
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
