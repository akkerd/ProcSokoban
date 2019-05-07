import copy
from generator.utils import Utils
from level_parser.border import Border

class TemplateContainer:

    def __init__(self, template, rotation=0, flipped=False, complementary=None):
        self._template = template
        self._rotation = rotation
        self._flipped = flipped
        self._complementary = complementary

    def __hash__(self):
        lvl = self.get_level()
        for index, row in enumerate(lvl):
            lvl[index] = tuple(row)
        temp = frozenset(lvl)
        return hash(temp)

    def get_border(self, index):
        rot_idx = (index + self._rotation) % 4
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
    
    def needs_complementary(self):
        return self._complementary is None

    def get_complementary(self):
        temp = {}
        for key, value in self._complementary.items():
            index = (key + self._rotation) % 4
            temp[index] = value

