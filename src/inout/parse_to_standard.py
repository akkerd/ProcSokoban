import sys
import os

def parse_to_standard(level_name):
    path = os.path.dirname(os.path.abspath(__file__))[:-5]
    level_path = path + "templates\\" + level_name
    lines = open(level_path, "r").read().splitlines()
    print(lines)

    level = []
    # Parse in standard format
    for row in lines:
        tmp_row = list(row)
        level.append(tmp_row)
        for i, char in enumerate(row):
            if char == "+":
                tmp_row[i] = "#"
            elif char == "X":
                tmp_row[i] = " "
            elif char in "ABCDEFGHIJKLMNOPQRSTUVWYZ":
                tmp_row[i] = "$"
            elif char in "abcdefghijklmnopqrstuvwyz":
                tmp_row[i] = "."
            elif char in "0123456789":
                tmp_row[i] = "@"
            elif char == "/":
                tmp_row[i] = "#"

    # Print
    print("Level name: ", level_name[:-3])
    WriteStream = open(path + "templates\\standard_" + level_name[:-3] + ".txt", "w+")
    for row in level:
        line = "".join(row)
        print(line)
        WriteStream.write(line + "\n")
    WriteStream.close()

if __name__ == "__main__":
    a = str(sys.argv[1])
    parse_to_standard(a)