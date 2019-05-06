from level_parser.template import Template
from generator.generator import Generator
from ai.ai_manager import initiate_ai_solution_search
from inout.utils import read_templates, print_and_write_grid, print_grid

# Algorithm Parameters:
rotation = True
flipping = True

# Read all the 4 rotated versions of each of the key-templates and wildcards
start_list = read_templates(".kt")
room_list = read_templates(".wc")
goal_list = read_templates(".gt")
for count, kt in enumerate(start_list):
    start_list[count] = Template(name=kt["name"], lines=kt["lines"])
for count, wc in enumerate(room_list):
    room_list[count] = Template(name=wc["name"], lines=wc["lines"])
for count, gt in enumerate(goal_list):
    goal_list[count] = Template(name=gt["name"], lines=gt["lines"])

# Generation
generator = Generator(
    starts=start_list,
    rooms=room_list,
    goals=goal_list,
    seed=127,
    doRotation=True,
    doFlipping=True,
)

level = generator.get_level(size=[2, 2], ensureOuterWalls=False)

# AI
# initiate_ai_solution_search(level)

# Place player in level
player_set = False
for row in level.values():
    if "a" in row and not player_set:
        row[row.index("a")] = "0"
        player_set = True
    if "/" in row:
        for i, char in enumerate(row):
            if char == "/":
                row[i] = " "


print("Final Iteration: ")
print_and_write_grid(level, "Test") 