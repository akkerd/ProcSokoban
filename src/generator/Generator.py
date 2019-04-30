import random
import copy
from generator.template_container import TemplateContainer
from generator.grid import Grid
# from io.utils import print_grid


class Generator:
    keys = set()
    wildcards = set()
    goals = set()

    def __init__(
        self,
        keys,
        wildcards,
        goals,
        seed=None,
        doRotation=False,
        doFlipping=False,
    ):
        '''
            keys: list of Templates [Object, Object]
            wildcards: list of Templates [Object, Object]
            goals: list of Templates [Object, Object]
            seed: integer
        '''
        # Add every template to a container
        if doRotation:
            for rot in range(0, 4):
                for template in keys:
                    Generator.keys.add(TemplateContainer(template=template, rotation=rot))
                for wildcard in wildcards:
                    Generator.wildcards.add(TemplateContainer(template=wildcard, rotation=rot))
                for goal in goals:
                    Generator.goals.add(TemplateContainer(template=goal, rotation=rot))
        else:
            for template in keys:
                Generator.keys.add(TemplateContainer(template=template))
            for wildcard in wildcards:
                Generator.wildcards.add(TemplateContainer(wildcard))
            for goal in goals:
                Generator.goals.add(TemplateContainer(goal))

        if doFlipping:
            for template in tuple(Generator.keys):
                temp_template = copy.copy(template)
                temp_template.flip()
                Generator.keys.add(temp_template)
          
            for wildcard in tuple(Generator.wildcards):
                temp_template = copy.copy(wildcard)
                temp_template.flip()
                Generator.wildcards.add(temp_template)
                    
            for goal in tuple(Generator.goals):
                temp_template = copy.copy(goal)
                temp_template.flip()
                Generator.goals.add(temp_template)

        if seed is not None:
            random.seed(seed)

    def get_level(self, size=[2, 2], ensureOuterWalls=False):
        # Generate the grid
        module_grid = Grid(size=size)

        # Wave Function Collapse
        ## NOTE: Fill grid with Modules
        module_grid.reset_grid(Generator.keys)
        # self.fake_solution(templategrid, size)

        ## NOTE: Iterate updating neighbours
        finished = False
        IterationCount = 0 
        while not finished:
            chosen_one = module_grid.pick_random_module()
            if chosen_one.collapsed:
                continue
            else:
                chosen_one.collapse_random()
                chosen_one.update_neighbours()

            # Check the all templates have collapsed or start all over again
            all_collapsed = True
            for i in range(0, size[0]):
                for j in range(0, size[1]):
                    if not module_grid.is_collapsed(i, j):
                        all_collapsed = False
                    if module_grid.is_contradiction(i, j):
                        # Contradiction found
                        all_collapsed = False
                        print("Reseting grid...")
                        module_grid.reset_grid(Generator.keys)
                        break
            if all_collapsed:
                finished = True
            else: 
                IterationCount += 1
                print("Iteration #", IterationCount, ": ")
                module_grid.print()

        # Run AI that shuffles boxes and goals around
        level_grid = module_grid.get_level_grid()
        # print(level_grid)
        # Create final level
        outGrid = module_grid.levelgrid_to_full_level(level_grid=level_grid, ensureOuterWalls=ensureOuterWalls)

        return outGrid