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
key_template_list, wildcard_list = read_templates()
for count, kt in enumerate(key_template_list):
    key_template_list[count] = Template(name=kt["name"], lines=kt["lines"])
for count, wc in enumerate(wildcard_list):
    wildcard_list[count] = Template(name=wc["name"], lines=wc["lines"])

# Generation
generator = Generator(
    key_templates=key_template_list,
    wildcards=wildcard_list,
    seed=127,
    pRotation=True,
    pFlipping=False,
    pPrioritize_loops=False,
    pPrioritize_double_edge_nodes=False,
    pPrioritize_triple_edge_nodes=False
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