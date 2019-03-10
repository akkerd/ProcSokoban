import random
import copy
from enum import Enum

from Tools.scripts.pathfix import new_interpreter

# class Direction(Enum):
#     Up = 0
#     Right = 1
#     Down = 2
#     Left = 3

class Module:
    def __init__(self, possibilities):
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
        for possibility in self.PossibilitySpace:
            # Check that this possibility fits with some possibility in neighbours
            for i in range(0, 4):
                if self.neighbours.get(i):
                    to_remove = []
                    for neighbour_possibility in self.neighbours[i].PossibilitySpace:
                        # Calculate inverse border index with function (i+2) % 4
                        if not neighbour_possibility.template.borders[(i+2) % 4].connects(possibility.template.borders[i]):
                            to_remove.append(neighbour_possibility)
                    # Remove items
                    for j in range(0, len(to_remove)):
                        self.neighbours[i].PossibilitySpace.remove(to_remove[j])

                    # NOTE: Check if the algorithm has run into a contradiction
                    if len(self.neighbours[i].PossibilitySpace) is 0:
                        self.neighbours[i].contradiction = True
                        print("Contradiction found. Starting over algorithm...")
                        break
                    # Check if last available option connects
                    if len(self.neighbours[i].PossibilitySpace) is 1:
                        if self.neighbours[i].PossibilitySpace[0].template.borders[i].connects(self.neighbours[i].PossibilitySpace[0].template.borders[(i+2) % 4]):
                            print("Last availabe option connects!")
                            self.neighbours[i].collapsed = True
                        else:
                            # Run into contradiction because the last available option does not connect
                            print("Last available option does not connect")
                            self.neighbours[i].contradiction = True
        self.updated = True

        # Recurse if needed
        for neighbour in self.neighbours.values():
            if neighbour:
                if not neighbour.updated:
                    # if not self.collapsed:
                    neighbour.update_neighbours()
