from tkinter import *
from tkinter import messagebox
import pickle
import os
import sqlite3


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

        self.top.geometry('750x550+500+200')
        self.included = [True, False, False, False, False, False, False, False, False, False, False]
        self.variables = []

        self.description = Label(top, text='Choose 2 different indefinite letters and 6 definite letters')
        self.description.place(x=180, y=20)

        self.inactive_label = Label(top, text='inactive letters')
        self.inactive_label.place(x=250, y=50)

        self.definite_label = Label(top, text='definite letters')
        self.definite_label.place(x=250, y=100)

        self.inactive1_Entry = Entry(top)
        self.inactive1_Entry.place(x=250, y=70, width=90)

        self.def1_Entry = Entry(top)
        self.def1_Entry.place(x=10, y=120, width=90)
        self.def2_Entry = Entry(top)
        self.def2_Entry.place(x=110, y=120, width=90)
        self.def3_Entry = Entry(top)
        self.def3_Entry.place(x=210, y=120, width=90)
        self.def4_Entry = Entry(top)
        self.def4_Entry.place(x=310, y=120, width=90)
        self.def5_Entry = Entry(top)
        self.def5_Entry.place(x=410, y=120, width=90)
        self.def6_Entry = Entry(top)
        self.def6_Entry.place(x=510, y=120, width=90)

        self.node1 = Button(top, text='Node 1', bg="DeepSkyBlue2")
        self.node1.place(x=50, y=170)
        self.node2 = Button(top, text='Node 2', command=lambda: self.button(0))
        self.node2.place(x=50, y=200)
        self.node3 = Button(top, text='Node 3', command=lambda: self.button(1))
        self.node3.place(x=50, y=230)
        self.node4 = Button(top, text='Node 4', command=lambda: self.button(2))
        self.node4.place(x=50, y=260)
        self.node5 = Button(top, text='Node 5', command=lambda: self.button(3))
        self.node5.place(x=50, y=290)
        self.node6 = Button(top, text='Node 6', command=lambda: self.button(4))
        self.node6.place(x=50, y=320)
        self.node7 = Button(top, text='Node 7', command=lambda: self.button(5))
        self.node7.place(x=50, y=350)
        self.node8 = Button(top, text='Node 8', command=lambda: self.button(6))
        self.node8.place(x=50, y=380)
        self.node9 = Button(top, text='Node 9', command=lambda: self.button(7))
        self.node9.place(x=50, y=410)
        self.node10 = Button(top, text='Node 10', command=lambda: self.button(8))
        self.node10.place(x=50, y=440)
        self.node11 = Button(top, text='Node 11', command=lambda: self.button(9))
        self.node11.place(x=50, y=470)

        self.text1 = Label(top, text='inactive = inactive')
        self.text1.place(x=190, y=170)
        self.text2 = Label(top, text='{inactive(indef1) != inactive} mod_anc_conc')
        self.text2.place(x=190, y=200)
        self.text3 = Label(top, text='{inactive(indef1) != inactive} mod_anc_subconc')
        self.text3.place(x=190, y=230)
        self.text4 = Label(top, text='{inactive(indef1) != inactive} anc_hyp')
        self.text4.place(x=190, y=260)
        self.text5 = Label(top, text='inactive(indef1) != inactive')
        self.text5.place(x=190, y=290)
        self.text6 = Label(top, text='{def1(indef1) != def1}inactive(indef1) != inactive')
        self.text6.place(x=190, y=320)
        self.text7 = Label(top, text='{def3(indef1) != def3}{indef1(indef2) != indef1}inactive(indef2) != inactive')
        self.text7.place(x=190, y=350)
        self.text8 = Label(top, text='{inactive(indef1) != inactive} inactive(indef1)(inactive) != inactive(indef1)')
        self.text8.place(x=190, y=380)
        self.text9 = Label(top, text='{inactive(indef1) != inactive}[indef1(indef2) != indef1]{def4(indef2) != def4}def5(indef1(indef2))!= def5')
        self.text9.place(x=190, y=410)
        self.text10 = Label(top, text='{anc_hyp}inactive(indef1) != inactive')
        self.text10.place(x=190, y=440)
        self.text11 = Label(top, text='anc.replace(indef2, inactive(indef1))')
        self.text11.place(x=190, y=470)

        self.done = Button(top, text='add', command=self.done)
        self.done.place(x=150, y=500)

    def button(self, nr):
        node = [self.node2, self.node3, self.node4, self.node5, self.node6,
                    self.node7, self.node8, self.node9, self.node10, self.node11][nr]
        if self.included[nr+1]:
            node.configure(bg="snow")
            self.included[nr+1] = False
        else:
            node.configure(bg="DeepSkyBlue2")
            self.included[nr+1] = True


    def done(self):
        self.variables = [self.inactive1_Entry.get(), self.def1_Entry.get(), self.def2_Entry.get(), self.def3_Entry.get(),
                          self.def4_Entry.get(), self.def5_Entry.get(), self.def6_Entry.get()]
        self.top.destroy()

    def return_info(self):
        return self.variables, self.included


