class Room:    

    def __init__(self, level, position):
        """ 
            Return a Room object, containing the information about
            one single room in the puzzle. The information includes
            possible goal positions
        """
        # Empty variables
        self.PossibleBoxes = {}
        self.PossibleGoals = {}
        self.IsGoalsTemplate = False

        self.Position = position
        # self.OriginalLevel = level
        self.Nrows = len(level)
        self.Ncols = len(max(level, key=len))
        # self.Walls = [[False for _ in range(self.Ncols)] for _ in range(self.Nrows)]

        # Read template line by line
        for row, line in enumerate(level):
            for col, char in enumerate(line):
                # Parse walls, boxes and goals into matrixes and lists 
                if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    self.PossibleBoxes[(row, col)] = char
                elif char in "abcdefghijklmnopqrstuvwxyz":
                    self.PossibleGoals[(row, col)] = char