class Level:
    def __init__(self, level):

        # Empty variables
        self.PossibleBoxes = {}
        self.PossibleGoals = {}

        self.OriginalLevel = level
        self.Nrows = len(level)
        self.Ncols = len(max(level, key=len))
        self.Walls = [[' ' for _ in range(self.Ncols)] for _ in range(self.Nrows)]

        # Read template line by line
        for row, line in enumerate(level):
            for col, char in enumerate(line):
                # Parse walls, boxes and goals into matrixes and lists 
                if char == '#':
                    self.Walls[row][col] = '#'
                if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    self.PossibleBoxes[(row, col)] = char
                elif char in "abcdefghijklmnopqrstuvwxyz":
                    self.PossibleGoals[(row, col)] = char

        # Finished
        x = 1

    def __repr__(self):
        return "Level()"

    def __str__(self):
        level = ""
        for line in self.OriginalLevel:
            level += line + "\n"
        return level