import glob
import os, os.path
import errno
import sys
import math
import copy

class IOUtils:
    @staticmethod
    def print_grid(grid):
        for row in grid.values():
            print("Row by row: ", "".join(row))

    @staticmethod
    def print_and_write_grid(grid, file_name):
        path_to_script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        # Print AI-MAS formatted level
        WriteStream = open(path_to_script_dir + "\levels\\" + file_name + ".lvl", "w+")
        for row in grid.values():
            for i, char in enumerate(row):
                if char == "?":
                    row[i] = " "
            line = "".join(row)
            print("Row by row: ", line)
            WriteStream.write(line + "\n")
        WriteStream.close()

        for row in grid.values():
            for i, char in enumerate(row):
                if char == "+":
                    row[i] = "#"
                elif char == "X":
                    row[i] = " "
                elif char in "ABCDEFGHIJKLMNOPQRSTUVWYZ":
                    row[i] = "$"
                elif char in "abcdefghijklmnopqrstuvwyz":
                    row[i] = "."
                elif char in "0123456789":
                    row[i] = "@"

        # Print in standard format
        WriteStream = open(path_to_script_dir + "\levels\\" + file_name + ".txt", "w+")
        for row in grid.values():
            line = "".join(row)
            WriteStream.write(line + "\n")
        WriteStream.close()        

    
    @staticmethod
    def read_templates():
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-5] + "templates\*"
        print(path)
        prototemplates = {'kt': [], 'wc': [], 'gt': []}
        files = glob.glob(path)
        longest_line = 0
        # Clean validity check folder
        IOUtils.clean_validity_check()
        for name in files:
            # print("File name to open: ", name)
            extension = name[-2:]
            if extension in prototemplates.keys():
                try:
                    lines = open(name, "r").read().splitlines()
                except IOError as exc:
                    print(exc)
                    if exc.errno != errno.EISDIR:
                        raise
                    
                # Clean up extra spaces at the right
                for i, line in enumerate(lines):
                    if not all(elem == ' ' for elem in line):
                        lines[i] = line.rstrip()

                # Find longest line in template
                longest_line = len(max(lines, key=lambda coll: len(coll)))

                # Adapt templates to have fixed 5x5 size, or multiples of that (5x10, 15x10...)
                width = math.ceil(longest_line / 5) * 5
                height = math.ceil(len(lines) / 5) * 5
                # print("Template width: " + str(width) + " and height: " + str(height))
                
                if height % 5 != 0 or width % 5 != 0:
                    # Check that sizes are multiple of 5
                    print("This template does not have the right size format.")
                    raise Exception  
                
                # Adapt width
                for i, line in enumerate(tuple(lines)):
                    # Add spaces if neccesary to maintain rectangular modules 
                    if width - len(line) > 0:
                        for j in range(0, width - len(line)):
                            line += " "
                    elif width - len(line) < 0:
                        if all(elem == ' ' for elem in line):
                            line = " " * width
                        else:
                            raise Exception
                    lines[i] = list(line)

                # Adapt height
                for k in range(0, height - len(lines)):
                    new_line = [' '] * width
                    lines.append(new_line)

                # Save templates for validity check
                t_name = name.split("\\")[-1]
                if extension != "kt":
                    IOUtils.save_validity_check(lines, t_name)

                # Create prototemplate structure
                if height > 5 or width > 5:
                    prototemplates_to_keep = []
                    # Split templates if size is bigger than 5x5
                    for i in range(0, int(height / 5)):
                        for j in range(0, int(width / 5)):
                            temp = {
                                'name': t_name,
                                'lines': [lines[(i * 5) + x][j * 5:(j + 1) * 5] for x in range(0, 5)],
                                'index': (i, j)
                            }
                            prototemplates_to_keep.append(temp)
                    for temp in prototemplates_to_keep:
                        # Add references to complementary modules
                        temp['complementary'] = [x['index'] for x in prototemplates_to_keep if temp != x]
                        prototemplates[extension].append(temp)
                else:
                    temp = {
                        'name': t_name,
                        'lines': lines
                    }
                    prototemplates[extension].append(temp)

        return prototemplates

    @staticmethod
    def clean_validity_check():
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-5] + "templates\\validity_check\*"
        files = glob.glob(path)
        # Delete previous
        for previous_file in files:
            os.unlink(previous_file)
    
    @staticmethod
    def save_validity_check(grid, name):
        exits = []
        print(grid)
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == "/":
                    exits.append((i, j))
        c = 0
        for ex in exits:
            temp_grid = copy.deepcopy(grid)
            temp_grid[ex[0]][ex[1]] = "0"
            for ex2 in exits:
                if ex2 != ex:
                    temp_grid[ex2[0]][ex2[1]] = "+"
            c += 1
            IOUtils.write_validitycheck_standard(temp_grid, name.replace(".", "") + "_" + str(c) + ".txt")

    @staticmethod
    def parse_to_standard(grid):
        temp_grid = copy.deepcopy(grid)
        for row in temp_grid:
            for i, char in enumerate(row):
                if char == "+":
                    row[i] = "#"
                elif char == "X":
                    row[i] = " "
                elif char in "ABCDEFGHIJKLMNOPQRSTUVWYZ":
                    row[i] = "$"
                elif char in "abcdefghijklmnopqrstuvwyz":
                    row[i] = "."
                elif char in "0123456789":
                    row[i] = "@"
        return temp_grid

    @staticmethod
    def write_validitycheck_standard(level, file_name):
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-5] + "templates\\validity_check\\"
        if not os.path.exists(path):
            os.mkdir(path)
        # Print in standard format
        grid = IOUtils.parse_to_standard(level)
        # print(path + file_name)
        # print(grid)
        heigth = len(grid)
        width = len(grid[0])
        wall_row = ("#"*(width+2))
        WriteStream = open(path + file_name, "w+")
        WriteStream.write(wall_row + "\n")
        for row in grid:
            line = "".join(row)
            WriteStream.write("#" + line + "#" + "\n")
        WriteStream.write(wall_row + "\n")
        WriteStream.close()