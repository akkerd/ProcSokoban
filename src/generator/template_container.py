import copy
from generator.utils import Utils
from level_parser.border import Border

class TemplateContainer:

    def __init__(self, template, rotation=0, flipped=False):
        self._template = template
        self._rotation = rotation
        self._flipped = flipped

    def __hash__(self):
        lvl = self.get_level()
        for index, row in enumerate(lvl):
            lvl[index] = tuple(row)
        temp = frozenset(lvl)
        return hash(temp)

    def get_border(self, index):
        rot_idx = (index+self._rotation) % 4
        border = self._template.borders[rot_idx]
        if (index <= 1 and rot_idx >= 2) or (index >= 2 and rot_idx <= 1):
            border = copy.deepcopy(border)
            border.Connections.reverse()
        return border

    def rotate(self):
        self._rotation += 1      

    def set_rotation(self, rotation):
        self._rotation = rotation % 4

    def flip(self):
        self._flipped = True

    def get_level(self):
        level = copy.deepcopy(self._template.OriginalLevel)
        # Rotate
        for i in range(0, self._rotation):
            level = Utils.rotate(level)

        # print(level)
        return level

    # NOT NEEDED - KEEP JIC
    # def get_template(self):
    #     # Create new template
    #     template = copy.deepcopy(self._template)
    #     # Copy elements taking into account rotation
    #     template.OriginalLevel = self.get_level()
    #     template.Nrows = self.get_rows()
    #     template.Ncols = self.get_cols()

    #     tempBorder = self.get_border(0)
    #     for i in range(0, 4):
    #         template.borders[0] = self.get_border(i)
    #     template.borders[self._rotation] = tempBorder

    #     template.PossibleBoxes = self.get_boxes()
    #     template.PossibleGoals = self.get_goals()

    #     return template
    
    def get_rows(self):
        if self._rotation % 2 is 0:
            return self._template.Nrows
        else:
            return self._template.Ncols

    def get_cols(self):
        if self._rotation % 2 is 0:
            return self._template.Ncols
        else:
            return self._template.Nrows

