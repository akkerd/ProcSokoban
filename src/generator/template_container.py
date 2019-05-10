import copy
import itertools
from generator.utils import Utils
from level_parser.border import Border

class TemplateContainer:

    def __init__(self, template, rotation=0, flipped=False):
        self._template = template
        self._rotation = rotation
        self._flipped = flipped
        self._index = template.Index
        self._complementary = template.Complementary

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
        comp = {}
        for comp_index in self._complementary:
            index_diff = tuple(x - y for x, y in zip(self._index, comp_index))
            # rotated_comp_index = (comp_index[0] + self._rotation % 4, comp_index[1] + self._rotation % 4)
            if index_diff == (0, 1):
                comp[0 + self._rotation] = comp_index
            elif index_diff == (1, 0):
                comp[1 + self._rotation] = comp_index
            elif index_diff == (0, -1):
                comp[2 + self._rotation] = comp_index
            elif index_diff == (-1, 0):
                comp[3 + self._rotation] = comp_index
            else:
                print("Not considered case?")
        return comp
    
    def get_name(self):
        return self._template.name

    def get_index(self):
        return self._index