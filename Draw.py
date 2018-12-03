
def remove_children(self, tree):
    self.nodes.remove(tree)
    for child in tree.children:
        remove_children(self, child)

def draw_root(self, tree, x, y):
    self.view.Canvas.create_text(x, y, fill="darkblue", font="Times 15",
                                 text=tree.sentence, width=self.leaf_width*2)
    tree.position = (x, y)

def draw_tree(self, tree, x, y):

    def paint_tree(self, tree, x, y):
        if tree == None:
            return
        draw_root(self, tree, x, y)
        children = tree.get_child_nodes()
        width = tree.get_max_width()

        if len(children) == 1:
            child = children[0]
            paint_tree(self, child, x, y + self.edge_height)
            self.view.Canvas.create_line(x, y + self.font_height, x, y + self.edge_height - self.font_height)

        elif len(children) == 2:
            left_child = children[0]
            right_child = children[1]
            left_width = left_child.get_max_width()
            right_width = right_child.get_max_width()
            paint_tree(self, right_child, x - right_width * self.leaf_width, y + self.edge_height)
            paint_tree(self, left_child, x + left_width * self.leaf_width, y + self.edge_height)
            self.view.Canvas.create_line(x, y + self.font_height, x - right_width * self.leaf_width,
                                         y + self.edge_height - self.font_height)
            self.view.Canvas.create_line(x, y + self.font_height, x + left_width * self.leaf_width,
                                         y + self.edge_height - self.font_height)

        elif len(children) == 3:
            left_child = children[0]
            middle_child = children[1]
            right_child = children[2]
            paint_tree(self, middle_child, x, y + self.edge_height)
            left_width = left_child.get_max_width()
            middle_width = middle_child.get_max_width()
            right_width = right_child.get_max_width()
            paint_tree(self, left_child, x - (-left_width - middle_width) * self.leaf_width, y + self.edge_height)
            paint_tree(self, right_child, x + (-right_width - middle_width) * self.leaf_width, y + self.edge_height)
            self.view.Canvas.create_line(x, y + self.font_height, x, y + self.edge_height - self.font_height)
            self.view.Canvas.create_line(x, y + self.font_height, x - (-left_width - middle_width) * self.leaf_width,
                                         y + self.edge_height - self.font_height)
            self.view.Canvas.create_line(x, y + self.font_height, x + (-right_width - middle_width) * self.leaf_width,
                                         y + self.edge_height - self.font_height)
    paint_tree(self, tree, x, y)

    def paint_box(self, node, color, line_width, edge):
        # selected node
        width = self.leaf_width-edge
        height = self.font_height
        self.view.Canvas.create_line(node.position[0] - width, node.position[1] + height,
                                     node.position[0] + width, node.position[1] + height,
                                     width=line_width, fill=color)
        self.view.Canvas.create_line(node.position[0] - width, node.position[1] - height,
                                     node.position[0] + width, node.position[1] - height,
                                     width=line_width, fill=color)
        self.view.Canvas.create_line(node.position[0] - width, node.position[1] + height,
                                     node.position[0] - width, node.position[1] - height,
                                     width=line_width, fill=color)
        self.view.Canvas.create_line(node.position[0] + width, node.position[1] + height,
                                     node.position[0] + width, node.position[1] - height,
                                     width=line_width, fill=color)

    self.view.NodeEdit.delete(0, "end")
    self.view.NodeEdit.insert(0, self.selected_node.sentence)

    nodes = self.tree.get_all_children()
    for node in nodes:
        paint_box(self, node, "black", 1, 0)
    paint_box(self, self.selected_node, "red", 2, 0)
    for index, node in enumerate(self.secondary_nodes):
        paint_box(self, node, "blue", 2, 0)
        self.view.Canvas.create_text(node.position[0]+self.leaf_width-3, node.position[1]+self.font_height+7,
                                     fill="darkblue", font="Times 8", text=index+1, width=self.leaf_width*2)
