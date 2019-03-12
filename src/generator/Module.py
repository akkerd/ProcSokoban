import random
import copy
from enum import Enum

from Tools.scripts.pathfix import new_interpreter

# class Direction(Enum):
#     North = 0
#     East = 1
#     South = 2
#     West = 3

class Module:
    def __init__(self, possibilities, position):
        self.Position = position
        self.PossibilitySpace = []
        self.collapsed = False
        self.updated = False
        self.contradiction = False
        self.neighbours = {}

        for template_container in possibilities:
            self.PossibilitySpace.append(template_container)

    def collapse_random(self):
        index = random.randrange(0, len(self.PossibilitySpace))
        # TODO: Can be optimized?
        temp = copy.deepcopy(self.PossibilitySpace[index])
        self.PossibilitySpace.clear()
        self.PossibilitySpace.append(temp)
        self.collapsed = True

    def set_neighbour(self, neighbour, direction):
        self.neighbours[direction] = neighbour

    def update_neighbours(self):
        for i in range(0, 4):
            if self.neighbours.get(i):
                # Check that this possibility fits with some possibility in neighbours
                to_keep = set()
                for neighbour_possibility in self.neighbours[i].PossibilitySpace:
                    for possibility in self.PossibilitySpace:
                        # Calculate inverse border index with function (i+2) % 4
                        if neighbour_possibility.template.borders[(i+2) % 4].connects(possibility.template.borders[i]):
                            to_keep.add(neighbour_possibility)

                # Keep only connecting possibilities
                self.neighbours[i].PossibilitySpace = list(to_keep)

                # for j in range(0, len(to_remove)):
                #     self.neighbours[i].PossibilitySpace.remove(to_remove[j])

                # NOTE: Check if the algorithm has run into a contradiction
                if len(self.neighbours[i].PossibilitySpace) is 0:
                    self.neighbours[i].contradiction = True
                    print("Contradiction found. Starting over algorithm...")
                    return 0
                # Check if last available option connects
                elif len(self.neighbours[i].PossibilitySpace) is 1:
                    if self.neighbours[i].PossibilitySpace[0].template.borders[(i+2) % 4].connects(self.PossibilitySpace[0].template.borders[i]):
                        # print("Last availabe option connects!")
                        self.neighbours[i].collapsed = True
                    else:
                        # Run into contradiction because the last available option does not connect
                        print("Last available option does not connect!")
                        self.neighbours[i].contradiction = True
        self.updated = True

        # Recurse if needed
        for neighbour in self.neighbours.values():
            if neighbour:
                if not neighbour.updated:
                    # if not self.collapsed:
                    neighbour.update_neighbours()