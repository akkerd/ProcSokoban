import sys
from src.LevelParser.Border import Border


class Template:    

    def __init__(self, level_file, debug=False):

        self.Debug = debug
        self.Ncols = 0
        self.Nrows = 0
        # borders = [UP, RIGHT, DOWN, LEFT]
        self.borders = {}
        self.PossibleBoxes = {}
        self.PossibleGoals = {}
        self.Walls = {}
        self.IsGoalsTemplate = False
        self.OriginalLevel = None
        self.Name = level_file

        try:
            # Read template file
            lines = open(level_file, "r").read().splitlines()
            self.OriginalLevel = lines
            tempwalls = []
            boxeslist = []
            goalslist = []
            leftline = []
            rightline = []
            tempboxes = {}
            tempgoals = {}
            self.Nrows = len(lines)
            self.Ncols = len(max(lines, key=len))

            # if lines[0] == "goals":
            #     self.IsGoalsTemplate = True
            # UpBorder
            self.borders[0] = Border(line=lines[0])
            # DownBorder
            self.borders[2] = Border(line=lines[self.Nrows-1])

            # Read template line by line
            for row, line in enumerate(lines):
                for col, char in enumerate(line):
                    if col is 0:
                        leftline.append(char)
                    elif col is self.Ncols-1:
                        rightline.append(char)
                    # Parse walls, boxes and goals into matrixes and lists 
                    if char == '#':
                        tempwalls.append((row, col))
                    elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        tempboxes[(row, col)] = char
                        boxeslist.append((row, col))
                    elif char in "abcdefghijklmnopqrstuvwxyz":
                        tempgoals[(row, col)] = char
                        goalslist.append((row, col))
            # RightBorder
            self.borders[1] = Border(line=rightline)
            # LeftBorder
            self.borders[3] = Border(line=leftline)

            self.PossibleBoxes, self.PossibleGoals = boxeslist, goalslist
            self.Walls = [[False for _ in range(self.Ncols)] for _ in range(self.Nrows)]
            for (i, j) in tempwalls:
                self.Walls[i][j] = True

        except Exception as ex:
            print('Error parsing level: {}.'.format(repr(ex)), file=sys.stderr, flush=True)
            if debug:
                raise ex
            sys.exit(1)