class SaveDialog:
    def __init__(self, parent, tree_info, cur_file):
        top = self.top = Toplevel(parent)

        self.top.geometry('300x300+600+400')
        self.filename = ""
        self.myLabel = Label(top, text='Enter the name of the tree below')
        if cur_file != None:
            self.myLabel.config(text=cur_file)
        self.myLabel.pack()

        #sql
        self.conn = sqlite3.connect('TreeTheoreeData.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS trees (name text, tree text)')

        self.filenameentry = Entry(top)
        self.filenameentry.pack()

        self.mySubmitButton = Button(top, text='Save', command=self.save)
        self.mySubmitButton.pack()

        self.tikz = Button(top, text='Compile to tikz', command=self.tikz)
        self.tikz.pack()
        self.forest = Button(top, text='Compile to Forest Format', command=self.forest)
        self.forest.pack()
        self.qtree = Button(top, text='Compile to Qtree Format', command=self.qtree)
        self.qtree.pack()
        self.tree = tree_info

    def save(self):
        self.filename = self.filenameentry.get()
        if self.filename == "" or self.filename == "enter a name":
            self.filenameentry.insert(0, "enter a name")
        else:
            self.c.execute('SELECT tree FROM trees WHERE name = ?', (self.filename,))
            res = self.c.fetchall()
            if res == []:
                txt = pickle.dumps(self.tree)
                self.c.execute("INSERT INTO trees VALUES (?, ?)", (self.filename, txt))
                self.conn.commit()
                self.c.close()
                self.conn.close()
            else:
                result = messagebox.askokcancel("Python", "Would you like to replace this file?")
                if result:
                    self.c.execute("DELETE FROM trees WHERE name=?", (self.filename,))
                    self.conn.commit()
                    txt = pickle.dumps(self.tree)
                    self.c.execute("INSERT INTO trees VALUES (?, ?)", (self.filename, txt))
                    self.conn.commit()
                    self.c.close()
                    self.conn.close()
                self.top.destroy()


    def tikz(self):
        tikz = self.tree[0].Tex_Compile_Tikz()
        with open("result.txt", 'w') as result:
            result.write(tikz)

    def forest(self):
        forest = self.tree[0].Tex_Compile_Forest()
        with open("result.txt", 'w') as result:
            result.write(forest)

    def qtree(self):
        qtree = self.tree[0].Tex_Compile_Qtree()
        with open("result.txt", 'w') as result:
            result.write(qtree)

    def savereturn(self):
        return self.filename


class OpenDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.top.geometry('600x300+600+400')
        self.tree = None

        # sql
        self.conn = sqlite3.connect('TreeTheoreeData.db')
        self.c = self.conn.cursor()

        self.myLabel = Label(top, text='Choose a tree below')
        self.myLabel.pack()
        self.filename = ""
        self.var = StringVar(top)
        self.var.set('Choose a tree')

        self.c.execute('SELECT name FROM trees')
        choices = self.c.fetchall()
        if not choices:
            choices = ["You have no saved trees"]

        self.option = OptionMenu(top, self.var, command=self.update, *choices)
        self.option.pack(padx=10, pady=10)

        self.filenameentry = Entry(top)
        self.filenameentry.pack()

        self.mySubmitButton = Button(top, text='Open', command=self.open)
        self.mySubmitButton.pack()
        self.mySubmitButton = Button(top, text='Delete', command=self.delete)
        self.mySubmitButton.pack()

    def open(self):
        self.filename = self.filenameentry.get()
        self.c.execute('SELECT tree FROM trees WHERE name = ?', (self.filename,))
        self.tree = self.c.fetchall()
        self.c.close()
        self.conn.close()
        self.top.destroy()

    def delete(self):
        self.filename = self.filenameentry.get()
        self.c.execute("DELETE FROM trees WHERE name=?", (self.filename,))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.top.destroy()

    def update(self, pick):
        self.filenameentry.insert(0, pick)

    def returntree(self):
        return pickle.loads(self.tree[0][0]), self.filename


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


class Tutorial:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.top.geometry('1000x800+400+100')
        self.T = Text(top, height=800, width=1000)
        self.T.pack()
        quote = """
        From my own experience, i know that learning how to maneuver an assisted theorem prover, or any program for that
        matter, can be quite a daunting prospect. So in this short tutorial i will go through the mechanics of this 
        program, giving click to click instructions on how to build one of the sample trees from the paper. 
         
        First lets add two dual statements. Click on the "Dual Statement" button. A window will pop up, asking you to 
        enter a Statement. Enter "{e=e}[n=n]e!=n" and click add. This will append two children two the root.
        
        Next lets apply the definition rule. Double click on the existential child, to change the current leaf node and 
        hit the "Definition" button. This wil open up a dialog, asking you to enter an inactive letter. Enter the letter
        "x" and click on set. Now a node and a sub-node will get added to the existential child of the root.
        
        Now lets add a new variable "y". To do this click on the "Addition" button. Type "x" into the left entry, and 
        "y" into the right entry. Click on the equality sign, and pick the inequality sign. Finally hit add.
        
        Slightly modify the step above, to add a node with "y=y".
        
        Now can apply a deduction. Single click on the node with the statement "{n=n}x=n". You have now selected a 
        secondary node. Now press on deduction. The node "x=y" should be added.
        Notice how all secondary nodes turn blue. If you want to deselect all secondary nodes hit
        clear secondaries. 
        
        But now we have a contradiction, since we have "x=y" and "x != y" in the same ancestry line. Deselect all 
        secondaries and select "x!=y" as your secondary node. Click on "Dual Statement". Now the dual statement of the 
        last dual fork gets added in the middle of that nodes parent. We have now proved "{e=e}[n=n]e!=n" successfully!!
        """
        self.T.insert(END, quote)

