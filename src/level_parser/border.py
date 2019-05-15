import math

class Border:
    
    def __init__(self, line):
        self.Connections = [False] * math.floor(len(line) / 5)
        self.IsConnection = False

        self.BorderSize = len(line)
        self.Line = line

        # Check that is not a fill-in line
        if not all(elem == ' ' for elem in line):
            for count, char in enumerate(line):
                i = (count-2) % 5
                if i == 0:
                    if char == '/':
                        # Set this spot as available for connection
                        self.Connections[max(0, math.floor(count / 5))] = True
                        self.IsConnection = True

    def __eq__(self, other):
        """Overrides the default implementation"""
        if not self.is_connection() or not other.is_connection():
            return False
        if self.BorderSize > other.BorderSize:
            big = self
            small = other
        else:
            big = other
            small = self

        for i in range(0, len(self.Connections)-len(other.Connections)+1):
            match = 0
            for j, elem in enumerate(small.Connections):
                if elem != big.Connections[i+j]:
                    match = 0
                    break
                else:
                    match += 1
                    if match == len(small.Connections):
                        return True
        return False
        
    def is_connection(self):
        return self.IsConnection
        

        # if self.MinimumConnection == other.MinimumConnection \
        #     and self.MinimumConnection is not 0:
        #     i = 0
        #     for connection in self.Connections:
        #         if connection != other.Connections[i]:
        #             return False
        #         i += 1
        #     return True
        # return False
