import random
import copy
from enum import Enum

class State(Enum):
    Closed = 0
    Open = 1
    Collapsed = 2
    Contradiction = 3

class Module:
    def __init__(self, possibilities, position, grid):
        '''
            possibilities: list of TemplateContainers [Object,Object]
            position: tuple [i,j]
        '''
        self.Position = tuple(position)
        self.PossibilitySpace = []
        self.state = State.Closed
        self.updated = False
        self.checked = False
        self.complementary_collapse = False
        self.neighbours = {}
        self.complements = {}
        self.grid = grid
        self.Connections = []

        for template_container in possibilities:
            self.PossibilitySpace.append(template_container)

    def recursive_collapse(self, poss):
        # NOTE: This is the only function where the State can be
        # is set to collapsed
        if self.is_collapsed() and not self.complementary_collapse:
            # Overlapping between templates
            raise Exception
        if self.complementary_collapse:
            # Skip if already collapsed in complementary pass
            return False

        self.complementary_collapse = True

        # Collapse complementary modules
        if poss.needs_complementary():
            for neigh_i, complementary in poss.get_complementary().items():
                if self.neighbours.get(neigh_i):
                    # Allow neighbours to be None if other connections in template can connect
                    # (checked in update if it connects somewhere) 
                    self.neighbours[neigh_i].recursive_collapse(complementary)

        self.PossibilitySpace = [poss]
        self.state = State.Collapsed

        if self.Position not in self.grid.CriticalPath:
            self.grid.expand_cpath(poss, self.Position)
        
        # Open neighbours
        for i in range(0, 4):
            if self.neighbours.get(i):
                if not (self.neighbours[i].is_collapsed() or self.neighbours[i].is_contradiction()):
                    self.neighbours[i].open()

    def collapse(self, poss):
        add_to_cgraph = True
        if self.Position in self.grid.CriticalPath:
            add_to_cgraph = False
        
        self.recursive_collapse(poss)
        
        if add_to_cgraph:
            self.grid.add_to_cgraph(self)

    def collapse_random(self):
        if len(self.PossibilitySpace) is 0:
            print("Possibility scape in module {}, {} is empty".format(self.Position[0], self.Position[1]))
            raise Exception
        else:
            index = random.randrange(0, len(self.PossibilitySpace), 1)

        self.collapse(self.PossibilitySpace[index])

    def set_neighbour(self, neighbour, direction):
        self.neighbours[direction] = neighbour


    def update(self):
        # This function should be the only place where a module gets updated
        if self.updated or self.is_collapsed():
            return True
        to_keep = set()
        for poss in self.PossibilitySpace:
            req_1 = False
            req_2 = False
            if poss.needs_complementary():
                # Check if neighbours contain complementary
                for comp_neigh, comp_tuple in poss.get_complementary().items:
                    if req_1:
                        break
                    if self.neighbours.get(comp_neigh) and not self.neighbours.get(comp_neigh).is_collapsed():
                        for n_poss in self.neighbours[comp_neigh].PossibilitySpace:
                            if n_poss.get_name() == poss.get_name() and n_poss.get_index() == comp_tuple:
                                req_1 = True
                                break
            else:
                req_1 = True

            for i in range(0, 4):
                # Check connectivity with neighbours
                if self.neighbours.get(i):
                    if not poss.get_border(i).IsConnection:
                        continue
                    # Check that this possibility fits with some possibility in neighbours
                    for n_poss in self.neighbours[i].PossibilitySpace:
                        # Calculate inverse border index with function (i+2) % 4
                        if poss.get_border(i) == n_poss.get_border((i + 2) % 4):
                            # Borders fit
                            req_2 = True
                            break
            if req_1 and req_2:
                to_keep.add(poss)

        # Keep only connecting possibilities
        self.PossibilitySpace = list(to_keep)

        if len(self.PossibilitySpace) is 0:
            # Check if the algorithm has run into a contradiction
            self.state = State.Contradiction
            print("Contradiction in ", self.Position)
            self.state = State.Contradiction
        elif len(self.PossibilitySpace) is 1:
            # Check if last available option connects
            connects = False
            for i in range(0, 4):
                if self.neighbours.get(i):
                    if not self.neighbours[i].is_contradiction() and self.PossibilitySpace[0].get_border(i) == self.neighbours[i].PossibilitySpace[0].get_border((i+2) % 4):
                        connects = True
                        break
                        print("Last availabe option connects!")
                else:
                    # Allow connection if last available option connects with out-of-gri
                    connects = True
            if connects:
                self.collapse()
            else:
                # Run into contradiction because the last available option does not connect
                print("Last available option does not connect!")
                self.state = State.Contradiction

        self.updated = True

        # Recurse if needed
        for neighbour in self.neighbours.values():
            if neighbour:
                if not neighbour.updated:
                    neighbour.update()

    def is_collapsed(self):
        return self.state == State.Collapsed

    def is_contradiction(self):
        return self.state == State.Contradiction

    def is_open(self):
        return self.state == State.Open

    def is_closed(self):
        return self.state == State.Closed

    def open(self):
        self.state = State.Open

    def get_final_name(self):
        if not self.is_collapsed():
            print("Module must be collapsed to get grid positions")
            raise Exception
        else:
            name = self.PossibilitySpace[0].get_name()
            if self.PossibilitySpace[0].needs_complementary():
                self.grid.reset_checked_modules()
                s_pos = self.get_final_grid_positions()
            else:
                s_pos = [tuple(self.Position)]
            return name + str(s_pos)

    def get_final_grid_positions(self):
        if not self.is_collapsed():
            print("Module must be collapsed to get grid positions")
            raise Exception
        if self.checked:
            return []
        
        self.checked = True
        positions = [self.Position]
        for comp_i in self.PossibilitySpace[0].get_complementary().keys():
            neigh_pos = self.grid.get_neighbour_pos(self.Position, comp_i)
            neigh_mod = self.grid.get_module(neigh_pos[0], neigh_pos[1])
            # if neigh_mod is not None:
            for pos in neigh_mod.get_final_grid_positions():
                if pos not in positions:
                    positions.append(pos)

        positions.sort()
        return positions
