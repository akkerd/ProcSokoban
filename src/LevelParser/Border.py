class Border:
    
    def __init__(self, line):
        self.Connections = line
        self.BorderSize = len(line)
        self.MinimumConnectionSize = 0
        i = 0
        connection_size = 0
        for char in line:
            if char is not "#":
                # Set this spot as available for connection
                # self.Connections[i] = True
                
                # Update minimum connection size
                connection_size += 1
                if connection_size > self.MinimumConnectionSize:
                    self.MinimumConnectionSize = connection_size
            else:
                connection_size = 0
            i += 1

    def connects(self, other):
        if self.BorderSize == other.BorderSize:
            if self.MinimumConnectionSize == other.MinimumConnectionSize:
                if self.Connections == other.Connections:
                    return True
                # i = 0
                # for connection in self.Connections:
                #     if connection != other.Connections[i]:
                #         return False
                #     i += 1
        return False
