import os

from ds_types.bnd3 import BND3

if __name__ == '__main__':
    path = 'bnd'
    for file in os.scandir(path):
        if str(file.name).__contains__('bnd'):

            try:
                with open(file, 'rb') as f:
                    bnd = BND3(f)

                    while bnd.has_next():
                        packed_file, data = bnd.next()
                        BND3.write(packed_file, data)

            except Exception as e:
                print(e)
