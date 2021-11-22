import os, sys

from ds_types.bnd3 import BND3

extensions = {'bnd': BND3, 'dcx': 'dcx parser', 'tpf': 'tpf parser'}

if __name__ == '__main__':

    for file in sys.argv[1:]:
        extension = os.path.basename(file).split('.')[1]
        print(extension)

        parser = [par for ext, par in extensions.items() if ext in extension][0]
        if parser:
            print(parser)
            try:
                with open(file, 'rb') as f:
                    binary_file = parser(f)

                    while binary_file.has_next():
                        packed_file, data = binary_file.next()
                        BND3.write(packed_file, data)
            except FileNotFoundError as e:
                print(e)
