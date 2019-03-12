from LevelParser.Border import Border


class Template:    

    def __init__(self, name, lines, debug=False):

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
        self.Name = name

        # Read template file
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

