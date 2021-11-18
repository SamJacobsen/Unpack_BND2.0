import os

from ds_types.bnd3 import BND3

class packedFile:
    def __init__(self, size, dataOffset, id, pathOffset):
        pass

if __name__ == '__main__':
    path = 'bnd'
    for file in os.scandir(path):
        if str(file.name).__contains__('bnd'):
            try:
                bnd = BND3(file)
            except Exception as e:
                print(e)
