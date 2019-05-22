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
                if prototemplate.get('complementary'):
                    template_list.append(Template(name=prototemplate["name"], lines=prototemplate["lines"], \
                        index=prototemplate["index"], complementary=prototemplate['complementary']))
                else:
                    template_list.append(Template(name=prototemplate["name"], lines=prototemplate["lines"], index=(0, 0)))
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
        grid = Grid(size=size, generator=self)

        # Fill grid with Modules
        grid.reset_grid(self.rooms)
        # self.fake_solution(templategrid, size)

        # Collapse main modules that define the cornerstones: 
        # Starts, Goals and Special (if needed) 
        if pattern == "cathedral":
            # TODO: Insert dome, arcade and wing connections
            raise Exception
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
        all_collapsed = False
        IterationCount = 0 
        while True:
            chosen_one = grid.collapse_next()
            if chosen_one is None:
                # Contradiction found, can't find next module to collapse
                all_collapsed = False
                grid.Reseted = True
                print("Reseting grid...")
                grid.reset_grid(self.rooms)
            else:
                # Check that the critical path is closed between start and goals
                if grid.is_critical_path():
                    # Finished
                    break
                grid.reset_update()
                chosen_one.update()
                if grid.is_critical_path():
                    # Finished
                    break
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
                break
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
        temp_starts = list(self.starts)
        while True:
            start = random.choice(temp_starts)
            # Ensure that the picked module it's a corner module
            while start.get_index() not in [(0, 0), 
                                            (0, int(start.get_cols() / 5)), 
                                            (int(start.get_rows() / 5), 0), 
                                            (int(start.get_rows() / 5), 
                                            int(start.get_cols() / 5))]:
                temp_starts.remove(start)
                start = random.choice(temp_starts)

            # Place template in one of the corners of the grid
            grid_width = grid.Size[0] - 1
            grid_height = grid.Size[1] - 1
            index = start.get_index()
            final_pos = (-1, -1)
            if index == (0, 0) and start.has_connections_at([1, 2], 1):
                final_pos = (0, 0)
            elif index == (0, int(start.get_cols() / 5)) and start.has_connections_at([2, 3], 1):
                final_pos = (0, grid_width)
            elif index == (int(start.get_rows() / 5), 0) and start.has_connections_at([0, 1], 1):
                final_pos = (grid_height, 0)
            elif index == (int(start.get_rows() / 5), int(start.get_cols() / 5)) and start.connects_at([0, 3]):
                final_pos = (grid_height, grid_width)

            if final_pos != (-1, -1):
                # Search finished. Place start and break while
                module = grid.set_start(start, final_pos)
                break

            # If couldn't place this start, remove it from list and continue
            temp_starts.remove(start)

            if len(temp_starts) == 0:
                print("Can't place any of the given start tamplates in the grid!")
                raise Exception

        return module

    def get_possible_connections(self, mod_pos, grid):
        connections = []
        if grid.get_module(mod_pos[0] - 1, mod_pos[1]) is not None:
            connections.append(0)
        if grid.get_module(mod_pos[0], mod_pos[1] + 1) is not None:
            connections.append(1)
        if grid.get_module(mod_pos[0] + 1, mod_pos[1]) is not None:
            connections.append(2)
        if grid.get_module(mod_pos[0], mod_pos[1] - 1) is not None:
            connections.append(3)
        return connections

    def place_goal(self, grid):
        goal_count = 0
        valid_goal = False
        while not valid_goal:
            goal = random.choice(self.goals)
            module_prioque = prioque()
            for i in range(0, grid.Size[0]):
                for j in range(0, grid.Size[1]):
                    # Manhattan distance
                    dist = min(abs(start_pos[0] - i) + abs(start_pos[1] - j) for start_pos in grid.Start)
                    module_prioque.put((-dist, (i, j)))
            
            mod_pos = module_prioque.get()[1]
            connections = self.get_possible_connections(mod_pos, grid)

            stopped = False
            while not grid.can_set_templatec(goal, mod_pos) or not goal.has_connections_at(connections, 1):
                if module_prioque.empty():
                    stopped = True
                    break
                mod_pos = module_prioque.get()[1]
            if not stopped:
                # Found good goal template
                valid_goal = True
            else:
                # Timeout if all goals checked
                goal_count += 1
                if goal_count == len(self.goals):
                    raise Exception

        return grid.set_goal(goal, (mod_pos[0], mod_pos[1]))