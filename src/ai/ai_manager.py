""" 
    Collection of methods to be used in the process of shuffling boxes and goals
"""

from ai.representation.level import Level

def initiate_ai_solution_search(level_grid):
    formatted_level = []
    for key in level_grid.keys():
        formatted_level.append("".join(level_grid[key]))
    level = Level(level=formatted_level)
    print(level)