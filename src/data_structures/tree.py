class ModuleTree(object):

    class Node(object):
        def __init__(self, name, mod_positions, parent, depth):
            self.descendents = []
            self.name = name
            self.module_positions = mod_positions
            self.parent = parent
            self.depth = depth

    def __init__(self, start_id, start_reference, goal_id, goal_reference):
        self.startnode = ModuleTree.Node(start_id, start_reference, None, 0)
        self.goalnode = ModuleTree.Node(goal_id, goal_reference, None, 0)
        self.nodes = {}
        self.nodes[start_id] = [self.startnode]
        self.nodes[goal_id] = [self.goalnode]
        self.depth = 0
        self.width = 0
        self.leaves = {}
        self.leaves[start_id] = [self.startnode]
        self.leaves[goal_id] = [self.goalnode]

    def FindNode(self, node_id, node_pos):
        node = None
        node_possibilities = self.nodes[node_id]
        for node_possibility in node_possibilities:
            if node_pos in node_possibility.module_positions:
                node = node_possibility
                break
        return node

    def AddNode(self, parent_id, parent_pos, node_id, node_module_positions):
        # Null check
        if parent_id not in self.nodes.keys() or self.FindNode(parent_id, parent_pos) is None:
            print("Parent not found when adding node: ", node_id)
            raise Exception
        
        # Find parent
        parent = self.FindNode(parent_id, parent_pos)
        # Create Node
        newnode = Tree.Node(node_id, node_module_positions, parent, self.parent.depth + 1)
        
        if(len(parent.descendents) is 0):
            # Remove parent from leaves
            self.leaves[parent_id].remove(parent)
        
        # Add node to descendents
        parent.descendents.append(newnode)
        # Add to node dic
        if not self.nodes.get(node_id):
            self.nodes[node_id] = [newnode]
        else:
            self.nodes[node_id].append(newnode)

        if(newnode.depth > self.depth):
            self.depth = newnode.depth

    def GetNode(self, node_id, node_pos):
        node = self.FindNode(node_id, node_pos)
        # Null check
        if node is None:
            print("Node not found when getting node: ", node_id)
            raise Exception
        return node

    def GetParentNode(self, node_id, node_pos):
        node = self.GetNode(node_id, node_pos)
        return node.parent

    def UpdateWidth(self):
        self.width = len(self.leaves)
