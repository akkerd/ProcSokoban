import copy
import random
from generator.module import Module, State
from generator.utils import Utils
from inout.utils import print_grid

class Grid:

    def __init__(self, size):
        self.Size = size
        self.Module_Grid = [[None for i in range(size[0])] for j in range(size[1])]
        self.Starts = []
        self.Goals = []
        self.CriticalPath = []
        self.HaveCriticalPath = False

    def reset_grid(self, key_templates, prune_edges=False):
        '''
            key_templates: list of TemplateContainers [Object, object]
        '''
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                possibility_space = copy.copy(key_templates)
                if prune_edges:
                    self.prune_templates(possibility_space, i, j)
                self.Module_Grid[i][j] = Module(possibilities=possibility_space, position=[i, j])

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

    def prune_templates(self, templates, i, j):
        ''' 
        Prune template list of the ones that have connections 
        where the grid ends
        '''
        for template in tuple(templates):
            if template in templates:
                if i is 0 and template.get_border(3).MinimumConnection is not 0:
                    templates.remove(template)
                elif i is self.Size[0]-1 and template.get_border(1).MinimumConnection is not 0:
                    templates.remove(template)

                if j is 0 and template.get_border(0).MinimumConnection is not 0:
                    templates.remove(template)
                elif j is self.Size[1]-1 and template.get_border(2).MinimumConnection is not 0:
                    templates.remove(template)
            
        return templates

    def fake_solution(self, key_templates):
        count = 0
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                self.Module_Grid[i][j] = Module(possibilities=copy.copy([key_templates[count]]), position=[i,j])
                self.Module_Grid[i][j].state = State.Collapsed
                count += 1
        self.Module_Grid[1][1].state = State.Collapsed
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
        level_grid = self.get_level_grid()
        level = self.levelgrid_to_full_level(level_grid=level_grid, ensureOuterWalls=False)
        print_grid(level)

    def get_level_grid(self, ensureOuterWalls=False):
        """ 
            This function takes a grid (double dimensional list) of
            Modules and turns it into a grid of OriginalLevels.

            (An OriginalLevel is a grid of characters that represent the
            original template, which might be rotated in the generation
            process or not).
        """
        # Get module_grid into level_grid
        level_grid = [[None for i in range(self.Size[0])] for j in range(self.Size[1])]
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                try:
                    if self.Module_Grid[i][j].state == State.Collapsed:
                        level_grid[i][j] = \
                            self.Module_Grid[i][j].PossibilitySpace[0].get_level()
                    else:
                        size_rows, size_cols = self.get_constraints((i, j))
                        if self.Module_Grid[i][j].state == State.Contradiction:
                            level_grid[i][j] = self.get_empty_template(size_rows, size_cols)
                        else:
                            level_grid[i][j] = self.get_temp_template(size_rows, size_cols)
                except IndexError as e:
                    print("IndexError:", e)
        return level_grid

    def levelgrid_to_full_level(self, level_grid, ensureOuterWalls=False):
        """ 
        This function takes a grid (double dimensional list) of
        Templates and turns it into a grid containing the
        characters that make the final level.

        NOTE: Inputing a grid of something else that are not
        Templates will make the function fail.
        """
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
        return self.Module_Grid[row][col].state == State.Collapsed

    def is_contradiction(self, row, col):
        return self.Module_Grid[row][col].state == State.Contradiction

    def get_temp_template(self, rows, cols):
        try:
            if rows < 2 or cols < 2:
                raise Exception
        except Exception as e:
            print(e)
        output = [['?'] * cols] * rows
        # print("Some mocking template: ", output)
        return output

    def get_empty_template(self, rows, cols):
        try:
            if rows < 2 or cols < 2:
                raise Exception
        except Exception as e:
            print(e)
        output = [[' '] * cols] * rows
        # print("Some mocking template: ", output)
        return output


    def set_start(self, start, pos: tuple):
        self.Module_Grid[pos[0]][pos[1]].PossibilitySpace = [start]
        self.Module_Grid[pos[0]][pos[1]].state = State.Collapsed
        self.Starts.append(pos)
    
    def set_goal(self, goal, pos: tuple):
        self.Module_Grid[pos[0]][pos[1]].PossibilitySpace = [goal]
        self.Module_Grid[pos[0]][pos[1]].state = State.Collapsed
        self.Goals.append(pos)

    def get_constraints(self, pos: tuple):
        sizes = [0] * 4
        for i in range(0, 4):
            j = i
            while True:
                # Find neighbour that is not a contradiction
                neighbour = self.Module_Grid[pos[0]][pos[1]].neighbours.get(j)
                if neighbour:
                    if neighbour.state == State.Contradiction:
                        j += 1
                    else:
                        break
                else:
                    break
            if neighbour:
                sizes[i] = max(poss.get_border((i + 2) % 4).BorderSize for poss in neighbour.PossibilitySpace)
            else:
                sizes[i] = 0
        width = max(sizes[0], sizes[2])
        height = max(sizes[1], sizes[3])

        return width, height
            