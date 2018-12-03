from tkinter import *
import pickle
import os
from os import listdir
from os.path import isfile, join


class ElementaryAddition:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.var1, self.var2, self.relation = "", "", ""

        self.top.geometry('500x300+600+300')

        def callback(event):
            self.var1, self.relation, self.var2 = self.inactive_Entry.get(), self.var.get(), self.definite_Entry.get()

        self.definite = Label(top, text='Add a two letters that are either definite or inactive')
        self.definite.place(x=130, y=70)

        self.inactive_Entry = Entry(top)
        self.inactive_Entry.place(x=100, y=120)
        self.inactive_Entry.bind('<Return>', callback)
        self.definite_Entry = Entry(top)
        self.definite_Entry.place(x=300, y=120)
        self.definite_Entry.bind('<Return>', callback)

        self.var = StringVar(top)
        self.var.set("=")

        choices = ["=", "!="]
        self.option = OptionMenu(top, self.var, *choices)
        self.option.place(x=215, y=140)

        self.switchButton = Button(top, text='  add ', command=self.add)
        self.switchButton.place(x=238, y=240)

        self.res = Label(top, text='')
        self.res.place(x=150, y=200)

    def add(self):
        self.var1, self.relation, self.var2 = self.inactive_Entry.get(), self.var.get(), self.definite_Entry.get()
        self.top.destroy()

    def returnstr(self):
        return self.var1, self.var2, self.relation


class Substitution:
    def __init__(self, parent, node):
        top = self.top = Toplevel(parent)

        self.legal = False
        self.var1 = ""
        self.var2 = ""
        self.node = node

        self.top.geometry('500x300+600+300')
        self.myLabel = Label(top, text='Choose an inactive and a definite letter')
        self.myLabel.place(x=150, y=50)
        self.myLabel = Label(top, text='Alternatively choose an inactive and a definite letter')
        self.myLabel.place(x=150, y=50)

        self.definite = Label(top, text='replace this')
        self.definite.place(x=130, y=90)
        self.relation = Label(top, text='with')
        self.relation.place(x=230, y=90)
        self.definite = Label(top, text='this variable')
        self.definite.place(x=330, y=90)

        self.var1_Entry = Entry(top)
        self.var1_Entry.place(x=100, y=120)
        self.var2_Entry = Entry(top)
        self.var2_Entry.place(x=300, y=120)

        self.var = StringVar(top)
        self.var.set('Equalities')
        choices = [repr(e[0]) + " | " + repr(e[1]) for e in node.equal]
        if not choices:
            choices = ["No letter can be substituted"]

        self.option = OptionMenu(top, self.var, *choices)
        self.option.place(x=215, y=80)

        self.replace = Button(top, text='replace', command=self.replace)
        self.replace.place(x=225, y=160)

        self.res = Label(top, text='')
        self.res.place(x=150, y=200)

    def replace(self):
        self.var1, self.var2 = self.var1_Entry.get(), self.var2_Entry.get()
        self.top.destroy()

    def return_vars(self):
        return self.var1, self.var2


class Definition:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.inactive_var = ""

        self.top.geometry('500x300+600+300')

        self.definite = Label(top, text='Choose an inactive Letter')
        self.definite.place(x=190, y=70)
        self.definite = Label(top, text='It will only be activated if hypothesis is not admissible')
        self.definite.place(x=120, y=90)

        self.var1_Entry = Entry(top)
        self.var1_Entry.place(x=200, y=120)

        self.replace = Button(top, text='Set', command=self.replace)
        self.replace.place(x=230, y=160)

        self.res = Label(top, text='')
        self.res.place(x=150, y=200)

    def replace(self):
        self.inactive_var = self.var1_Entry.get()
        self.top.destroy()

    def return_var(self):
        return self.inactive_var


