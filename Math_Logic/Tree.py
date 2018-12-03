

"""This is the base Tree class"""


class TreeNode:
    def __init__(self,  parent):
        self.parent = parent
        self.children = []

    def add_child(self, child, index=None):
        if index == "left":
            self.children.append(child)
            child.parent = self
        elif index == "middle":
            self.children.insert(1, child)
            child.parent = self
        else:
            self.children.insert(0, child)
            child.parent = self

    def is_leaf(self):
        # returns True iff node is a leaf
        return len(self.children) > 0

    def has_parent(self):
        #checks if node has a parent
        return not self.parent == None

    def get_depth(self):
        # returns the depth of the tree
        children = self.get_child_nodes()
        if len(children) == 0:
            return 1
        depths = []
        for child in children:
            depths.append(child.get_depth())
        return max(depths)+1

    def get_layerwidth(self, layer):
        # gets the width of a layer
        children = self.get_child_nodes()
        if layer == 1:
            return len(children)
        sum = 0
        for child in children:
            sum += child.get_layerwidth(layer-1)
        return sum

    def get_max_width(self):
        # gets the max width of a tree
        depth = self.get_depth()
        widths = [self.get_layerwidth(layer) for layer in range(1, depth)]
        if widths == []:
            return 1
        return max(widths)

    def get_child_nodes(self):
        # returns all children of the node
        return self.children

    def get_all_children(self):
        # get every descendant of the node
        nodes = [self]
        if len(self.children) == 0:
            return nodes
        else:
            for child in self.children:
                nodes += (child.get_all_children())
            return nodes

    def is_ancestor(self, other):
        # checks other node is ancestor of self
        if other == self:
            return True
        cur = self
        while cur.has_parent():
            cur = cur.parent
            if other == cur:
                return True
        return False