import random 

class Utils:

    @staticmethod
    def rotate(level):
        # Transpose
        rotated = list(map(list,zip(*level)))
        # Reverse
        for row in rotated:
            row.reverse()
        return rotated          
    
    @staticmethod
    def ensureOuterWalls(grid):
        expanded_level = {}
        expanded_level[0] = ["+"] * (len(grid) + 2)
        for i in range(0, len(grid)):
            expanded_level[i + 1] = ["+"] + grid[i] + ["+"]
        expanded_level[len(grid) + 1] = ["+"] * (len(grid) + 2)
        return expanded_level

    @staticmethod
    def ensure_one_player(grid):
        raise NotImplementedError

    @staticmethod
    def fit_box_goals(level):
        # Track final level variables
        box_count = 0
        goals_tracker = []
        goals_count = 0
        for i, row in level.items():
            for j, char in enumerate(row):
                if char in "ABCDEFGHIJKLMNOPQRSTUVWYZ":
                    box_count += 1
                elif char in "abcdefghijklmnopqrstuvwyz":
                    goals_tracker.append((i, j))
                    goals_count += 1
                elif char == "/":
                    level[i][j] = " "

        # Remove extra goals
        for i in range(0, goals_count - box_count):
            pos = goals_tracker.pop(random.randrange(0, len(goals_tracker)))
            level[pos[0]][pos[1]] = " "
