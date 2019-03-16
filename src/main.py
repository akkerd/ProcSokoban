from IO.Utils import read_templates, print_and_write_grid
from LevelParser.Template import Template
from Generator.Generator import Generator

# Read all the key-templates adn wildcards from folder
key_template_list, wildcard_list = read_templates()
for count, kt in enumerate(key_template_list):
    key_template_list[count] = Template(name=kt["name"], lines=kt["lines"])
for count, wc in enumerate(wildcard_list):
    wildcard_list[count] = Template(name=wc["name"], lines=wc["lines"])

generator = Generator(key_templates=key_template_list, wildcards=wildcard_list, seed=123)
level = generator.get_level(size=[2, 2], ensureOuterWalls=False)

print("Final Iteration: ")
print_and_write_grid(level, "src/Levels/Test.lvl")