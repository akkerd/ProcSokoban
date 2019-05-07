from level_parser.template import Template
from generator.generator import Generator
from ai.ai_manager import initiate_ai_solution_search
from inout.utils import read_templates, print_and_write_grid, print_grid

# Algorithm Parameters:
rotation = True
flipping = True

# Read all the 4 rotated versions of each of the key-templates and wildcards
templates = read_templates()

starts = []
rooms = []
goals = []
for extension, template_list in templates.items():
    # TODO: CHECK HERE IF TEMPLATE SIZE IS BIGGER THAN 5x5 
    # AND SPLIT ACCORDINGLY, USING THE ATTRIBUTE "complementary"
    for template in template_list:
        print("Template height: " + str(len(template['lines'])) + " and width: " + str(max(len(x) for x in template['lines'])))
        if len(template['lines']) % 5 != 0 or max(len(x) for x in template['lines']) % 5 != 0:
            print("This template does not have the right size format.")
            raise Exception            
        if extension == "kt":
            starts.append(Template(name=template["name"], lines=template["lines"]))
        elif extension == "wc":
            rooms.append(Template(name=template["name"], lines=template["lines"]))
        elif extension == "gt":
            goals.append(Template(name=template["name"], lines=template["lines"]))

# Generation
generator = Generator(
    starts=starts,
    rooms=rooms,
    goals=goals,
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