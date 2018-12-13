from Math_Logic.Tree import TreeNode
from Math_Logic.Statement import Statement
from Math_Logic.Property import Property
from Math_Logic.Term import Term
from Math_Logic import ParseStr
import copy


"""
MathTree is the main MathLogic class. Each node consists of either one statement or one property. Also for each node the
contained active adjective etc letters are saved in a sql table.
"""


class MathTree(TreeNode):

    def __init__(self, parent, sentence, position=(0, 0)):
        super().__init__(parent)

        # a sentence is either a property or a statement
        self.sentence = sentence

        self.let_contained = []
        self.let_active = []
        self.let_adjective = []
        self.let_definite = []
        self.equal = []
        self.abbreviations = {}
        self.type = None
        if self.sentence.__class__.__name__ == "str":
            self.sentence = Statement(self.sentence)
        if self.sentence.__class__.__name__ == "Statement":
            self.set_up_statement()
            self.type = "statement"
        elif self.sentence.__class__.__name__=="Property":
            self.set_up_property()
            self.type = "property"

    def set_up_statement(self):
        self.let_contained = self.sentence.get_letters()
        if self.parent is not None:
            self.let_definite = self.parent.let_definite
            self.let_adjective = self.parent.let_adjective
            self.let_active = self.parent.let_active+self.parent.let_contained
            self.equal = self.parent.equal
            self.abbreviations = self.parent.abbreviations
        # definite
        if not self.sentence.presumptions:
            for letter in self.sentence.get_letters():
                if letter not in self.let_adjective:
                    self.let_definite.append(letter)
        # elementary equal
        if self.sentence.is_equality():
            self.equal.append((self.sentence.parameters[0], self.sentence.parameters[1]))

    def set_up_property(self):
        if self.parent is not None:
            self.let_definite = self.parent.let_definite
            self.let_adjective = self.parent.let_adjective
            self.let_active = self.parent.let_active+self.parent.let_contained
            self.equal = self.parent.equal
            self.abbreviations = self.parent.abbreviations
        # adjective
        self.let_adjective.append(self.sentence.contraction.acronym.char)
        if self.sentence.contraction.acronym not in self.abbreviations:
            self.abbreviations[self.sentence.contraction.acronym] = self.sentence
        self.let_adjective = list(set(self.let_adjective))


    # Addition Rule 2.2 and Rule 4.3


    def addition(self, var1, var2, relation):
        check = self.check_addition(var1, var2, relation)
        if check[0]:
            childstatement = Statement(var1 + relation + var2)
            child = MathTree(self, childstatement)
            self.add_child(child)
            return True, "Elementary Addition successful", child
        else:
            return False, check[1]

    def check_addition(self, var1, var2, relation):
        var1, var2 = Term(var1), Term(var2)
        letters1 = var1.get_letters()
        letters2 = var2.get_letters()
        # functional term
        if var1.is_functional() and var2.is_functional():
            return False, "cant add two functional terms"
        if var1.is_functional():
            if var2 not in self.let_active:
                for let in letters1:
                    if let not in self.let_definite:
                        return False, "letter is not definite"
                return True, "possible elementary addition"
        if var2.is_functional():
            if var1 not in self.let_active:
                for let in letters2:
                    if let not in self.let_definite:
                        return False, "letter is not definite"
                return True, "possible elementary addition"
        # elementary Term
        if (var1 not in self.let_active and var2 in self.let_definite) or (
                var2 not in self.let_active and var1 in self.let_definite):
            return True, "possible elementary addition"
        if (var1 not in self.let_active and var2 not in self.let_active) or (
                var1 in self.let_definite and var2 in self.let_definite):
            if var1 == var2 and relation == "=":
                return True, "possible elementary addition"
            return False, "If both letter are of the same flavour, the equality must be reflexive"
        return False, "Both letters have to either be inactive or indefinite"


    # Elementary Substitution Rule 2.3


    def elementary_substitution(self, node, var1, var2):
        if self.type == "statement":
            if self.check_equal(var1, var2):
                var1, var2 = Term(var1), Term(var2)
                modcopy = node.sentence.replace(var1, var2)
                child = MathTree(self, modcopy)
                self.add_child(child)
                return True, "Substitution successful", child
            else:
                return False, "These are not equal"
        return False, "substitution can only be "

    def check_equal(self, var1, var2):
        var1, var2 = Term(var1), Term(var2)
        if (var1, var2) in self.equal or (var2, var1) in self.equal:
            return True
        return False


    # Dual Statements Rule 2.4


    def dual_statement(self, statementstr):
        # add dual statements to a leaf
        statement = Statement(statementstr)
        dual = statement.get_dual()
        if statement.check_admissible(self) and dual.check_admissible(self):
            childa = MathTree(self, statement)
            childb = MathTree(self, dual)
            self.add_child(childa)
            self.add_child(childb)
            return True, "added dual statement", childa, childb
        return False, "dual statement not admissible"

    def contradiction(self, anc1, anc2):
        # if two contradictory statements are found, go back to the last dual split, and add the right statement as
        # middle child
        if anc1.sentence == anc2.sentence.get_dual():
            cur, lastcur = self, self
            while len(cur.children) != 2:
                if cur.has_parent():
                    lastcur = cur
                    cur = cur.parent
                else:
                    return False, "False Tree, mistakes were made"
            child = MathTree(self, lastcur.sentence.get_dual())
            cur.add_child(child, "middle")
            return True, "Contradiction successful"
        return False, "statements not dual"

    def twin_agreement(self, anc1):
        if anc1.sentence == self.sentence:
            cur = self
            while len(cur.children) != 2:
                if cur.has_parent():
                    cur = cur.parent
            if anc1.is_ancestor(cur):
                child = MathTree(self, self.sentence)
                cur.add_child(child, "middle")
                return True, " successful"
            else:
                return False, "These nodes are not twins"
        return False, "statements nto dual"


    # Definition Rule 3.3


    def definition(self, ancestor, var_Str):
        if len(ancestor.sentence.presumptions) > 0:
            hypothesis = ancestor.sentence.presumptions[0][1]
            hyp_quantifier = ancestor.sentence.presumptions[0][0]
            conclusion = ancestor.sentence.copy()
            conclusion.presumptions = conclusion.presumptions[1:]
            if hyp_quantifier == "existential":
                if hypothesis.check_admissible(self):
                    child = MathTree(self, hypothesis)
                    subchild = MathTree(self, conclusion)
                    self.add_child(child)
                    child.add_child(subchild)
                else:
                    var = Term(var_Str)
                    if var not in self.let_active:
                        var_indefinite = Term(repr(hypothesis.get_first_indefinite(self)))
                        child_statement = hypothesis.replace(var_indefinite, var).copy()
                        subchild_statement = conclusion.replace(var_indefinite, var).copy()
                        child = MathTree(self, child_statement)
                        subchild = MathTree(self, subchild_statement)
                        self.add_child(child)
                        child.add_child(subchild)
                    else:
                        return False, "the entered variable is not inactive"
            else:
                return False, "ancestor is not existential"
        else:
            return False, "ancestor is not quantified"
        return True, "successful definition", child, subchild


    # Deduction Rule 3.4


    def Deduction(self, ancestor, hypothesis_ancestor):
        if hypothesis_ancestor.sentence.presumptions > ancestor.sentence.presumptions:
            temp = hypothesis_ancestor
            hypothesis_ancestor = ancestor
            ancestor = temp
        if len(ancestor.sentence.presumptions) > 0:
            hypothesis = ancestor.sentence.presumptions[0][1]
            hyp_quantifier = ancestor.sentence.presumptions[0][0]
            conclusion = ancestor.sentence.copy()
            conclusion.presumptions = conclusion.presumptions[1:]
            if hyp_quantifier == "universal":
                if hypothesis.check_admissible(self):
                    if hypothesis == hypothesis_ancestor.sentence:
                        child = MathTree(self, Statement(hypothesis))
                        subchild = MathTree(self, Statement(conclusion))
                        self.add_child(child)
                        child.add_child(subchild)
                    else:
                        return False, "The hypothesis is not the statement of the third ancestor"
                else:
                    hypanc = hypothesis_ancestor.sentence
                    hyp_lets, hypanc_lets = hypothesis.get_letters(), hypanc.get_letters()
                    if len(hyp_lets) == len(hypanc_lets):
                        index = 0
                        if hypanc == hypothesis:
                            return False, "Third ancestor is not modified copy of hypothesis"
                        while hyp_lets[index] == hypanc_lets[index]:
                            index += 1
                        mod_hypothesis = hypothesis.replace(hyp_lets[index], hypanc_lets[index])
                        if mod_hypothesis == hypanc:
                            child_statement = hypothesis.replace(hyp_lets[index], hypanc_lets[index]).copy()
                            subchild_statement = conclusion.replace(hyp_lets[index], hypanc_lets[index]).copy()
                            if child_statement.check_admissible(self) and subchild_statement.check_admissible(self):
                                subchild = MathTree(self, subchild_statement)
                                self.add_child(subchild)
                            else:
                                return False, "Either the modified hypothesis or modified conclusion are not admissible"
                        else:
                            return False, "hypothesis can not be modified to equal third ancestor"
                    else:
                        return False, "hypothesis can not be modified to equal third ancestor"
            else:
                return False, "ancestor is not universal"
        else:
            return False, "ancestor is not quantified"
        return True, "successful definition", subchild


    # Property addition Rule 4.7


    def property_addition(self, prop_str):
        if ParseStr.check_valid_prop_string(prop_str):
            property = Property(prop_str)
            if property.check_admissible(self):
                if property.contraction.acronym.char in self.let_adjective:
                    if self.abbreviations[property.contraction.acronym].check_modified_copy(property):
                        child = MathTree(self, property)
                        self.add_child(child)
                        return True, "Property Addition successful", child
                    return False, "Property is not proper modified copy"
                child = MathTree(self, property)
                self.add_child(child)
                return True, "Property Addition successful", child
            return False, "The Property was not admissible"
        return False, "Not a valid property string"


    # Apply Property Rule 4.9


    def apply_property(self, property, statement):
        if property.__class__.__name__ == "Property" and statement.__class__.__name__ == "Statement":
            pass
        elif property.__class__.__name__ == "Statement" and statement.__class__.__name__ == "Property":
            temp = property
            property = statement
            statement = temp
        else:
            return False, "One sentence must be a property, while the other is a statement"
        if property.sentence.contraction.acronym == statement.sentence.acronym:
            if len(property.sentence.contraction.parameters) == len(statement.sentence.parameters):
                copy_statement = property.sentence.expansion.copy()
                for index in range(len(property.sentence.contraction.parameters)):
                    copy_statement = copy_statement.replace(property.sentence.contraction.parameters[index],
                                                            statement.sentence.parameters[index])
                    child = MathTree(self, copy_statement)
                    self.add_child(child)
                    return True, "Property application successful", child
            return False, "Something went wrong, different number of parameters"
        return False, "Property must define the acronym of statement"


    # Choice 1 Rule 5.2


    def choice(self, node, variables, additions, secondnode=None):
        # variables is a list of first the two indefinite, then the inactive and finally the 5 definite letters
        # additions is a list of 7 boolean values, describing what nodes to add
        if additions[0] or additions[1]:
            if variables[0] not in self.let_active:
                for i in range(1, 6):
                    if variables[i] not in self.let_definite:
                        return False, "A definite letter is not definite"

                inactive = variables[0]
                def1, def2, def3, def4, def5, def6 = \
                    variables[1], variables[2], variables[3], variables[4], variables[5], variables[6]
                children = []

                if len(node.sentence.parameters) < 2:
                    return False, "Non-valid ancestor"
                sentence1 = node.sentence.presumptions[0]
                sentence2 = node.sentence.presumptions[1]
                for index, hypothesis in enumerate([sentence1, sentence2]):
                    if hypothesis[0] != ["universal", "existential"][index]:
                        return False, "Non-Valid first ancestor"
                    if hypothesis[1].presumptions != []:
                        return False, "Non-Valid first ancestor"
                sentence1, sentence2 = sentence1[1], sentence2[1]
                indef1 = repr(sentence1.get_first_indefinite(self))
                indef2 = repr(sentence2.get_first_indefinite(self))
                if indef1 == None or indef2 == None:
                    return False, "Non-Valid first ancestor"

                cur_node = self

                if additions[0]:
                    statement = Statement(str(inactive + "=" + inactive))
                    child = MathTree(cur_node, statement)
                    cur_node.add_child(child)
                    children.append(child)
                    cur_node = child
                # first statement
                if additions[1]:
                    print(indef2)
                    print(node.sentence)
                    copy = node.sentence.replace(Term(indef2), Term(inactive+"("+indef1+")"))
                    copy.presumptions = copy.presumptions[1:]
                    statement = Statement(str("{"+inactive + "(" + indef1 + ")" + "!=" + inactive + "}" + repr(copy)))
                    child = MathTree(cur_node, statement)
                    cur_node.add_child(child)
                    children.append(child)
                    cur_node = child

                if additions[2]:
                    copy = node.sentence.replace(Term(indef2), Term(inactive+"("+indef1+")"))
                    copy.presumptions = copy.presumptions[2:]
                    statement = Statement(str("{"+inactive + "(" + indef1 + ")" + "!=" + inactive + "}" + repr(copy)))
                    child = MathTree(cur_node, statement)
                    cur_node.add_child(child)
                    children.append(child)
                    cur_node = child
                # second statement
                if additions[3]:
                    statement = Statement(str("{"+inactive+"(" + indef1+")" + "!=" + inactive + "}" + repr(sentence1)))
                    child = MathTree(cur_node, statement)
                    cur_node.add_child(child)
                    children.append(child)
                    cur_node = child

                print(sentence1.is_equality())
                if sentence1.is_equality() and sentence1.parameters[0] == sentence1.parameters[1]:

                    # third statement
                    if additions[4]:
                        statement = Statement(str(inactive+"(" + def1+")" + "!=" + inactive))
                        child = MathTree(cur_node, statement)
                        cur_node.add_child(child)
                        children.append(child)
                        cur_node = child

                    # fourth statement
                    if additions[5]:
                        statement = Statement(str("{"+def1+"(" + indef1+")" + "!=" + def1+"}"
                                                  +inactive+"(" + indef1+")" + "!=" + inactive))
                        child = MathTree(cur_node, statement)
                        cur_node.add_child(child)
                        children.append(child)
                        cur_node = child

                    # fifth statement
                    if additions[6]:
                        statement = Statement(str("{"+def3+"(" + indef1+")" + "!=" + def3+"}"
                                                  + "{"+indef1+"(" + indef2+")" + "!=" + indef1+"}"
                                                  + inactive+"(" + indef2+")" + "!=" + inactive))
                        child = MathTree(cur_node, statement)
                        cur_node.add_child(child)
                        children.append(child)
                        cur_node = child

                    # sixth statement
                    if additions[7]:
                        statement = Statement(str("{" + inactive + "(" + indef1 + ")" + "!=" + inactive + "}"
                                                  + inactive + "(" + inactive + "(" + indef1 + ")" + ")"
                                                  + "!=" + inactive + "(" + indef1 + ")"))
                        child = MathTree(cur_node, statement)
                        cur_node.add_child(child)
                        children.append(child)
                        cur_node = child

                    # seventh statement
                    if additions[8]:
                        statement = Statement(str("{"+inactive+"("+indef1+")!="+inactive+"}"+"["+indef1+"("+indef2+")!="
                                                  +indef1+"]"+"{"+def4+"("+indef2+")!="+def4+"}"
                                                  +def5+"("+indef1+"("+indef2+")"+")!="+def5))
                        child = MathTree(cur_node, statement)
                        cur_node.add_child(child)
                        children.append(child)
                        cur_node = child

                    if secondnode:
                        anc_sent = secondnode.sentence
                        if len(anc_sent.presumptions) > 1:
                            pre1 = anc_sent.presumptions[0][1].replace(def1, def3)

                        # eighth statement
                        if additions[9]:
                            statement = Statement(str("{"+sentence1+"}"+inactive+"("+indef1+") != " +inactive))
                            child = MathTree(cur_node, statement)
                            cur_node.add_child(child)
                            children.append(child)
                            cur_node = child

                        # ninth statement
                        if additions[10]:
                            statement = node.sentence.replace(indef2, Term(str(inactive+"("+indef1+")")))
                            child = MathTree(cur_node, statement)
                            cur_node.add_child(child)
                            children.append(child)
                            cur_node = child

                return True, "Choice succesful", children, cur_node

            return False, "The inactive letter is active"
        return False, "one of the first two nodes have to be added first"

    def convert_text(self):
        def childtree(child):
            if len(child.children) == 0:
                return "{[(" + repr(child.sentence) + ")]}"
            else:
                str = "{[( {[(" + repr(child.sentence) + ")]}"
                for subchild in reversed(child.children):
                    str += childtree(subchild)
                str += ")]}"
                return str
        if len(self.children) == 0:
            return str
        return str+childtree(self)

    def tex_compile_tikz(self):
        str = ""
        str += "\\node{"+repr(self.sentence)+"}"
        def childtree(child):
            if len(child.children) == 0:
                return "child { node {" + repr(child.sentence) + "} }"
            else:
                str = "child { node {" + repr(child.sentence) + "}"
                for subchild in reversed(child.children):
                    str += childtree(subchild)
                str += "}"
                return str
        if len(self.children) == 0:
            return str
        return str+childtree(self)

    def tex_compile_forest(self):
        str = ""
        str += "\\begin{forest} squared/.style={rectangle,draw}"

        def childtree(child):
            if len(child.children) == 0:
                return "[" + repr(child.sentence) + ", squared]"
            else:
                str = "[" + repr(child.sentence) + ", squared"
                for subchild in reversed(child.children):
                    str += childtree(subchild)
                str += "]"
                return str

        if len(self.children) == 0:
            return str + "\\end{forest}"
        return str + childtree(self) + "\\end{forest}"

    def tex_compile_qtree(self):
        str = ""
        str += "\\Tree "
        box_width = "3.0"
        def childtree(child):
            if len(child.children) == 0:
                return "[. " + "\\framebox[" + box_width + "\width]{" + repr(child.sentence) + "} " + " ]"
            else:
                str = "[. " + "\\framebox[" + box_width + "\width]{" + repr(child.sentence)+ "} "
                for subchild in reversed(child.children):
                    str += childtree(subchild)
                str += "]"
                return str

        return str + childtree(self)
