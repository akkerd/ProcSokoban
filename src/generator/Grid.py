import copy
import random
from IO.Utils import print_grid
from Generator.Module import Module
from Generator.Utils import Utils


class Grid:

    def __init__(self, size):
        self.Size = size
        self.Module_Grid = [[None for i in range(size[0])] for j in range(size[1])]

    def reset_grid(self, key_templates):
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                self.Module_Grid[i][j] = Module(possibilities=copy.copy(key_templates), position=[i,j])

        # Set modules' neighbours
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                try:
                    # North
                    if i-1 > -1:
                        self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i-1][j], 0)
                except Exception:
                    pass
                try:
                    # East
                    if j+1 < self.Size[1]:
                        self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i][j+1], 1)
                except Exception:
                    pass
                try:
                    # South
                    if i+1 < self.Size[0]:
                        self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i+1][j], 2)
                except Exception:
                    pass
                try:
                    # West
                    if j-1 > -1:
                        self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i][j-1], 3)
                except Exception:
                    pass

    def fake_solution(self, key_templates):
        count = 0
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                self.Module_Grid[i][j] = Module(possibilities=copy.copy([key_templates[count]]), position=[i,j])
                self.Module_Grid[i][j].collapsed = True
                count += 1
        self.Module_Grid[1][1].collapsed = False
        # Set modules' neighbours
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                try:
                    # North
                    self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i - 1][j], 0)
                except Exception:
                    pass
                try:
                    # East
                    self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i][j + 1], 1)
                except Exception:
                    pass
                try:
                    # South
                    self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i + 1][j], 2)
                except Exception:
                    pass
                try:
                    # West
                    self.Module_Grid[i][j].set_neighbour(self.Module_Grid[i][j - 1], 3)
                except Exception:
                    pass

    def pick_random_module(self):
        chosenI = random.randrange(0, self.Size[0])
        chosenJ = random.randrange(0, self.Size[1])
        return self.Module_Grid[chosenI][chosenJ]

    def print(self):
        level = self.grid_to_level()
        print_grid(level)

    def grid_to_level(self, ensureOuterWalls=False):
        # Get module_grid into level_grid
        level_grid = [[None for i in range(self.Size[0])] for j in range(self.Size[1])]
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                try:
                    if self.Module_Grid[i][j].collapsed:
                        level_grid[i][j] = \
                            self.Module_Grid[i][j].PossibilitySpace[0].get_level()
                    else:
                        level_grid[i][j] = self.create_empty_template(self.Module_Grid[i][j].PossibilitySpace[0].get_rows(), self.Module_Grid[i][j].PossibilitySpace[0].get_cols())
                except IndexError as e:
                    print("IndexError:", e)
        
        level = {}
        lastRow = 0
        for templateRowCount, templateRow in enumerate(level_grid):
            for templateCount, template in enumerate(templateRow):
                for rowCount, row in enumerate(template):
                    if rowCount + lastRow in level:
                        level[rowCount + lastRow] = \
                            level[rowCount + lastRow] + row
                    else:
                        level[rowCount + lastRow] = row
            lastRow += len(template)

        if ensureOuterWalls:
            Utils.ensureOuterWalls(level)

        return level

    def is_collapsed(self, row, col):
        return self.Module_Grid[row][col].collapsed

    def is_contradiction(self, row, col):
        return self.Module_Grid[row][col].contradiction

    def create_empty_template(self, rows, cols):
        try:
            if rows < 2 or cols < 2:
                raise Exception
        except Exception as e:
            print(e)
        output = [['?'] * cols] * rows
        # print("Some mocking template: ", output)
        return output