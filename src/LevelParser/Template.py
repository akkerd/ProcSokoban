import sys
from src.LevelParser.Border import Border


class Template:    

    def __init__(self, level_file, debug=False):

        self.Debug = debug
        self.Ncols = 0
        self.Nrows = 0
        self.TopBorder = None
        self.BottomBorder = None
        self.LeftBorder = None
        self.RightBorder = None
        self.PossibleBoxes = {}
        self.PossibleGoals = {}
        self.Walls = {}
        self.IsGoalsTemplate = False
        self.OriginalLevel = None

        try:
            # Read template file
            lines = open(level_file, "r").read().splitlines()
            self.OriginalLevel = lines
            # Read template line by line
            tempwalls = []

            tempboxes = {}
            boxeslist = []

            tempgoals = {}
            goalslist = []

            self.Nrows = len(lines)
            self.Ncols = len(max(lines, key=len))
            self.TopBorder = Border(lines[0])
            if lines[0] == "goals":
                self.IsGoalsTemplate = True
            self.BottomBorder = Border(lines[self.Nrows-1])
            
            leftline = []
            rightline = []
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

            self.LeftBorder = Border(leftline)
            self.RightBorder = Border(rightline)

            self.PossibleBoxes, self.PossibleGoals = boxeslist, goalslist
            self.Walls = [[False for _ in range(self.Ncols)] for _ in range(self.Nrows)]
            for (i, j) in tempwalls:
                self.Walls[i][j] = True
            x = 1 # Finished
            # self.initial_state = State(size=(nrows, ncols))
            # self.initial_state.agent_row = temp_agent_row
            # self.initial_state.agent_col = temp_agent_col
            # self.initial_state.walls = [row[:ncols] for row in tempwalls[:nrows]]
            # self.initial_state.boxes = [row[:ncols] for row in tempboxes[:nrows]]
            # self.initial_state.goals = [row[:ncols] for row in tempgoals[:nrows]]
            # self.initial_state.goals_list = goals_list
            # self.initial_state.goalletter = goalletter

        except Exception as ex:
            print('Error parsing level: {}.'.format(repr(ex)), file=sys.stderr, flush=True)
            if debug:
                raise ex
            sys.exit(1)