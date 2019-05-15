import random
import copy
from level_parser.template import Template
from generator.template_container import TemplateContainer
from generator.grid import Grid
from generator.module import State
from queue import PriorityQueue as prioque
# from io.utils import print_grid


class Generator:

    def __init__(
        self,
        prototemplates,
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
        self.starts = []
        self.rooms = []
        self.goals = []

        # Parse prototemplates into Template objects
        for extension, prototemplate_list in prototemplates.items(): 
            template_list = []
            for prototemplate in prototemplate_list:
                if prototemplate['complementary']:
                    template_list.append(Template(name=prototemplate["name"], lines=prototemplate["lines"], \
                        index=prototemplate["index"], complementary=prototemplate['complementary']))
                else:
                    template_list.append(Template(name=prototemplate["name"], lines=prototemplate["lines"]), index=(0, 0))
            for template in template_list:
                # Find complementary templates and add template references
                if template.needs_complementary():
                    complementary_list = [x for x in template_list if x.Index in template.Complementary and x.Name == template.Name]
                    template.set_complementary_list(complementary_list)
                # Create template_container and add it to corresponding list
                if extension == "kt":
                    self.starts.append(TemplateContainer(template=template))
                elif extension == "wc":
                    self.rooms.append(TemplateContainer(template=template))
                elif extension == "gt":
                    self.goals.append(TemplateContainer(template=template))

        # Do rotations if neccessary
        if doRotation:
            for rot in range(0, 4):
                for start in tuple(self.starts):
                    start.set_rotation(rot)
                    self.starts.append(start)
                for room in tuple(self.rooms):
                    room.set_rotation(rot)
                    self.rooms.append(room)
                for goal in tuple(self.goals):
                    goal.set_rotation(rot)
                    self.goals.append(goal)
        
        # Do flip if neccessary
        if doFlipping:
            for start in tuple(self.starts):
                start.flip()
                self.starts.append(start)
            for room in tuple(self.rooms):
                room.flip()
                self.rooms.append(room)
            for goal in tuple(self.goals):
                goal.flip()
                self.goals.append(goal)

        if seed is not None:
            random.seed(seed)

    def get_level(self, size=[2, 2], ensureOuterWalls=False, pattern=""):
        # Generate the grid
        grid = Grid(size=size)

        # Fill grid with Modules
        grid.reset_grid(self.rooms)
        # self.fake_solution(templategrid, size)

        # Collapse main modules that define the cornerstones: 
        # Starts, Goals and Special (if needed) 
        if pattern == "cathedral":
            # TODO: Insert dome, arcade and wing connections
            x = 1
        else:
            # Default case, insert start (boxes) and (goals)
            # start_module = self.place_start(grid, random.sample(self.starts, 1)[0])
            start_module = self.place_start(grid)
            grid.reset_update()
            start_module.update()

            # goal_module = self.place_goal(grid, random.sample(self.goals, 1)[0])
            goal_module = self.place_goal(grid)
            grid.reset_update()
            goal_module.update()

        #############################################################################
        ########################### Wave Function Collapse ##########################
        #############################################################################

        ## NOTE: Iterate updating neighbours
        finished = False
        IterationCount = 0 
        while not finished:
            chosen_one = grid.collapse_next()
            grid.reset_update()
            chosen_one.update()

            # Check the critical path is closed between start and goals
            all_collapsed = True
            for i in range(0, size[0]):
                for j in range(0, size[1]):
                    module = grid.get_module(i, j)
                    if not module.is_collapsed() and not module.is_contradiction():
                        all_collapsed = False
                    # if grid.is_contradiction(i, j):
                    #     # Contradiction found
                    #     all_collapsed = False
                    #     print("Reseting grid...")
                    #     grid.reset_grid(self.starts)
                    #     break
            if all_collapsed:
                finished = True
            else: 
                IterationCount += 1
                print("Iteration #", IterationCount, ": ")
                grid.print()

        #############################################################################
        ######################### Run AI to shuffle elements ########################
        #############################################################################
        # TODO

        #############################################################################
        ############################ Final level creation ###########################
        #############################################################################
        # Create final level
        outGrid = grid.get_full_level(ensureOuterWalls=ensureOuterWalls)

        return outGrid

    def place_start(self, grid):
        start = random.choice(self.starts)
        while start.get_index() not in [(0, 0), (0, int(start.get_cols() / 5)), (int(start.get_rows() / 5), 0), (int(start.get_rows() / 5), int(start.get_cols() / 5))]:
                start = random.choice(self.starts)

        grid_width = grid.Size[0] - 1
        grid_height = grid.Size[1] - 1
        if start.get_index() == (0, 0):
            module = grid.set_start(start, (0, 0), self.starts)
        elif start.get_index() == (0, int(start.get_cols() / 5)):
            module = grid.set_start(start, (0, grid_width), self.starts)
        elif start.get_index() == (int(start.get_rows() / 5), 0):
            module = grid.set_start(start, (grid_height, 0), self.starts)
        elif start.get_index() == (int(start.get_rows() / 5), int(start.get_cols() / 5)):
            module = grid.set_start(start, (grid_height, grid_width), self.starts)
        
        return module

    def place_goal(self, grid):
        start_pos = grid.Starts[0]
        goal_count = 0
        valid_goal = False
        while not valid_goal:
            goal = random.choice(self.goals)
            module_prioque = prioque()
            for i in range(0, grid.Size[0]):
                for j in range(0, grid.Size[1]):
                    # Manhattan distance
                    dist = abs(start_pos[0] - i) + abs(start_pos[1] - j)
                    module_prioque.put((-dist, (i, j)))
            
            module_pos = module_prioque.get()
            stopped = False
            while not grid.can_set_templatec(goal, module_pos[1]):
                if module_prioque.empty():
                    stopped = True
                    break
                module_pos = module_prioque.get()
            if not stopped:
                # Found good goal template
                valid_goal = True
            else:
                # Timeout if all goals checked
                goal_count += 1
                if goal_count == len(self.goals):
                    raise Exception

        return grid.set_goal(goal, (module_pos[1][0], module_pos[1][1]))