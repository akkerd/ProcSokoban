import random
from generator.template_container import TemplateContainer
from generator.grid import Grid
# from io.utils import print_grid


class Generator:
    key_templates = []
    wildcards = []

    def __init__(
        self,
        key_templates,
        wildcards=[],
        seed=None,
        pRotation=False,
        pFlipping=False,
        pPrioritize_loops=False,
        pPrioritize_double_edge_nodes=False,
        pPrioritize_triple_edge_nodes=False
    ):
        '''
            key_templates: list of Templates [Object, Object]
            wildcards: list of Templates [Object, Object]
            seed: integer
        '''
        # Add every template to a container
        for template in key_templates:
            Generator.key_templates.append(TemplateContainer(template=template))
            if pRotation:
                for rot in range(0, 4):
                    Generator.key_templates.append(
                        TemplateContainer(template=template, rotation=rot)
                    )
            else:
                Generator.key_templates.append(
                    TemplateContainer(template=template, rotation=0)
                )

        # Add every template to a container
        for wildcard in wildcards:
            Generator.wildcards.append(TemplateContainer(wildcard))
        if seed is not None:
            random.seed(seed)

    def get_level(self, size=[2, 2], ensureOuterWalls=False):
        # Generate the grid
        module_grid = Grid(size=size)

        # Wave Function Collapse
        ## NOTE: Fill grid with Modules
        module_grid.reset_grid(Generator.key_templates)
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
                        module_grid.reset_grid(Generator.key_templates)
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