import glob
import os
import errno

def print_grid(grid):
    for row in grid.values():
        print("Row by row: ", row)

def print_and_write_grid(grid, file_path):
    WriteStream = open(file_path, "w+")
    for row in grid.values():
        print("Row by row: ", row)
        WriteStream.write(row+"\n")
    WriteStream.close()


def read_templates():
    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:-2] + "Templates\*"
    print(path)
    key_template_list = []
    wildcard_list = []
    files = glob.glob(path)
    for name in files:
        try:
            temp = {"name":name, "lines":open(name, "r").read().splitlines()}
            if name[-2:] == "kt":
                key_template_list.append(temp)
            elif name[-2:] == "wc":
                wildcard_list.append(temp)            
        except IOError as exc:
            print(exc)
            if exc.errno != errno.EISDIR:
                raise
    return key_template_list, wildcard_list
