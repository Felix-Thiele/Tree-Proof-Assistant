import math
from tkinter import *

import Draw
import Math_Logic.MathTree as Tree
import PopUps


class View(Tk):
    def __init__(self, callback_add, callback_mouse, callback_second,
                 callback_remove, callback_width, save_open, Rules, help, callback_import):
        Tk.__init__(self)
        self.callback_add = callback_add
        self.callback_click = callback_mouse[0]
        self.callback_doubleclick = callback_mouse[2]
        self.callback_sec = callback_second
        self.callback_mousewheel = callback_mouse[1]
        [self.callback_removeNode, self.callback_removeSub] = callback_remove
        self.callback_width = callback_width
        [self.callback_save, self.callback_open] = save_open
        [self.callback_addition, self.callback_substitution, self.callback_dual_statement,
         self.callback_definition, self.callback_deduction, self.callback_property, self.callback_choice] = Rules
        self.callback_help = help
        self.callback_import = callback_import

        #Canvas
        self.Canvas = Canvas(master=self, width=300, height=300, scrollregion=(-10000, 0, 10000, 10000))

        # Fenster
        self.title("Tree GUI")
        self.geometry('1400x800+200+100')
        # Entries
        self.NodeTxt = Entry(master=self)
        self.NodeTxt.insert(0, '')
        self.NodeTxt.place(x=200, y=23, width=700)
        self.NodeEdit = Entry(master=self)
        self.NodeEdit.insert(0, '')
        self.NodeEdit.place(x=400, y=50, width=500)
        self.NodeIndex = Entry(master=self)
        self.NodeIndex.insert(0, 'right')
        self.NodeIndex.place(x=130, y=23, width=50)
        self.LeafWidth = Entry(master=self)
        self.LeafWidth.insert(0, '100')
        self.LeafWidth.place(x=130, y=110, width=50)

        # Button
        self.add = Button(master=self, text="Add Child", command=self.callback_add)
        self.add.place(x=20, y=20, width=100)
        self.second = Button(master=self, text="Clear Secondaries", command=self.callback_sec)
        self.second.place(x=20, y=50, width=100)
        self.remove = Button(master=self, text="Remove Node", command=self.callback_removeNode)
        self.remove.place(x=20, y=80, width=100)
        self.remove = Button(master=self, text="Remove Subtree", command=self.callback_removeSub)
        self.remove.place(x=120, y=80, width=100)
        self.leafw = Button(master=self, text="Change Width", command=self.callback_width)
        self.leafw.place(x=20, y=110, width=100)
        self.save = Button(master=self, text="Save Tree", command=self.callback_save)
        self.save.place(x=200, y=110, width=150)
        self.open = Button(master=self, text="Open Tree", command=self.callback_open)
        self.open.place(x=400, y=110, width=150)
        self.help = Button(master=self, text="Help", command=self.callback_help)
        self.help.place(x=20, y=170, width=150)
        self._import = Button(master=self, text="Import", command=self.callback_import)
        self._import.place(x=600, y=110, width=150)
        # syntax rules
        self.addition = Button(master=self, text="Addition", command=self.callback_addition)
        self.addition.place(x=950, y=20, width=150)
        self.elementary_substitution = Button(master=self, text="Elementary Substitution", command=self.callback_substitution)
        self.elementary_substitution.place(x=1150, y=80, width=150)
        self.dual_statement = Button(master=self, text="Dual Statement", command=self.callback_dual_statement)
        self.dual_statement.place(x=950, y=50, width=150)
        self.definition = Button(master=self, text="Definition", command=self.callback_definition)
        self.definition.place(x=1150, y=20, width=150)
        self.deduction = Button(master=self, text="Deduction", command=self.callback_deduction)
        self.deduction.place(x=1150, y=50, width=150)
        self.deduction = Button(master=self, text="Property", command=self.callback_property)
        self.deduction.place(x=950, y=80, width=150)
        self.deduction = Button(master=self, text="Choice", command=self.callback_choice)
        self.deduction.place(x=1150, y=110, width=150)


        # Label
        self.Error = Label(master=self, text='Error Messages are displayed here', bg="pink")
        self.Error.place(x=220, y=80)
        self.FileName = Label(master=self, text='This tree has no name')
        self.FileName.place(x=20, y=150)
        # Canvas Config
        self.vbar = Scrollbar(self, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.Canvas.yview)
        self.hbar = Scrollbar(self, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.Canvas.xview)
        self.Canvas.config(width=300, height=300)
        self.Canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.Canvas.pack(side=LEFT, expand=True, fill=BOTH)

        # mouse
        def key(event):
            print("pressed", repr(event.char))

        self.Canvas.bind("<Key>", key)
        self.Canvas.bind_all("<MouseWheel>", self.callback_mousewheel)
        self.Canvas.bind("<Button-1>", self.callback_click)
        self.Canvas.bind('<Double-Button-1>', self.callback_doubleclick)

