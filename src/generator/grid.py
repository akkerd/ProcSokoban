import copy
import random
from generator.module import Module
from generator.utils import Utils
from inout.utils import IOUtils
from data_structures.graph import ModuleGraph

class Grid:

    def __init__(self, size, generator):
        self.Size = size
        self.Module_Grid = [[None for i in range(size[0])] for j in range(size[1])]
        self.Start = []
        self.Goal = []
        self.CriticalPath = []
        self.CPathGraph = None
        self.CheckedPositions = []
        self.HaveCriticalPath = False
        self.Reseted = False

    def reset_grid(self, templates, prune_edges=False):
        '''
            templates: list of TemplateContainers [Object, object]
        '''
        self.CriticalPath = []
        to_keep = []
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                if (i, j) in self.Goal or (i, j) in self.Start:
                    self.CriticalPath.append((i, j))
                    mod = self.get_module(i, j)
                    mod.neighbours = {}
                    to_keep.append(mod)
                    continue
                possibility_space = copy.copy(templates)
                if prune_edges:
                    self.prune_templates(possibility_space, i, j)
                self.Module_Grid[i][j] = Module(possibilities=possibility_space, position=[i, j], grid=self)

        # Set modules' neighbours
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                # North
                if i - 1 > -1:
                    self.get_module(i, j).set_neighbour(self.get_module(i - 1, j), 0)
                # East
                if j + 1 < self.Size[1]:
                    self.get_module(i, j).set_neighbour(self.get_module(i, j + 1), 1)
                # South
                if i + 1 < self.Size[0]:
                    self.get_module(i, j).set_neighbour(self.get_module(i + 1, j), 2)
                # West
                if j - 1 > -1:
                    self.get_module(i, j).set_neighbour(self.get_module(i, j - 1), 3)  
        
        for crit_mod in to_keep:
            # Open neighbours
            for i in range(0, 4):
                if crit_mod.neighbours.get(i):
                    if not (crit_mod.neighbours[i].is_collapsed() or crit_mod.neighbours[i].is_contradiction()):
                        crit_mod.neighbours[i].open()

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

    def reset_update(self):
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                self.get_module(i, j).updated = False
    
    def reset_check(self):
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                self.get_module(i, j).checked = False

    def get_module(self, i, j):
        if i < 0 or j < 0 or i > self.Size[0] - 1 or j > self.Size[1] - 1:
            return None
        else:
            return self.Module_Grid[i][j]

    def get_open_list(self, ignore_list=[]):
        open_list = []

        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                if self.get_module(i, j).is_open():
                    module = self.get_module(i, j)
                    if module not in ignore_list:
                        open_list.append(module)

                    if len(module.PossibilitySpace) == 0:
                        # CHECK: Open module should have possibilities, else it would have
                        # been set to contradiction when updating
                        raise Exception
        
        if len(open_list) == 0:
            # CHECK: There should be open modules to continue
            raise Exception

        return open_list

    def get_neighbour_pos(self, pos: tuple, neigh_i):
        neigh_pos = (-1, -1)
        if neigh_i is 0:
            neigh_pos = (pos[0] - 1, pos[1])
        elif neigh_i is 1:
            neigh_pos = (pos[0], pos[1] + 1)
        elif neigh_i is 2:
            neigh_pos = (pos[0] + 1, pos[1])
        elif neigh_i is 3:
            neigh_pos = (pos[0], pos[1] - 1)
        return tuple(neigh_pos)

    def pick_random(self, module_list):
        return random.choice(module_list)

    def pick_next(self, module_list, use_distance_function=True):
        if use_distance_function:
            # Find open modules with minimum distance from goals
            heuristic = [0] * len(module_list)
            for k, openm in enumerate(module_list):
                # Calculate connection possibility
                # max_conn, max_templates = self.get_max_conn_templates(openm.PossibilitySpace)

                heuristic[k] = self.get_module_dist(openm)
                # Get minimum conn value
            
            candidate_indexes = self.locate_min_indexes(heuristic)
        else:
            candidate_indexes = []
            for i, module in enumerate(module_list):
                candidate_indexes.append(i)

        if len(candidate_indexes) != 1:
            # If some cells are at same distance, pick module \
            # with minimum entropy in its PossibilitySpace
            min_entropy = 100000
            for m in candidate_indexes:
                entropy = len(module_list[m].PossibilitySpace)
                if entropy < min_entropy:
                    chosen_index = m
        elif len(candidate_indexes) == 0:
            raise Exception
        else:
            chosen_index = candidate_indexes[0]

        return module_list[chosen_index]
 
    def collapse_next(self):
        use_distance_heuristic = not self.Reseted
        open_list = self.get_open_list()

        if self.Reseted:
            module_candidate = self.pick_random(open_list)
        else:
            module_candidate = self.pick_next(open_list, True)

        if use_distance_heuristic:
            template_candidates = self.get_min_dist_templates(module_candidate)
        else:
            template_candidates = self.get_max_conn_templates(module_candidate)

        templatec = random.choice(template_candidates)
        self.CheckedPositions = []
        self.reset_check()
        contradiction = False
        while not self.can_set_templatec(templatec, module_candidate.Position) or not self.templatec_expands_cpath(templatec, module_candidate.Position):
            template_candidates.remove(templatec)
            if len(template_candidates) == 0:
                open_list.remove(module_candidate)
                if len(open_list) == 0:
                    print("################# CONTRADICTION #################")
                    print("Contradiction found, can't ensure critical path")
                    contradiction = True
                    break
                module_candidate = self.pick_next(open_list, use_distance_heuristic)
                template_candidates = self.get_min_dist_templates(module_candidate)

            templatec = random.choice(template_candidates)
            self.CheckedPositions = []
            self.reset_check()

        if contradiction:
            return None
        module_candidate.collapse(templatec)
        return module_candidate

    def can_set_templatec(self, template, pos: tuple):
        module = self.get_module(pos[0], pos[1])
        if module.checked:
            # Avoid checking modules more than once
            return True
        if module.is_collapsed():
            return False
        if template.needs_complementary():
            for neigh_i, complementary in template.get_complementary().items():
                if not module.neighbours.get(neigh_i):
                    return False
            module.checked = True
            for neigh_i, complementary in template.get_complementary().items():        
                if not self.can_set_templatec(complementary, module.neighbours[neigh_i].Position):
                    return False
        else:
            module.checked = True

        return True

    def distance_function(self, pos: tuple):
        # Calculate distance from goal
        dist_goal = min(abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1]) for goal_pos in self.Goal)
        # Calculate distance from start
        dist_start = min(abs(pos[0] - start_pos[0]) + abs(pos[1] - start_pos[1]) for start_pos in self.Start) 
        return dist_goal + dist_start

    def get_module_dist(self, module):
        templatec_list = module.PossibilitySpace
        conn_distances = []
        conn_dist = self.distance_function(module.Position)
        for templatec in templatec_list:
            if templatec.needs_complementary():
                final_conn_dist = min(conn_dist, min(self.distance_function(self.get_neighbour_pos(module.Position, neigh_i))
                                    for neigh_i in templatec.get_complementary().keys()))
            else:
                final_conn_dist = conn_dist
            conn_distances.append(final_conn_dist)

        return min(conn_distances)

    def get_max_conn_templates(self, module):
        templatec_list = module.PossibilitySpace
        max_conn = max(m.get_connections() for m in templatec_list)
        max_temp = [m for m in templatec_list if m.get_connections() == max_conn]
        return max_temp

    def get_min_dist_templates(self, module):
        templatec_list = module.PossibilitySpace
        conn_distances = []
        conn_dist = self.distance_function(module.Position)
        for templatec in templatec_list:
            if templatec.needs_complementary():
                final_conn_dist = min(conn_dist, min(self.distance_function(self.get_neighbour_pos(module.Position, neigh_i))
                                    for neigh_i in templatec.get_complementary().keys()))
            else:
                final_conn_dist = conn_dist
            conn_distances.append(final_conn_dist)

        min_indexes = self.locate_min_indexes(conn_distances)
        min_templates = []
        if len(min_indexes) != 0:
            for index in min_indexes:
                min_templates.append(templatec_list[index])
        else:
            raise Exception

        return min_templates

    def locate_min_indexes(self, p_list):
        min_indexes = []
        smallest = min(p_list)
        for index, element in enumerate(p_list):
                if smallest == element: # check if this element is the minimum_value
                        min_indexes.append(index) # add the index to the list if it is

        return min_indexes

    def set_start(self, start, pos: tuple):
        pos = tuple(pos)
        module = self.get_module(pos[0], pos[1])
        self.add_position_to_list(pos, start, self.Start)
        self.add_position_to_list(pos, start, self.CriticalPath)
        module.collapse(start)
        return module
    
    def set_goal(self, goal, pos: tuple):
        pos = tuple(pos)
        module = self.get_module(pos[0], pos[1])
        self.add_position_to_list(pos, goal, self.Goal)
        self.add_position_to_list(pos, goal, self.CriticalPath)
        module.collapse(goal)

        # Initialize CPathGraph
        start = self.get_module(self.Start[0][0], self.Start[0][1])
        self.CPathGraph = ModuleGraph(start.get_final_name(), start, module.get_final_name(), module)
        return module

    def add_position_to_list(self, mod_pos: tuple, templatec, p_list):
        if mod_pos in p_list:
            return True

        p_list.append(mod_pos)
        if templatec.needs_complementary():
            for comp_i, comp in templatec.get_complementary().items():
                comp_pos = self.get_neighbour_pos(mod_pos, comp_i)
                self.add_position_to_list(comp_pos, comp, p_list)

    def templatec_expands_cpath(self, templatec, pos: tuple):
        """
        Fast version for checking if the given template expands the critical path.
        If any template from the complementary list expands it, break and return True
        """
        if not self.get_module(pos[0], pos[1]):
            # Null check
            return False

        expands_cpath = False
        for i in range(0, 4):
            neigh_pos = self.get_neighbour_pos(pos, i)
            if neigh_pos in self.CriticalPath:
            # Template connection points towards the Critical Path
                neigh_mod = self.get_module(neigh_pos[0], neigh_pos[1])
                if templatec.get_border(i) == neigh_mod.PossibilitySpace[0].get_border((i + 2) % 4):
                # and Critical Path's corresponding module connects with this template
                    expands_cpath = True
                    break

        self.CheckedPositions.append(pos)

        if not expands_cpath and templatec.needs_complementary():
            # If this template does not expand the cpath, check complementary templates
            for comp_i, comp in templatec.get_complementary().items():
                comp_pos = self.get_neighbour_pos(pos, comp_i)
                if comp_pos not in self.CheckedPositions:
                # Avoid checking complementary templates twice
                    if self.templatec_expands_cpath(comp, comp_pos):
                    # Recursive call to this function check if it expands the cpath
                        expands_cpath = True
                        # If one of the templates expands the cpath, that is enough
                        break
        
        return expands_cpath

    def expand_cpath(self, templatec, pos: tuple):
        """
        Explore template and complementaries while expanding the critical path along the way
        """
        if not self.get_module(pos[0], pos[1]) or pos in self.CheckedPositions:
            # Null check
            return False

        module = self.get_module(pos[0], pos[1])
        for i in range(0, 4):
            neigh_pos = self.get_neighbour_pos(pos, i)
            if neigh_pos in self.CriticalPath:
            # Template connection points towards the Critical Path
                neigh_mod = self.get_module(neigh_pos[0], neigh_pos[1])
                if templatec.get_border(i) == neigh_mod.PossibilitySpace[0].get_border((i + 2) % 4):
                # and Critical Path's corresponding module connects with this template
                    module.Connections.append(neigh_pos)
                    neigh_mod.Connections.append(pos)

        self.CheckedPositions.append(pos)
        self.add_to_cpath(pos)

        if templatec.needs_complementary():
            # Expand complementary templates
            for comp_i, comp in templatec.get_complementary().items():
                comp_pos = self.get_neighbour_pos(pos, comp_i)
                # Recursive call to this function to expand the cpath
                self.expand_cpath(comp, comp_pos)                        
        return True

    def add_to_cpath(self, pos: tuple):
        self.CriticalPath.append(tuple(pos))
            
    def is_critical_path(self):
        return self.HaveCriticalPath

    def print(self):
        level = self.get_full_level()
        IOUtils.print_grid(level)

    def get_level_grid(self):
        """ 
            This function takes a grid (double dimensional list) of
            Modules and turns it into a grid of OriginalLevels.

            An OriginalLevel is a 2-dimensional matrix of lists of characters that 
            represent the original template (already rotated and/or fliped).
        """
        # Get module_grid into level_grid
        level_grid = [[None for i in range(self.Size[0])] for j in range(self.Size[1])]
        for i in range(0, self.Size[0]):
            for j in range(0, self.Size[1]):
                try:
                    if self.get_module(i, j).is_collapsed():
                        level_grid[i][j] = self.Module_Grid[i][j].PossibilitySpace[0].get_level()
                    else:
                        if self.get_module(i, j).is_contradiction():
                            level_grid[i][j] = self.get_empty_template(5, 5)
                        else:
                            level_grid[i][j] = self.get_temp_template(5, 5)
                except IndexError as e:
                    print("IndexError:", e)
        return level_grid

    def get_full_level(self, ensureOuterWalls=False):
        """ 
        This function takes a grid (double dimensional list) of OriginalLevels and 
        turns it into a grid containing the characters that make the final level.
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
                        level[row_count + column_size[level_column_count]] = copy.copy(row)

                # Update lenght of column
                column_size[level_column_count] += len(original_level)

        if ensureOuterWalls:
            level = Utils.ensureOuterWalls(level)

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
    
    def add_to_cgraph(self, module):
        connections = list(module.Connections)
        for i, conn in enumerate(connections):
            connections[i] = self.get_module(conn[0], conn[1]).get_final_name()
        self.CPathGraph.AddNode(module.get_final_name(), module, connections)
        self.HaveCriticalPath = self.CPathGraph.IsCriticalPath()
