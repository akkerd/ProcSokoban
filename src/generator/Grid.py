import copy
import random
from generator.module import Module
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

    def reset_grid(self, templates, prune_edges=False):
        '''
            templates: list of TemplateContainers [Object, object]
        '''
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                possibility_space = copy.copy(templates)
                if prune_edges:
                    self.prune_templates(possibility_space, i, j)
                self.Module_Grid[i][j] = Module(possibilities=possibility_space, position=[i, j])

        # Set modules' neighbours
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                try:
                    # North
                    if i - 1 > -1:
                        self.get_module(i, j).set_neighbour(self.get_module(i - 1, j), 0)
                except Exception:
                    pass
                try:
                    # East
                    if j + 1 < self.Size[1]:
                        self.get_module(i, j).set_neighbour(self.get_module(i, j+1), 1)
                except Exception:
                    pass
                try:
                    # South
                    if i + 1 < self.Size[0]:
                        self.get_module(i, j).set_neighbour(self.get_module(i + 1, j), 2)
                except Exception:
                    pass
                try:
                    # West
                    if j - 1 > -1:
                        self.get_module(i, j).set_neighbour(self.get_module(i, j - 1), 3)
                except Exception:
                    pass

    def get_module(self, i, j):
        return self.Module_Grid[i][j]

    def prune_templates(self, templates, i, j):
        ''' 
        Prune template list of the ones that have connections 
        where the grid ends
        '''
        for template in tuple(templates):
            if template in templates:
                if i is 0 and template.get_border(3).MinimumConnection is not 0:
                    templates.remove(template)
                elif i is self.Size[0] - 1 and template.get_border(1).MinimumConnection is not 0:
                    templates.remove(template)

                if j is 0 and template.get_border(0).MinimumConnection is not 0:
                    templates.remove(template)
                elif j is self.Size[1] - 1 and template.get_border(2).MinimumConnection is not 0:
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

    def pick_random(self):
        chosenI = random.randrange(0, self.Size[0])
        chosenJ = random.randrange(0, self.Size[1])
        return self.Module_Grid[chosenI][chosenJ]

    def pick_next(self):
        open_list = []

        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                if self.get_module(i, j).is_open():
                    open_list.append(self.get_module(i, j))
        
        if len(open_list) == 0:
            raise Exception
        # Find open modules with minimum distance from goals
        distance_from_goal = [0] * len(open_list)
        for k, openm in enumerate(open_list):
            # Calculate distance from goal
            for goal in self.Goals:
                distance_from_goal[k] += abs(openm.Position[0] - goal[0]) + abs(openm.Position[1] - goal[1])
        
        min_indexes = self.locate_min_indexes(distance_from_goal)
        
        # NOTE: WIP - Normalize vector to compare it with other heuristic, like the connectivity of the module
        # distance_from_goal = norm = [float(i) / sum(distance_from_goal) for i in distance_from_goal]
        
        if len(min_indexes) != 1:
            # If some cells are at same distance, pick module \
            # with minimum entropy in its PossibilitySpace
            min_entropy = 100000
            for m in min_indexes:
                entropy = len(open_list[m].PossibilitySpace)
                if entropy < min_entropy:
                    chosen_index = m
        else:
            chosen_index = min_indexes[0]

        return open_list[chosen_index]
 
    def locate_min_indexes(self, p_list):
        min_indexes = []
        smallest = min(p_list)
        for index, element in enumerate(p_list):
                if smallest == element: # check if this element is the minimum_value
                        min_indexes.append(index) # add the index to the list if it is

        return min_indexes


    def print(self):
        level = self.get_full_level()
        print_grid(level)

    def get_level_grid(self):
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
                    if self.get_module(i, j).is_collapsed():
                        level_grid[i][j] = self.Module_Grid[i][j].PossibilitySpace[0].get_level()
                    else:
                        size_rows, size_cols = self.get_constraints((i, j))
                        if self.get_module(i, j).is_contradiction():
                            level_grid[i][j] = self.get_empty_template(size_rows, size_cols)
                        else:
                            level_grid[i][j] = self.get_temp_template(size_rows, size_cols)
                except IndexError as e:
                    print("IndexError:", e)
        return level_grid

    def get_full_level(self, ensureOuterWalls=False):
        """ 
        This function takes a grid (double dimensional list) of
        Templates and turns it into a grid containing the
        characters that make the final level.

        NOTE: Inputing a grid of something else that are not
        Templates will make the function fail.
        """
        level_grid = self.get_level_grid()
        level = {}
        column_size = {}
        for i in range(0, len(level_grid[0])): 
            column_size[i] = 0
        lastRow = 0

        for level_row_count, row_of_levels in enumerate(level_grid):            
            for level_column_count, original_level in enumerate(row_of_levels):
                for row_count, row in enumerate(original_level):
                    if level.get(row_count + column_size[level_column_count]):
                        level[row_count + column_size[level_column_count]] += row
                    else:
                        level[row_count + column_size[level_column_count]] = row

                # Update lenght of column
                column_size[level_column_count] += len(level)

        if ensureOuterWalls:
            Utils.ensureOuterWalls(level)

        return level

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
        output = [['X'] * cols] * rows
        # print("Some mocking template: ", output)
        return output

    def set_start(self, start, pos: tuple):
        module = self.get_module(pos[0], pos[1])
        module.collapse(start)
        self.Starts.append(pos)
        return module
    
    def set_goal(self, goal, pos: tuple):
        module = self.get_module(pos[0], pos[1])
        module.collapse(goal)
        self.Goals.append(pos)
        return module

    def get_constraints(self, pos: tuple):
        sizes = [0] * 4
        for i in range(0, 4):
            while True:
                # Find neighbour that is not a contradiction
                neighbour = self.Module_Grid[pos[0]][pos[1]].neighbours.get(i)
                if neighbour:
                    if neighbour.is_contradiction():
                        # If contradiction found, try the next cell in the grid
                        if i == 0:
                            pos[0] -= 1
                        elif i == 1:
                            pos[1] += 1
                        elif i == 2:
                            pos[0] += 1
                        elif i == 3:
                            pos[1] -= 1
                    else:
                        break
                else:
                    break
                    
            if neighbour:
                if i % 2 == 0:
                    sizes[i] = max(poss.get_cols() for poss in neighbour.PossibilitySpace)
                else:
                    sizes[i] = max(poss.get_rows() for poss in neighbour.PossibilitySpace)
            else:
                sizes[i] = 5

        width = max(sizes[0], sizes[2])
        height = max(sizes[1], sizes[3])
        # if width == 1 and height == 1:
        #     print('Unclear constraint situation')
        #     raise Exception

        return width, height