# controller
class Controller(object):
    def __init__(self):
        self.filename = None
        self.edge_height = 90
        self.font_height = 20
        self.leaf_width = 100
        self.view = View(self.add_child, [self.click, self.mousewheel, self.doubleclick], self.second_choice,
                         [self.removeNode, self.removeSub],
                         self.width, [self.save, self.open],
                         [self.addition, self.substitution, self.dual_statement, self.definition,
                          self.deduction, self.property, self.choice], self.help, self._import)
        self.tree = Tree.MathTree(None, "a=a", (0, 0))
        self.nodes = [self.tree]
        self.selected_node = self.tree
        self.secondary_nodes = []
        self.edit_node = 0
        self.y = 10
        self.draw_tree()
        self.view.mainloop()

    def draw_tree(self):
        self.view.Canvas.delete("all")
        self.nodes = self.tree.get_all_children()
        Draw.draw_tree(self, self.tree, 600, 200)

    # Math Logic Buttons:
    def addition(self):
        input_dialog = PopUps.ElementaryAddition(self.view)
        self.view.wait_window(input_dialog.top)
        var1, var2, relation = input_dialog.returnstr()
        res = self.selected_node.addition(var1, var2, relation)
        self.view.Error.config(text=res[1])
        if res[0]:
            self.nodes.append(res[2])
            self.selected_node = res[2]
        self.draw_tree()

    def substitution(self):
        input_dialog = PopUps.Substitution(self.view, self.selected_node)
        self.view.wait_window(input_dialog.top)
        var1, var2 = input_dialog.return_vars()
        if len(self.secondary_nodes) == 0:
            res = self.selected_node.elementary_substitution(self.selected_node, var1, var2)
        else:
            res = self.selected_node.elementary_substitution(self.secondary_nodes[0], var1, var2)
        self.view.Error.config(text=res[1])
        if res[0]:
            self.nodes.append(res[2])
            self.selected_node = res[2]
        self.draw_tree()

    def dual_statement(self):
        if len(self.secondary_nodes) != 0:
            if len(self.secondary_nodes) == 1:
                first = self.selected_node
                second = self.secondary_nodes[0]
            elif len(self.secondary_nodes) == 2:
                first = self.secondary_nodes[0]
                second = self.secondary_nodes[1]
            else:
                self.view.Error.config(text="more than two secondaries selected")
                return
            if first.is_ancestor(second) or second.is_ancestor(first):
                res = self.selected_node.contradiction(first, second)
            else:
                res = first.twin_agreement(second)
            if res[0]:
                self.view.Error.config(text=res[1])
        else:
            input_dialog = PopUps.Dual(self.view)
            self.view.wait_window(input_dialog.top)
            statement = input_dialog.return_statement()
            res = self.selected_node.dual_statement(statement)
            if res[0]:
                self.nodes.append(res[2])
                self.selected_node = res[2]
                self.nodes.append(res[3])
            self.view.Error.config(text=res[1])
        self.draw_tree()

    def definition(self):
        if len(self.secondary_nodes) == 1:
            second_node = self.secondary_nodes[0]
        elif len(self.secondary_nodes) == 0:
            second_node = self.selected_node
        else:
            self.view.Error.config(text="More than one secondary node selected")
            return
        if second_node:
            input_dialog = PopUps.Definition(self.view)
            self.view.wait_window(input_dialog.top)
            var = input_dialog.return_var()
            res = self.selected_node.definition(second_node, var)
            self.view.Error.config(text=res[1])
            if res[0]:
                self.nodes.append(res[2])
                self.selected_node = res[3]
                self.nodes.append(res[3])
        else:
            self.view.Error.config(text="No second node selected")
        self.draw_tree()

    def deduction(self):
        if len(self.secondary_nodes) == 2:
            second_node = self.secondary_nodes[0]
            third_node = self.secondary_nodes[1]
        elif len(self.secondary_nodes) == 1:
            second_node = self.selected_node
            third_node = self.secondary_nodes[0]
        else:
            self.view.Error.config(text="More than two nodes selected")
            return
        res = self.selected_node.Deduction(second_node, third_node)
        self.view.Error.config(text=res[1])
        if res[0]:
            self.nodes.append(res[2])
            self.selected_node = res[2]
        self.draw_tree()

    def property(self):
        if len(self.secondary_nodes) == 0:
            input_dialog = PopUps.Property(self.view)
            self.view.wait_window(input_dialog.top)
            prop_str = input_dialog.return_statement()
            res = self.selected_node.property_addition(prop_str)
            self.view.Error.config(text=res[1])
            if res[0]:
                self.nodes.append(res[2])
                self.selected_node = res[2]
        elif len(self.secondary_nodes) == 1:
            res = self.selected_node.apply_property(self.secondary_nodes[0], self.selected_node)
            if res[0]:
                self.nodes.append(res[2])
                self.selected_node = res[2]
        self.draw_tree()

    def choice(self):
        if len(self.secondary_nodes) > 0:
            node = self.secondary_nodes[0]
        else:
            node = self.selected_node
        input_dialog = PopUps.Choice(self.view)
        self.view.wait_window(input_dialog.top)
        info = input_dialog.return_info()
        res = self.selected_node.choice(node, info[0], info[1])
        if res[0]:
            self.nodes += res[2]
            self.selected_node = res[3]
        self.view.Error.config(text=res[1])
        self.draw_tree()


    def add_child(self):
        if self.view.NodeTxt.get() == "":
            self.view.Error.config(text="A Leaf can not have an empty statement")
            return
        child = Tree.MathTree(self.selected_node, self.view.NodeTxt.get(), (0, 0), True)
        res = self.selected_node.add_child(child, index=self.view.NodeIndex.get())

        if res == None:
            self.nodes.append(child)
            self.view.NodeTxt.delete(0, "end")
            self.draw_tree()
        elif res == "maxchilds":
            self.view.Error.config(text="A Leaf can only have 3 children")

    def removeSub(self):
        if self.secondary_nodes[0] is not None:
            self.secondary_nodes[0].parent.children.remove(self.secondary_nodes[0])
            self.secondary_nodes[0] = self.secondary_nodes[0].parent
        self.draw_tree()

    def removeNode(self):
        if self.secondary_nodes[0].parent is not None:
            if len(self.secondary_nodes[0].parent.children) + len(self.secondary_nodes[0].children) <= 4:
                self.secondary_nodes[0].parent.children.remove(self.secondary_nodes[0])
                for child in self.secondary_nodes[0].children:
                    child.parent = self.secondary_nodes[0].parent
                    self.secondary_nodes[0].parent.children.append(child)
            else:
                self.view.Error.config(text="There are more than 4 children")
            self.secondary_nodes[0] = self.secondary_nodes[0].parent
        self.draw_tree()

    def _import(self):
        input_dialog = PopUps._Import(self.view)
        self.view.wait_window(input_dialog.top)
        imports = input_dialog.return_inputs()
        print(imports)

    def click(self, event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        best_node = self.selected_node
        small_dist = 9999999
        for node in self.nodes:
            if math.sqrt((node.position[0]-x)**2+(node.position[1]-y)**2) < small_dist:
                best_node = node
                small_dist = math.sqrt((node.position[0]-x)**2+(node.position[1]-y)**2)
        if best_node in self.secondary_nodes:
            self.secondary_nodes.remove(best_node)
        else:
            if best_node != self.selected_node:
                self.secondary_nodes.append(best_node)
        self.draw_tree()

    def doubleclick(self, event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        best_node = self.selected_node
        small_dist = 9999999
        for node in self.nodes:
            if math.sqrt((node.position[0]-x)**2+(node.position[1]-y)**2) < small_dist:
                best_node = node
                small_dist = math.sqrt((node.position[0]-x)**2+(node.position[1]-y)**2)
        if len(best_node.children) == 0:
            self.selected_node = best_node
            if best_node in self.secondary_nodes:
                self.secondary_nodes.remove(best_node)
        self.draw_tree()

    def second_choice(self):
        self.secondary_nodes = []
        self.draw_tree()



    def mousewheel(self, event):
        self.view.Canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def help(self):
        input_dialog = PopUps.Help(self.view)
        self.view.wait_window(input_dialog.top)

    def width(self):
        try:
            self.leaf_width = int(self.view.LeafWidth.get())
        except:
            self.view.Error.config(text="Leaf Width m ust be an Int")
        print("The Slected Node has folowing letter flavours: ")
        print("contained")
        print(self.selected_node.let_contained)
        print("active")
        print(self.selected_node.let_active)
        print("adjective")
        print(self.selected_node.let_adjective)
        print("definite")
        print(self.selected_node.let_definite)
        print("equal")
        print(self.selected_node.equal)
        self.draw_tree()

    def save(self):
        print(self.tree)
        input_dialog = PopUps.SaveDialog(self.view, [self.tree, self.selected_node, self.secondary_nodes, self.nodes],
                                         self.filename)
        self.view.wait_window(input_dialog.top)
        res = input_dialog.savereturn()
        if res:
            self.view.FileName.config(text="Filename : " + res)

    def open(self):
        input_dialog = PopUps.OpenDialog(self.view)
        self.view.wait_window(input_dialog.top)
        tree = input_dialog.returntree()
        if tree != None:
            self.tree = tree[0][0]
            self.selected_node = tree[0][1]
            self.secondary_nodes = tree[0][2]
            self.nodes = tree[0][3]
            self.view.FileName.config(text="Filename : " + tree[1])
            self.filename = tree[1]
        self.draw_tree()


