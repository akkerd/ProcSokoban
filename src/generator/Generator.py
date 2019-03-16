import random
from Generator.TemplateContainer import TemplateContainer
from IO.Utils import print_grid
from Generator.Grid import Grid


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

    def get_level(self, size=[2, 2], ensureOuterWalls=False):
        # Generate the grid
        templategrid = Grid(size=size)

        # Wave Function Collapse
        ## NOTE: Fill grid with Modules
        templategrid.reset_grid(Generator.key_templates)
        # self.fake_solution(templategrid, size)

        ## NOTE: Iterate updating neighbours
        finished = False
        IterationCount = 0 
        while not finished:
            chosen_one = templategrid.pick_random_module()
            if chosen_one.collapsed:
                continue
            else:
                chosen_one.collapse_random()
                chosen_one.update_neighbours()

            # Check the all templates have collapsed or start all over again
            all_collapsed = True
            for i in range(0, size[0]):
                for j in range(0, size[1]):
                    if not templategrid.is_collapsed(i, j):
                        all_collapsed = False
                    if templategrid.is_contradiction(i, j):
                        # Contradiction found
                        all_collapsed = False
                        print("Reseting grid...")
                        templategrid.reset_grid(Generator.key_templates)
                        break
            if all_collapsed:
                finished = True
            else: 
                IterationCount += 1
                print("Iteration #", IterationCount, ": ")
                templategrid.print()

        # Create final level
        outGrid = templategrid.grid_to_level(ensureOuterWalls=ensureOuterWalls)

        return outGrid