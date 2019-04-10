class Border:
    
    def __init__(self, line):
        self.Connections = [False]*len(line)
        self.BorderSize = len(line)
        self.Line = line
        self.MinimumConnection = 0
        i = 0
        connection_size = 0
        for char in line:
            if char is not "+":
                # Set this spot as available for connection
                self.Connections[i] = True
                
                # Update minimum connection size
                connection_size += 1
                if connection_size > self.MinimumConnection:
                    self.MinimumConnection = connection_size
            else:
                connection_size = 0
            i += 1

    def connects(self, other):
        
        if self.BorderSize > other.BorderSize:
            big = self
            small = other
        else:
            big = other
            small = self
        if self.MinimumConnection is not 0 and other.MinimumConnection is not 0:
            if small.Line in big.Line:
                return True
        return False

        # if self.MinimumConnection == other.MinimumConnection \
        #     and self.MinimumConnection is not 0:
        #     i = 0
        #     for connection in self.Connections:
        #         if connection != other.Connections[i]:
        #             return False
        #         i += 1
        #     return True
        # return False
