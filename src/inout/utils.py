import glob
import os
import errno
import sys
import os

def print_grid(grid):
    for row in grid.values():
        print("Row by row: ", "".join(row))

def print_and_write_grid(grid, file_name):
    path_to_script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    WriteStream = open(path_to_script_dir + "\levels\\" + file_name + ".lvl", "w+")
    for row in grid.values():
        line = "".join(row)
        print("Row by row: ", line)
        WriteStream.write(line+"\n")
    WriteStream.close()

def read_templates():
    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:-5] + "Templates\*"
    print(path)
    key_template_list = []
    wildcard_list = []
    files = glob.glob(path)
    longest_line = 0
    for name in files:
        if name[-3:] == ".kt" or name[-3:] == ".wc":
            try:
                lines = open(name, "r").read().splitlines()
                for i, line in enumerate(lines):
                    # Add spaces if possible (helps in case the level was
                    # designed forgetting about spaces as visible chars)
                    if len(line) > longest_line:
                        longest_line = len(line)
                    elif len(line) < longest_line:
                        for i in range(0, longest_line-len(line)):
                            line += " "
                    lines[i] = list(line)
                temp = {
                    'name': name,
                    'lines': lines
                }
                if name[-3:] == ".kt":
                    key_template_list.append(temp)
                elif name[-3:] == ".wc":
                    wildcard_list.append(temp)            
            except IOError as exc:
                print(exc)
                if exc.errno != errno.EISDIR:
                    raise
    return key_template_list, wildcard_list
