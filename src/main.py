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
    # Check here if template size is bigger than 5x5 
    # and split accordingly, using the attribute "complementary"
    for template in list(template_list):
        t_height = len(template['lines'])
        t_width = max(len(x) for x in template['lines'])
        print("Template height: " + str(t_height) + " and width: " + str(t_width))
        
        if t_height % 5 != 0 or t_width % 5 != 0:
            # Check that sizes are multiple of 5
            print("This template does not have the right size format.")
            raise Exception  

        templates_toadd = []
        if t_height > 5 or t_width > 5:
            # Split templates if size is bigger than 5x5
            t_name = template["name"]
            t_lines = template["lines"]
            for i in range(0, int(t_height / 5)):
                for j in range(0, int(t_width / 5)):
                    temp = {
                        'name': t_name,
                        'lines': [t_lines[i][j * 5:(j + 1) * 5] for i in range(i * 5, (i + 1) * 5)],
                        'index': (i, j)
                    }
                    templates_toadd.append(temp)
            
            template_list.remove(template)
            for new_temp in templates_toadd:
                new_temp['complementary'] = [x['index'] for x in templates_toadd if new_temp != x]
                template_list.append(new_temp)
    
    for template in template_list:
        if template['complementary']:
            temp_obj = Template(name=template["name"], lines=template["lines"], \
                index=template["index"], complementary=template['complementary'])
        else:
            temp_obj = Template(name=template["name"], lines=template["lines"])

        if extension == "kt":
            starts.append(temp_obj)
        elif extension == "wc":
            rooms.append(temp_obj)
        elif extension == "gt":
            goals.append(temp_obj)

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