from src.LevelParser.Template import Template
from src.generator.Generator import Generator

# Read all the templates
# mytemplate = Template("../Templates/Simplest.txt", debug=True)
template_list = []
template_list.append( Template("../Templates/temp1.txt", debug=True) )
template_list.append( Template("../Templates/temp2.txt", debug=True) )
template_list.append( Template("../Templates/temp3.txt", debug=True) )
template_list.append( Template("../Templates/temp4.txt", debug=True) )

generator = Generator(key_templates=template_list)
outGrid = generator.getlevel(size=[2,2], surroundWalls=False)

WriteStream = open("../Levels/Test.txt", "w+")
for row in outGrid.values():
    print("Row by row: ", row)
    WriteStream.write(row+"\n")
WriteStream.close()