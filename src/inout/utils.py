import glob
import os
import errno
import sys
import math

class IOUtils:
    def print_grid(grid):
        for row in grid.values():
            print("Row by row: ", "".join(row))

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

        # Print in standard level
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
        WriteStream = open(path_to_script_dir + "\levels\\" + file_name + ".txt", "w+")
        for row in grid.values():
            line = "".join(row)
            WriteStream.write(line + "\n")
        WriteStream.close()

    def read_templates(extension: str):
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-5] + "templates\*"
        print(path)
        template_list = []
        files = glob.glob(path)
        longest_line = 0
        for name in files:
            if name[-3:] == ".".join(extension):
                try:
                    lines = open(name, "r").read().splitlines()
                    
                    # Find longest line in template
                    longest_line = len(max(lines, key=lambda coll: len(coll.rstrip())))
                    
                    # Adapt templates to have fixed 5x5 size, or multiples of that (5x10, 15x10...)
                    width = math.ceil(longest_line / 5) * 5
                    height = math.ceil(len(lines) / 5) * 5
                    
                    # Adapt width
                    for i, line in enumerate(tuple(lines)):
                        # Add spaces if neccesary to mainatin rectangular modules 
                        if width - len(line) != 0:
                            for j in range(0, width - len(line)):
                                line += " "
                        lines[i] = list(line)

                    # Adapt height
                    for k in range(0, height - len(lines)):
                        new_line = [' '] * width
                        lines.append(new_line)

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

    def read_templates():
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-5] + "templates\*"
        print(path)
        prototemplates = {'kt': [], 'wc': [], 'gt': []}
        files = glob.glob(path)
        longest_line = 0
        for name in files:
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

                # Create prototemplate structure
                t_name = name.split("\\")[-1]
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
