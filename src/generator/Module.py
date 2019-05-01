import random
import copy
from enum import Enum

class State(Enum):
    Closed = 0
    Open = 1
    Collapsed = 2
    Contradiction = 3

class Module:
    def __init__(self, possibilities, position):
        '''
            possibilities: list of TemplateContainers [Object,Object]
            position: tuple [i,j]
        '''
        self.Position = position
        self.PossibilitySpace = []
        self.state = State.Closed
        self.updated = False
        self.neighbours = {}

        for template_container in possibilities:
            self.PossibilitySpace.append(template_container)

    def collapse_random(self):
        if len(self.PossibilitySpace) is 0:
            print("Possibility scape in module {}, {} is empty".format(self.Position[0], self.Position[1]))
            raise Exception
        else:
            index = random.randrange(0, len(self.PossibilitySpace), 1)
        
        self.PossibilitySpace = [self.PossibilitySpace[index]]
        self.state = State.Collapsed

    def set_neighbour(self, neighbour, direction):
        self.neighbours[direction] = neighbour

    def update(self):
        to_keep = set()
        for i in range(0, 4):
            if self.neighbours.get(i):
                # Check that this possibility fits with some possibility in neighbours
                for poss in self.PossibilitySpace:
                    for n_poss in self.neighbours[i].PossibilitySpace:
                        # Calculate inverse border index with function (i+2) % 4
                        if poss.get_border(i) == n_poss.get_border((i+2) % 4):
                            to_keep.add(poss)

        # Keep only connecting possibilities
        self.PossibilitySpace = list(to_keep)

        if len(self.PossibilitySpace) is 0:
            # Check if the algorithm has run into a contradiction
            self.state = State.Contradiction
            print("Contradiction in ")
            return 0
        elif len(self.PossibilitySpace) is 1:
            # Check if last available option connects
            connects = False
            for i in range(0, 4):
                if self.neighbours.get(i):
                    if self.PossibilitySpace[0].get_border(i) == self.neighbours[i].PossibilitySpace[0].get_border((i+2) % 4):
                        connects = True                        
                        print("Last availabe option connects!")
            if connects:
                self.neighbours[i].state = State.Collapsed
            else:
                # Run into contradiction because the last available option does not connect
                print("Last available option does not connect!")
                self.neighbours[i].state = State.Contradiction

        self.updated = True

        # Recurse if needed
        for neighbour in self.neighbours.values():
            if neighbour:
                if not neighbour.updated:
                    neighbour.update()