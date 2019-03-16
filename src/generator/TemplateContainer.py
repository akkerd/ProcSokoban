import copy
from Generator.Utils import Utils

class TemplateContainer:

    def __init__(self, template, rotation=0):
        self._template = template
        self._rotation = rotation

    def get_border(self, index):
        return self._template.borders[(index+self._rotation) % 4]

    def rotate(self):
        self._rotation += 1      

    def set_rotation(self, rotation):
        self._rotation = rotation % 4

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

