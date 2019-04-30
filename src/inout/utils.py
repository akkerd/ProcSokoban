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

def read_templates(extension: str):
    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:-5] + "templates\*"
    print(path)
    template_list = []
    files = glob.glob(path)
    longest_line = 0
    for name in files:
        if name[-3:] == extension:
            try:
                lines = open(name, "r").read().splitlines()
                longest_line = len(max(lines, key=lambda coll: len(coll.rstrip())))
                for i, line in enumerate(tuple(lines)):
                    # Add spaces if neccesary to mainatin rectangular modules 
                    if len(line) < longest_line:
                        for j in range(0, longest_line-len(line)):
                            line += " "
                    lines[i] = list(line)
                    print(lines[i])
                temp = {
                    'name': name.split("\\")[-1],
                    'lines': lines
                }
                template_list.append(temp)       
            except IOError as exc:
                print(exc)
                if exc.errno != errno.EISDIR:
                    raise
    return template_list
