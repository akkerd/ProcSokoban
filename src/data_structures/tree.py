class Tree(object):

    class Node(object):
        def __init__(self, name, reference, parent, depth):
            self.descendents = []
            self.name = name
            self.reference = reference
            self.parent = parent
            self.depth = depth

    def __init__(self, root_id, root_reference):
        self.rootnode = Tree.Node(root_id, root_reference, None, 0)
        self.nodes[root_id] = self.rootnode
        self.depth = 0
        self.width = 0
        self.nodes = {}
        self.leaves = {}
        self.leaves[root_id] = self.rootnode

    def AddNode(self, parent_id, node_id, node_reference):
        # Null check
        if parent_id not in self.nodes.keys():
            print("Parent not found when adding node: ", node_id)
            raise Exception
        
        # Find parent
        parent = self.nodes[parent_id]      
        # Create Node
        newnode = Tree.Node(node_id, node_reference, parent, self.parent.depth+1)
        
        if(len(parent.descendents) is 0):
            # Remove parent from leaves
            del self.leaves[parent_id]
        
        parent.descendents.append(newnode)  # Add node to descendents
        self.nodes[node_id] = newnode       # Add to node dic

        if(newnode.depth > self.depth):
            self.depth = newnode.depth

    def GetNode(self, node_id):
        return self.nodes[node_id]

    def GetParentNode(self, node_id):
        return self.nodes[node_id].parent

    def UpdateWidth(self):
        self.width = len(self.leaves)
