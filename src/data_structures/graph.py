class ModuleGraph(object):

    class Node(object):
        def __init__(self, name, mod_positions, connections):
            self.name = name
            self.module_positions = mod_positions
            self.connections = connections

    def __init__(self, start_id, start_reference, goal_id, goal_reference):
        self.startnode = ModuleGraph.Node(start_id, start_reference, [])
        self.goalnode = ModuleGraph.Node(goal_id, goal_reference, [])
        self.nodes = {}
        self.nodes[start_id] = self.startnode
        self.nodes[goal_id] = self.goalnode
        self.CheckedNodes = set()

    def AddNode(self, node_id, node_reference, connections):
        # Null check
        for conn in list(connections):
            if conn not in self.nodes.keys():
                print("Connection not found when adding node: ", node_id)
                raise Exception
            else:
                self.nodes[conn].connections.append(node_id)
            
        # Create Node
        newnode = ModuleGraph.Node(node_id, node_reference, connections)
        # Add to node dic
        self.nodes[node_id] = newnode

    def GetNode(self, node_id):
        return self.nodes[node_id]

    def GetParentNode(self, node_id):
        return self.nodes[node_id].parent

    def IsCriticalPath(self):
        self.CheckedNodes = set()
        return self.Explore(self.startnode.name, self.goalnode)
    
    def Explore(self, node_id, desired_node):
        if node_id in self.CheckedNodes:
            return False
        self.CheckedNodes.add(node_id)
        if node_id in desired_node.connections:
            return True
        else:
            found = False
            for conn in self.GetNode(node_id).connections:
                if self.Explore(conn, desired_node):
                    found = True
                    break
        return found

