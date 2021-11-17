import io


class BinaryFile:

    def __init__(self, file):
        self.file: io.BytesIO = file

    def read_string(self):
        byte_buffer: bytes = b''

        while True:
            byte = self.file.read(1)
            if byte == b'' or byte == b'\x00':
                break
            byte_buffer += byte

        try:
            return byte_buffer.decode("utf-8")
        except UnicodeDecodeError as e:
            raise e
