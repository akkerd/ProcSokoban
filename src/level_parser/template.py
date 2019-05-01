from level_parser.border import Border


class Template:    

    def __init__(self, name, lines):
        """ 
            Return a template object, containing the original level
            as a list of strings and borders as Border objects, among others.
            name : string
            lines : [string]
        """
        # Empty variables
        self.borders = [0, 0, 0, 0]  # [UP, RIGHT, DOWN, LEFT]

        # Read template file
        self.Name = name
        self.OriginalLevel = lines
        self.Nrows = len(lines)
        self.Ncols = len(max(lines, key=len))
        # self.Walls = [[False for _ in range(self.Ncols)] for _ in range(self.Nrows)]

        # UpBorder
        self.borders[0] = Border(line=lines[0])
        # DownBorder
        self.borders[2] = Border(line=lines[self.Nrows-1])
        leftline = []
        rightline = []

        # Read template line by line
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if col is 0:
                    leftline.append(char)
                elif col is self.Ncols-1:
                    rightline.append(char)

                #### DON'T PARSE WALLS, BOXES OR GOALS IF NOT NEEDED YET ####
                # Parse walls, boxes and goals into matrixes and lists 
                # if char == '#':
                #     self.Walls[row][col] = True
                # elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                #     self.PossibleBoxes[(row, col)] = char
                # elif char in "abcdefghijklmnopqrstuvwxyz":
                #     self.PossibleGoals[(row, col)] = char
        # RightBorder
        self.borders[1] = Border(line=rightline)
        # LeftBorder
        self.borders[3] = Border(line=leftline)

