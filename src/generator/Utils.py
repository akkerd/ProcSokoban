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
        for i in range(0, len(grid)):
            if i is 0 or i is len(grid)-1:
                    grid[i] = ["+"] * (len(grid[i])-1)
            else:
                grid[i] = ["+"] + grid[i][1:len(grid[i])-2] + ["+"]
