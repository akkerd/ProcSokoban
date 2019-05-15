import random
from level_parser.template import Template
from generator.generator import Generator
from ai.ai_manager import initiate_ai_solution_search
from inout.utils import read_templates, print_and_write_grid, print_grid

# Algorithm Parameters:
rotation = False
flipping = False

# Read all the 4 rotated versions of each of the key-templates and wildcards
prototemplates = read_templates()

starts = []
rooms = []
goals = []
for extension, prototemplate_list in prototemplates.items():
    # Check here if template size is bigger than 5x5 
    # and split accordingly, using the attribute "complementary"
    for prototemplate in list(prototemplate_list):
        t_height = len(prototemplate['lines'])
        t_width = max(len(x) for x in prototemplate['lines'])
        print("Template height: " + str(t_height) + " and width: " + str(t_width))

        if t_height % 5 != 0 or t_width % 5 != 0:
            # Check that sizes are multiple of 5
            print("This template does not have the right size format.")
            raise Exception  

        prototemplates_to_keep = []
        if t_height > 5 or t_width > 5:
            # Split templates if size is bigger than 5x5
            t_name = prototemplate["name"]
            t_lines = prototemplate["lines"]
            for i in range(0, int(t_height / 5)):
                for j in range(0, int(t_width / 5)):
                    temp = {
                        'name': t_name,
                        'lines': [t_lines[(i * 5) + x][j * 5:(j + 1) * 5] for x in range(0, 5)],
                        'index': (i, j)
                    }
                    prototemplates_to_keep.append(temp)
            
            prototemplate_list.remove(prototemplate)
            for new_temp in prototemplates_to_keep:
                new_temp['complementary'] = [x['index'] for x in prototemplates_to_keep if new_temp != x]
                prototemplate_list.append(new_temp)
    
    # Parse prototemplates into Template objects
    template_list = []
    for prototemplate in prototemplate_list:
        if prototemplate['complementary']:
            template_list.append(Template(name=prototemplate["name"], lines=prototemplate["lines"], \
                index=prototemplate["index"], complementary=prototemplate['complementary']))
        else:
            template_list.append(Template(name=prototemplate["name"], lines=prototemplate["lines"]), index=(0, 0))

    # Find complementary templates and add them to the list
    for template in template_list:
        if template.needs_complementary():
            complementary_list = [x for x in template_list if x.Index in template.Complementary and x.Name == template.Name]
            template.set_complementary_list(complementary_list)

        if extension == "kt":
            starts.append(template)
        elif extension == "wc":
            rooms.append(template)
        elif extension == "gt":
            goals.append(template)

# Generation
generator = Generator(
    starts=starts,
    rooms=rooms,
    goals=goals,
    seed=127,
    doRotation=True,
    doFlipping=True,
)

level = generator.get_level(size=[5, 5], ensureOuterWalls=False)

# AI
# initiate_ai_solution_search(level)

# Track final level variables
box_count = 0
goals_tracker = []
goals_count = 0
for i, row in level.items():
    for j, char in enumerate(row):
        if char in "ABCDEFGHIJKLMNOPQRSTUVWYZ":
            box_count += 1
        elif char in "abcdefghijklmnopqrstuvwyz":
            goals_tracker.append((i, j))
            goals_count += 1
        elif char == "/":
            level[i][j] = " "

# Place player 
if goals_count - box_count > 0:
    pos = goals_tracker.pop(random.randrange(0, len(goals_tracker)))
    goals_count -= 1
else:
    print("Find a suitable place for the player without using goals")
    raise Exception
level[pos[0]][pos[1]] = "0"

# Remove extra goals
for i in range(0, goals_count - box_count):
    pos = goals_tracker.pop(random.randrange(0, len(goals_tracker)))
    level[pos[0]][pos[1]] = " "


print("Final Iteration: ")
print_and_write_grid(level, "Test") 