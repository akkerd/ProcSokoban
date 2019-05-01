from level_parser.template import Template
from generator.generator import Generator
from ai.ai_manager import initiate_ai_solution_search
from inout.utils import read_templates, print_and_write_grid, print_grid

# Algorithm Parameters:
rotation = True
flipping = False

prioritize_loops = False
prioritize_double_edge_nodes = False
prioritize_triple_edge_nodes = False

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

level = generator.get_level(size=[3, 3], ensureOuterWalls=True)

# AI
# initiate_ai_solution_search(level)

# Place player in level
for row in level.values():
    if "a" in row:
        row[row.index("a")] = "0"
        break


print("Final Iteration: ")
print_and_write_grid(level, "Test")