from generator.generator import Generator
from generator.utils import Utils
from ai.ai_manager import initiate_ai_solution_search
from inout.utils import IOUtils

# Algorithm Parameters:
rotation = False
flipping = False

# Read all the 4 rotated versions of each of the key-templates and wildcards
prototemplates = IOUtils.read_templates()

# Generation
generator = Generator(
    prototemplates=prototemplates,
    # seed=127,
    doRotation=rotation,
    doFlipping=flipping,
)

level = generator.get_level(size=[5, 5], ensureOuterWalls=True)

# Ensure same number of box & goals
Utils.fit_box_goals(level)

# AI
# initiate_ai_solution_search(level)

print("Final Iteration: ")
IOUtils.print_and_write_grid(level, "Test") 