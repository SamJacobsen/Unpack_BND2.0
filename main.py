import os, sys

from ds_types.bnd3 import BND3
from ds_types.dcx import DCX

extensions = {'bnd': BND3, 'dcx': DCX, 'tpf': 'tpf parser'}

if __name__ == '__main__':

    for file in sys.argv[1:]:
        extension = os.path.basename(file).split('.')
        extension = extension[len(extension) - 1]
        print(extension)

        parser = [par for ext, par in extensions.items() if ext in extension]
        if parser:
            parser = parser[0]
            print(parser)
            try:
                with open(file, 'rb') as f:

                    ds_file = parser(f)

                    while ds_file.has_next():
                        file_path, data = ds_file.next()
                        ds_file.write(file_path, data)
            except FileNotFoundError as e:
                print(e)
