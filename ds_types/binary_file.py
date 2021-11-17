import io


class BinaryFile:

    def __init__(self, file):
        self.file: io.BytesIO = file
