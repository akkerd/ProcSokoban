class Border:
    
    def __init__(self, line):
        self.Connections = [False] * len(line)
        self.BorderSize = len(line)
        self.MinimumConnectionSize = 0
        i = 0
        connectionCount = 0
        for char in line:
            if char is not "#":
                # Set this spot as available for connection
                self.Connections[i] = True
                
                # Update minimum connection size
                connectionCount += 1
                if connectionCount > self.MinimumConnectionSize:
                    self.MinimumConnectionSize = connectionCount
            else:
                connectionCount = 0
            i += 1

