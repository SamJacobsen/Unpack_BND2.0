import io, os

from abc import ABC, abstractmethod


class BinaryFile(ABC):

    def __init__(self, file: io.BytesIO):
        self.file = file

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> tuple:
        pass

    @staticmethod
    def write(full_path: str, data) -> None:
        path, file_name = os.path.split(full_path)
        path = os.path.splitdrive(path)[1][1:]
        file_name = os.path.join(path, file_name)

        if not os.path.exists(path):
            os.makedirs(path)

        with open(file_name, 'wb') as writer:
            writer.write(data)

    def read_string(self) -> str:
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