class Dual:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.inactive_var = ""

        self.top.geometry('600x300+600+300')

        self.definite = Label(top, text='Enter a Statement')
        self.definite.place(x=190, y=90)

        self.var1_Entry = Entry(top)
        self.var1_Entry.place(x=25, y=120, width=550)

        self.replace = Button(top, text='add', command=self.replace)
        self.replace.place(x=230, y=160)

        self.res = Label(top, text='')
        self.res.place(x=150, y=200)

    def replace(self):
        self.inactive_var = self.var1_Entry.get()
        self.top.destroy()

    def return_statement(self):
        return self.inactive_var


class Property:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.inactive_var = ""

        self.top.geometry('600x300+600+300')

        self.definite = Label(top, text='Enter an admissible Property')
        self.definite.place(x=190, y=20)

        self.definite = Label(top, text='First Enter the acronym, then the parameters everything seperated by commas')
        self.definite.place(x=100, y=60)

        self.definite = Label(top, text='Then a colon followed by the statement')
        self.definite.place(x=190, y=80)

        self.var1_Entry = Entry(top)
        self.var1_Entry.place(x=25, y=120, width=550)

        self.replace = Button(top, text='add', command=self.replace)
        self.replace.place(x=230, y=160)

        self.res = Label(top, text='')
        self.res.place(x=150, y=200)

    def replace(self):
        self.inactive_var = self.var1_Entry.get()
        self.top.destroy()

    def return_statement(self):
        return self.inactive_var

class Choice:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.inactive_var = ""

        self.top.geometry('600x500+600+300')
        self.included = [True, False, False, False, False, False, False]

        self.definite = Label(top, text='Choose 2 different indefinite letters and 5 definite letters')
        self.definite.place(x=180, y=20)

        self.definite = Label(top, text='indefinite letters')
        self.definite.place(x=250, y=50)

        self.definite = Label(top, text='definite letters')
        self.definite.place(x=250, y=130)

        self.indef1_Entry = Entry(top)
        self.indef1_Entry.place(x=200, y=70, width=90)
        self.indef2_Entry = Entry(top)
        self.indef2_Entry.place(x=300, y=70, width=90)

        self.def1_Entry = Entry(top)
        self.def1_Entry.place(x=50, y=150, width=90)
        self.def2_Entry = Entry(top)
        self.def2_Entry.place(x=150, y=150, width=90)
        self.def3_Entry = Entry(top)
        self.def3_Entry.place(x=250, y=150, width=90)
        self.def4_Entry = Entry(top)
        self.def4_Entry.place(x=350, y=150, width=90)
        self.def5_Entry = Entry(top)
        self.def5_Entry.place(x=450, y=150, width=90)

        self.node1 = Button(top, text='Node 1', command=self.button1, bg="DeepSkyBlue2")
        self.node1.place(x=50, y=200)
        self.node2 = Button(top, text='Node 2', command=self.button2)
        self.node2.place(x=50, y=230)
        self.node3 = Button(top, text='Node 3', command=self.button3)
        self.node3.place(x=50, y=260)
        self.node4 = Button(top, text='Node 4', command=self.button4)
        self.node4.place(x=50, y=290)
        self.node5 = Button(top, text='Node 5', command=self.button5)
        self.node5.place(x=50, y=320)
        self.node6 = Button(top, text='Node 6', command=self.button6)
        self.node6.place(x=50, y=350)
        self.node7 = Button(top, text='Node 7', command=self.button7)
        self.node7.place(x=50, y=380)

        self.text1 = Label(top, text='f = f')
        self.text1.place(x=190, y=200)
        self.text2 = Label(top, text='f(g) = f')
        self.text2.place(x=190, y=230)
        self.text3 = Label(top, text='{g(e) != g} f(e) != f')
        self.text3.place(x=190, y=260)
        self.text4 = Label(top, text='{g(e) != g} {e(n) != e} f(n) != f')
        self.text4.place(x=190, y=290)
        self.text5 = Label(top, text='{f(e) != f} f(f(e)) != f')
        self.text5.place(x=190, y=320)
        self.text6 = Label(top, text='{f(e) = f} [e(n) != e] {g(n) != g} h(e(n)) = h')
        self.text6.place(x=190, y=350)
        self.text7 = Label(top, text='{f(e) != f} Aef(e)')
        self.text7.place(x=190, y=380)



        self.res = Label(top, text='')
        self.res.place(x=150, y=200)

    def button1(self):
        if self.included[0]:
            if self.included[1]:
                self.node1.configure(bg="snow")
                self.included[0] = False
        else:
            self.node1.configure(bg="DeepSkyBlue2")
            self.included[0] = True

    def button2(self):
        if self.included[1]:
            if self.included[0]:
                self.node2.configure(bg="snow")
                self.included[1] = False
        else:
            self.node2.configure(bg="DeepSkyBlue2")
            self.included[1] = True

    def button3(self):
        if self.included[2]:
            self.node3.configure(bg="snow")
            self.included[2] = False
        else:
            self.node3.configure(bg="DeepSkyBlue2")
            self.included[2] = True

    def button4(self):
        if self.included[3]:
            self.node4.configure(bg="snow")
            self.included[3] = False
        else:
            self.node4.configure(bg="DeepSkyBlue2")
            self.included[3] = True

    def button5(self):
        if self.included[4]:
            self.node5.configure(bg="snow")
            self.included[4] = False
        else:
            self.node5.configure(bg="DeepSkyBlue2")
            self.included[4] = True

    def button6(self):
        if self.included[5]:
            self.node6.configure(bg="snow")
            self.included[5] = False
        else:
            self.node6.configure(bg="DeepSkyBlue2")
            self.included[5] = True

    def button7(self):
        if self.included[6]:
            self.node7.configure(bg="snow")
            self.included[6] = False
        else:
            self.node7.configure(bg="DeepSkyBlue2")
            self.included[6] = True

    def return_statement(self):
        return self.inactive_var


