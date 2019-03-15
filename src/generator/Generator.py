import copy
import random
from Generator.Module import Module
from Generator.TemplateContainer import TemplateContainer
from IO.Utils import print_grid


class Generator:
    key_templates = []
    wildcards = []

    def __init__(self, key_templates, wildcards=[], seed=None):

        # Add every template to a container
        for template in key_templates:
            Generator.key_templates.append(TemplateContainer(template))

        # Add every template to a container
        for wildcard in wildcards:
            Generator.wildcards.append(TemplateContainer(wildcard))

        random.seed(seed)

    def get_level(self, size=[2, 2], surroundWalls=False):
        # Generate the grid
        templategrid = [[None for i in range(size[0])] for j in range(size[1])]
        # print("Templates: ", Generator.key_templates)
        # print("Wildcards: ", Generator.wildcards)

        ################### Wave Function Collapse ###################
        # NOTE: Fill grid with Modules
        self.reset_grid(templategrid, size)
        # self.fake_solution(templategrid, size)

        # NOTE: Iterate updating neighbours
        finished = False
        IterationCount = 0
        while not finished:
            # Pick one of the modules randomly and collapse it
            chosenI = random.randrange(0, size[0])
            chosenJ = random.randrange(0, size[1])
            chosen_one = templategrid[chosenI][chosenJ]
            if chosen_one.collapsed:
                continue
            else:
                # print("Selected to collapse: ", chosen_one)
                chosen_one.collapse_random()
                chosen_one.update_neighbours()

            # Check whether to finish (all templates have collapsed)
            # or stop and start over again (contradiction found)
            all_collapsed = True
            for i in range(0, size[0]):
                for j in range(0, size[1]):
                    if not templategrid[i][j].collapsed:
                        all_collapsed = False
                    if templategrid[i][j].contradiction:
                        # Contradiction found
                        print("Reseting grid...")
                        self.reset_grid(templategrid, size)
                        break
            if all_collapsed:
                finished = True
            else: 
                IterationCount += 1
                print("Iteration #", IterationCount, ": ")
                print_grid(self.create_final_grid(templategrid, size))

        # Create final level
        outGrid = self.create_final_grid(templategrid, size)

        if surroundWalls:
            self.ensureOuterWalls(outGrid)

        return outGrid

    def ensureOuterWalls(self, grid):
        for i in range(0, len(grid)):
            print("Row", i)
            if i is 0 or i is len(grid)-1:
                    grid[i] = "#" * (len(grid[i])-1)
            else:
                grid[i] = "#" + grid[i][1:len(grid[i])-2] + "#"

    def reset_grid(self, grid, size):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                grid[i][j] = Module(possibilities=copy.copy(Generator.key_templates), position=[i,j])

        # Set modules' neighbours
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                try:
                    # North
                    if i-1 > -1:
                        grid[i][j].set_neighbour(grid[i-1][j], 0)
                except Exception:
                    pass
                try:
                    # East
                    if j+1 < size[1]:
                        grid[i][j].set_neighbour(grid[i][j+1], 1)
                except Exception:
                    pass
                try:
                    # South
                    if i+1 < size[0]:
                        grid[i][j].set_neighbour(grid[i+1][j], 2)
                except Exception:
                    pass
                try:
                    # West
                    if j-1 > -1:
                        grid[i][j].set_neighbour(grid[i][j-1], 3)
                except Exception:
                    pass

    def fake_solution(self, grid, size):
        count = 0
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                grid[i][j] = Module(possibilities=copy.copy([Generator.key_templates[count]]), position=[i,j])
                grid[i][j].collapsed = True
                count += 1
        grid[1][1].collapsed = False
        # Set modules' neighbours
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                try:
                    # North
                    grid[i][j].set_neighbour(grid[i - 1][j], 0)
                except Exception:
                    pass
                try:
                    # East
                    grid[i][j].set_neighbour(grid[i][j + 1], 1)
                except Exception:
                    pass
                try:
                    # South
                    grid[i][j].set_neighbour(grid[i + 1][j], 2)
                except Exception:
                    pass
                try:
                    # West
                    grid[i][j].set_neighbour(grid[i][j - 1], 3)
                except Exception:
                    pass

    def create_final_grid(self, templategrid, size):
        outGrid = {}
        finalgrid = [[None for i in range(size[0])] for j in range(size[1])]
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                try:
                    if templategrid[i][j].collapsed:
                        finalgrid[i][j] = \
                            templategrid[i][j].PossibilitySpace[0].template.OriginalLevel
                    else:
                        finalgrid[i][j] = self.mock_template(templategrid[i][j].PossibilitySpace[0].template.Ncols, templategrid[i][j].PossibilitySpace[0].template.Nrows)
                except IndexError as e:
                    print("IndexError:", e)

        lastRow = 0
        for templateRowCount, templateRow in enumerate(finalgrid):
            for templateCount, template in enumerate(templateRow):
                for rowCount, row in enumerate(template):
                    if rowCount + lastRow in outGrid:
                        outGrid[rowCount + lastRow] = \
                            outGrid[rowCount + lastRow] + row
                    else:
                        outGrid[rowCount + lastRow] = row
            lastRow += len(template)
        return outGrid

    def mock_template(self, cols, rows):
        try:
            if cols < 2 or rows < 2:
                raise Exception
        except Exception as e:
            print(e)
        output = [' ' * cols] * rows
        # print("Some mocking template: ", output)
        return output



