from level_parser.border import Border


class Template:    

    def __init__(self, name, lines, index=(0, 0), complementary=None):
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
        # self.RealSize = (max(x[0] for x in complementary) * 5, max(x[1] for x in complementary) * 5)
        self.Index = index
        self.Complementary = complementary
        self.ConnectionCount = 0
        # self.Walls = [[False for _ in range(self.Ncols)] for _ in range(self.Nrows)]

        # UpBorder
        self.borders[0] = Border(line=lines[0])
        # DownBorder
        self.borders[2] = Border(line=lines[self.Nrows - 1])
        leftline = []
        rightline = []

        # Read template line by line
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if col is 0:
                    leftline.append(char)
                elif col is self.Ncols - 1:
                    rightline.append(char)

        # RightBorder
        self.borders[1] = Border(line=rightline)
        # LeftBorder
        self.borders[3] = Border(line=leftline)

        for border in self.borders:
            if border.is_connection():
                self.ConnectionCount += 1

    def needs_complementary(self):
        return self.Complementary is not None

    def set_complementary_list(self, comp_list):
        temp_comp_list = {}
        for comp in comp_list:
            temp_comp_list[comp.Index] = comp
        self.Complementary = temp_comp_list

    def is_connection_at(self, dir):
        return self.borders[dir].IsConnection