import time
import datetime
from generator.generator import Generator
from generator.utils import Utils
from ai.ai_manager import initiate_ai_solution_search
from inout.utils import IOUtils

# Measuring and logs
start_time = time.time()

# Algorithm Parameters:
rotation = True
flipping = False

# Read all the 4 rotated versions of each of the key-templates and wildcards
prototemplates = IOUtils.read_templates()

# Generation
generator = Generator(
    prototemplates=prototemplates,
    # seed=131742594536867100,
    doRotation=rotation,
    doFlipping=flipping,
)

level = generator.get_level(size=[6, 6], ensureOuterWalls=True)

# Ensure same number of box & goals
Utils.fit_box_goals(level)
Utils.close_non_connecting_links(level)

# AI
# initiate_ai_solution_search(level)

end_time = time.time()
elapsed_time = end_time - start_time
now = str(datetime.datetime.now())[:19].replace(" ", "_").replace(":","-")

print("Final Iteration: ")
IOUtils.print_and_write_grid(level, now) 

print("Running time: ", elapsed_time)
print("Seed was: ", generator.seed)