class SaveDialog:
    def __init__(self, parent, tree_info, cur_file):
        top = self.top = Toplevel(parent)

        self.top.geometry('300x300+600+400')
        self.filename = None
        self.myLabel = Label(top, text='Enter the name of the tree below')
        if cur_file != None:
            self.myLabel.config(text=cur_file)
        self.myLabel.pack()

        self.myEntryBox = Entry(top)
        self.myEntryBox.pack()

        self.mySubmitButton = Button(top, text='Save', command=self.send)
        self.mySubmitButton.pack()

        self.tikz = Button(top, text='Compile to tikz', command=self.tikz)
        self.tikz.pack()
        self.forest = Button(top, text='Compile to Forest Format', command=self.forest)
        self.forest.pack()
        self.qtree = Button(top, text='Compile to Qtree Format', command=self.qtree)
        self.qtree.pack()
        self.tree_info = tree_info

    def send(self):
        self.filename = self.myEntryBox.get()

        with open("TreeLibrary/" + self.filename + '.pickle', 'wb') as handle:
            pickle.dump(self.tree_info, handle, protocol=pickle.HIGHEST_PROTOCOL)

        self.top.destroy()

    def tikz(self):
        tikz = self.tree.Tex_Compile_Tikz()
        with open("result.txt", 'w') as result:
            result.write(tikz)

    def forest(self):
        forest = self.tree.Tex_Compile_Forest()
        with open("result.txt", 'w') as result:
            result.write(forest)

    def qtree(self):
        qtree = self.tree.Tex_Compile_Qtree()
        with open("result.txt", 'w') as result:
            result.write(qtree)

    def savereturn(self):
        return self.filename


class OpenDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.top.geometry('600x300+600+400')
        self.tree_info = None

        self.myLabel = Label(top, text='Choose a tree below')
        self.myLabel.pack()
        self.filename = "You have no saved trees"
        self.var = StringVar(top)
        self.var.set('Choose a tree')

        choices = [f[:-7] for f in listdir("TreeLibrary/") if isfile(join("TreeLibrary/", f))]
        if not choices:
            choices = ["You have no saved trees"]

        self.option = OptionMenu(top, self.var, *choices)
        self.option.pack(padx=10, pady=10)

        self.myEntryBox = Entry(top)
        self.myEntryBox.pack()

        self.mySubmitButton = Button(top, text='Open', command=self.open)
        self.mySubmitButton.pack()
        self.mySubmitButton = Button(top, text='Delete', command=self.delete)
        self.mySubmitButton.pack()

    def open(self):
        filename = self.var.get()
        if self.var.get() != "TreeLibrary/Choose a tree.pickle" and self.var.get() != "You have no saved trees":
            print("TreeLibrary/" + filename + ".pickle")
            with open("TreeLibrary/" + str(filename) + ".pickle", 'rb') as handle:
                tree_info = pickle.load(handle)
            self.tree_info = tree_info
        self.top.destroy()

    def delete(self):
        filename = self.var.get()
        os.remove("TreeLibrary/" + str(filename) + ".pickle")

    def returntree(self):
        return self.tree_info, self.var.get()


class _Import:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.imports = []

        self.top.geometry('1000x800+400+100')
        self._import = Button(top, text='Import', command=self._import)
        self._import.pack()
        self.T = Text(top, height=800, width=1000)
        self.T.pack()
        quote = """import Zero"""
        self.T.insert(END, quote)

    def _import(self):
        import_text = self.T.get("1.0", END)
        for line in import_text.splitlines():
            if line[:6] == "import":
                self.imports.append(line[7:])
        self.top.destroy()

    def return_inputs(self):
        return self.imports


class Help:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.top.geometry('1000x800+400+100')
        self.T = Text(top, height=800, width=1000)
        self.T.pack()
        quote = """
        Tree Theory:

        This Program is based around Christoph Thiele's "Definitions in Mathematics", a Mathematical Language
        with precise rules. Every rule is implemented, so that Proofs that can be entered must be True in the context of
        the axioms given in Christoph's Paper.

        <Link>

        On the right hand corner there are buttons, one for each rule. These can be used to expand a proof tree. If 
        an input does not precisely correspond to a rule, an Error message is displayed in the pink label field. 

        Leafs can be selected by double clicking on them, secondary nodes, required by some rules, can be selected by 
        clickingon them in the right order. Clicking on them again will remove them. 

        Trees can be saved and opened internally 
        with the Save Tree andOpen Tree button. In future Versions, saved trees will be able to be appended to a leaf 
        of the current tree. Furthermore trees can be compiled to latex code in three formats, at the moment the Forest 
        Format is recommended. 

        The remove functions work with the first secondary node.


        Also the Add Child and Edit Child Functions will soon be removed, these are for testing purposes. Inputs are not
        tested.

        Signs: {}: universal brackets, [] existential brackets, = equal, != inequal, () functional brackets

        Usage:


        Addition:
        To add anaddition press the  addition button, and a popup will open. Enter two variables 
        and choose the relation before pressing enter.

        Elementary Substitution:
        Pressing the elementary substitution button will open a popup. In it you can enter the variables that should be
         exchanged. You can also press on equalities, for a list of substitutable items. if a secondary node is selected
         its statement will be where variables are replaced.

        Dual Statement:
        If 2 secondary nodes are selected, they wil be checked for duality. if they are dual, the last node with two 
        children from the selected leaf will get a direct descendant, form with the statement of the branch not 
        producing a contradiction. 

        If 1 secondary node is selected, the selected leaf will be checked for contradiction with the selected secondary 
        node.

        If 0 secondary nodes are selected pressing on the Dual Statement button will open a popup. In it you can enter a statement as a string. This 
        statement wil be added as a child to the current leaf, along with the corresponding dual child.

        Definition:
        Select a leaf. Also select an ancestor with an existential statement to the leaf. If this is not done, the 
        program assumes, that the leaf is existential. Then press the definition button. If an inactive letter is 
        required, a popup will open requesting one.

        Deduction:
        If 2 secondary nodes are selected, the first should be a universal statement. the second should be the 
        hypothesis, or a modified hypothesis of the universal statement.

        If 1 secondary node is selected, the seleceted leaf will be assumed to be universal.

        """
        self.T.insert(END, quote)

