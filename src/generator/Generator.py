import random
import copy
from generator.template_container import TemplateContainer
from generator.grid import Grid
from generator.module import State
# from io.utils import print_grid


class Generator:
    starts = []
    rooms = []
    goals = []

    def __init__(
        self,
        starts,
        rooms,
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

        for start in starts:
            Generator.starts.append(TemplateContainer(template=start))
        for room in rooms:
            Generator.rooms.append(TemplateContainer(template=room))
        for goal in goals:
            Generator.goals.append(TemplateContainer(template=goal))

        # Add every template to a container
        if doRotation:
            for rot in range(0, 4):
                for start in starts:
                    Generator.starts.append(TemplateContainer(template=start, rotation=rot))
                for room in rooms:
                    Generator.rooms.append(TemplateContainer(template=room, rotation=rot))
                for goal in goals:
                    Generator.goals.append(TemplateContainer(template=goal, rotation=rot))
        else:
            for start in starts:
                Generator.starts.append(TemplateContainer(template=start))
            for room in rooms:
                Generator.rooms.append(TemplateContainer(template=room))
            for goal in goals:
                Generator.goals.append(TemplateContainer(template=goal))

        if doFlipping:
            for start in tuple(Generator.starts):
                temp_template = copy.copy(start)
                temp_template.flip()
                Generator.starts.append(temp_template)
          
            for room in tuple(Generator.rooms):
                temp_template = copy.copy(room)
                temp_template.flip()
                Generator.rooms.append(temp_template)
                    
            for goal in tuple(Generator.goals):
                temp_template = copy.copy(goal)
                temp_template.flip()
                Generator.goals.append(temp_template)

        if seed is not None:
            random.seed(seed)

    def get_level(self, size=[2, 2], ensureOuterWalls=False, pattern=""):
        # Generate the grid
        grid = Grid(size=size)

        # Fill grid with Modules
        grid.reset_grid(Generator.rooms)
        # self.fake_solution(templategrid, size)

        # Collapse main modules that define the cornerstones: 
        # Starts, Goals and Special (if needed) 
        if pattern == "cathedral":
            # TODO: Insert dome, arcade and wing connections
            x = 1
        else:
            # Default case, insert start (boxes) and (goals)
            # start_module = self.place_start(grid, random.sample(Generator.starts, 1)[0])
            start_module = self.place_start(grid, random.choice(Generator.starts))
            start_module.update()
            # goal_module = self.place_goal(grid, random.sample(Generator.goals, 1)[0])
            goal_module = self.place_goal(grid, random.choice(Generator.goals))
            goal_module.update()

        #############################################################################
        ########################### Wave Function Collapse ##########################
        #############################################################################

        ## NOTE: Iterate updating neighbours
        finished = False
        IterationCount = 0 
        while not finished:
            chosen_one = grid.pick_next()
            chosen_one.collapse_random()
            chosen_one.update()

            # Check the all templates have collapsed or start all over again
            all_collapsed = True
            for i in range(0, size[0]):
                for j in range(0, size[1]):
                    if not grid.get_module(i, j).is_collapsed() and not grid.get_module(i, j).is_contradiction():
                        all_collapsed = False
                    # if grid.is_contradiction(i, j):
                    #     # Contradiction found
                    #     all_collapsed = False
                    #     print("Reseting grid...")
                    #     grid.reset_grid(Generator.starts)
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

    def place_start(self, grid, start):
        size_x = grid.Size[0] - 1
        size_y = grid.Size[1] - 1
        # Check all corners first
        if grid.get_module(0, 0).state in (State.Open, State.Closed):
            if start.get_border(1).is_connection() or start.get_border(2).is_connection(): 
                return grid.set_start(start, (0, 0))
        if grid.get_module(0, size_y).state in (State.Open, State.Closed):
            if start.get_border(2).is_connection() or start.get_border(3).is_connection():
                return grid.set_start(start, (0, size_y)) 
        if grid.get_module(size_x, 0).state in (State.Open, State.Closed):
            if start.get_border(0).is_connection() or start.get_border(1).is_connection():
                return grid.set_start(start, (size_x, 0)) 
        if grid.get_module(size_x, size_y).state in (State.Open, State.Closed):
            if start.get_border(0).is_connection() \
                or start.get_border(3).is_connection():
                return grid.set_start(start, (size_x, size_y)) 

        raise NotImplementedError
        # Check edges after
        for i in range(1, size_x):
            for j in range(1, size_y):
                if not grid.get_module(i)(j).state in (State.Open, State.Closed):
                    raise NotImplementedError

    def place_goal(self, grid, goal):
        start_pos = grid.Starts[0]
        max_dist = 0
        for i in range(0, grid.Size[0]):
            for j in range(0, grid.Size[1]):
                # Manhattan distance
                dist = abs(start_pos[0] - i) + abs(start_pos[1] - j)
                if dist > max_dist:
                    max_dist = dist
                    goal_pos = (i, j)
        if goal_pos:
            return grid.set_goal(goal, (goal_pos[0], goal_pos[1]))
        else:
            raise Exception