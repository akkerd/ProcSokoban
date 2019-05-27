import copy
import itertools
from generator.utils import Utils
from level_parser.border import Border

class TemplateContainer:
    CheckedTemplates = []

    def __init__(self, template, rotation=0, flipped=False):
        self._template = template
        self._rotation = rotation
        self._flipped = flipped
        self._index = template.Index
        self._complementary = template.Complementary
        self.corners = [(0, 0), (0, int(self._template.Ncols / 5)), (int(self._template.Nrows / 5), int(self._template.Ncols / 5)), (int(self._template.Nrows / 5), 0)]

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

    def get_rotation(self):
        return self._rotation

    def set_rotation(self, rotation):
        self._rotation = rotation % 4

    def flip(self):
        raise NotImplementedError
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
        return self._complementary is not None

    def get_complementary(self, rotate=True):
        comp = {}
        for comp_index, comp_template in self._complementary.items():
            index_diff = tuple(x - y for x, y in zip(self._index, comp_index))
            final_index = -1
            if index_diff == (1, 0):
                final_index = 0
            elif index_diff == (0, -1):
                final_index = 1
            elif index_diff == (-1, 0):
                final_index = 2
            elif index_diff == (0, 1):
                final_index = 3

            if final_index != -1:
                # Rotate if needed
                final_index = (final_index + self._rotation) % 4 if rotate else final_index
                # Assign
                comp[final_index] = TemplateContainer(template=comp_template, rotation=self._rotation, flipped=self._flipped)
        return comp
    
    def get_name(self):
        return self._template.Name

    def get_index(self):
        return self._index

    def fit_in_corner(self, corner, index):
        fits = False
        i = self.corners.index(index)
        if i == corner:
            if i == 0 and self.has_connections_at([1, 2], 1):
                fits = True
            elif i == 1 and self.has_connections_at([2, 3], 1):
                fits = True
            elif i == 2 and self.has_connections_at([0, 1], 1):
                fits = True
            elif i == 3 and self.has_connections_at([0, 3], 1):
                fits = True
        return fits

    def get_rotated_corner(self):
        rotated_index = None
        if self._index in self.corners:
            i = self.corners.index(self._index)
            rotated_index = self.corners[(i + self._rotation) % 4]
        return rotated_index

    def get_connections(self):
        return self._template.ConnectionCount

    def reset_check(self):
        TemplateContainer.CheckedTemplates = []
    
    def connects_at(self, conn_list):
        is_connection = [False] * (len(conn_list))
        for i, conn in enumerate(conn_list):
            if self.needs_complementary():
                is_connection[i] = self.connects_with(conn)
            else:
                is_connection[i] = self._template.is_connection_at(conn)

        return all(is_connection)

    def has_connections_at(self, conn_list, desired_conn):
        """
        Check if template has AT LEAST num_connections in 
        the given directions contained in conn_list
        """
        is_connection = [False] * (len(conn_list))
        for i, conn in enumerate(conn_list):
            rotated_conn = (conn + self._rotation) % 4
            if self.needs_complementary():
                is_connection[i] = self.connects_with(rotated_conn)
            else:
                is_connection[i] = self._template.is_connection_at(rotated_conn)
        num_real_conn = sum(1 for x in is_connection if x is True)

        return desired_conn >= num_real_conn

    def connects_with(self, conn):
        if self._template.is_connection_at(conn):
            return True
        elif self.get_index() in TemplateContainer.CheckedTemplates:
            return False
        
        TemplateContainer.CheckedTemplates.append(self.get_index())
        for comp_i, comp in self.get_complementary(rotate=False).items():
            if comp.connects_with(conn):
                return True
        
        return False


     