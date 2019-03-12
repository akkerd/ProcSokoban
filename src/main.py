import glob
import os
import errno

from LevelParser.Template import Template
from Generator.Generator import Generator

# Read all the key-templates adn wildcards from folder
path = os.path.dirname(os.path.abspath(__file__)) + "\Templates\*"
print(path)
key_template_list = []
wildcard_list = []
files = glob.glob(path)
for name in files:
    try:
        if name[-2:] == "kt":
            key_template_list.append(Template(name=name, lines=open(name, "r").read().splitlines()))
        elif name[-2:] == "wc":
            wildcard_list.append(Template(name=name, lines=open(name, "r").read().splitlines()))            
    except IOError as exc:
        print(exc)
        if exc.errno != errno.EISDIR:
            raise
    print("Name: ", name)

# template_list.append(Template("src/Templates/test1.kt", debug=True))
# template_list.append(Template("src/Templates/test2.kt", debug=True))
# template_list.append(Template("src/Templates/test3.kt", debug=True))
# template_list.append(Template("src/Templates/test4.kt", debug=True))
# template_list.append(Template("src/Templates/test5.kt", debug=True))

generator = Generator(key_templates=key_template_list)
outGrid = generator.getlevel(size=[2, 2], surroundWalls=False)

WriteStream = open("src/Levels/Test.lvl", "w+")
for row in outGrid.values():
    print("Row by row: ", row)
    WriteStream.write(row+"\n")
WriteStream.close()