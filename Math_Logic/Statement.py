import copy
from Math_Logic import ParseStr


"""
In the original Paper the concept of statements is introduced with equality or inequality relations between objects.
Later the concept of abbreviations are introduced. Here we look at everything as an abbreviations. Each abbreviation
consists of an acronym followed by parameters everything seperated by commas.Internally we treat a=b as =,a,b.
All acronyms are saved in a project individual sql database, more of which can be merged to use content from other
proofs.

Each statement also saves a list of its presumptions, which are the quantified statements. A presumption is a set of the
quantifer type and the statement.
"""


class Statement:
    def __init__(self, statestr):
        statestr = statestr.replace(" ", "")
        self.acronym = None
        self.parameters = []
        self.presumptions = []

        # the statementstr is split into its quantified presumptions and the claim
        substatements, functions = ParseStr.split_presumptions(statestr)
        for statement, function in zip(substatements[:-1], functions[:-1]):
            self.presumptions.append((function, Statement(statement)))
        # readstr returns the acronym as an acronym object, and all the parameters as term objects
        # of a unquantified str
        self.acronym = ParseStr.readstr(substatements[-1])[0]
        self.parameters = ParseStr.readstr(substatements[-1])[1]

    def __eq__(self, other):
        if other.__class__.__name__ != "Statement":
            return False
        if self.acronym == other.acronym:
            if self.parameters == other.parameters:
                return True
        return False

    def __repr__(self):
        presumptions = ""
        for pre in self.presumptions:
            open, close = "[", "] "
            if pre[0] == "universal":
                open, close = "{", "} "
            presumptions += open + repr(pre[1]) + close
        if self.acronym.is_equality():
            return presumptions + repr(self.parameters[0]) + " = " + repr(self.parameters[1])
        elif self.acronym.is_inequality():
            return presumptions + repr(self.parameters[0]) + " != " + repr(self.parameters[1])
        else:
            str = repr(self.acronym)
            for param in self.parameters:
                str += ", " + repr(param)
            return presumptions + str

    def get_dual(self):
        # returns the dual statement of self
        dual = self.copy()
        dual.presumptions = [("universal", s) if a == "existential" else ("existential", s) for (a, s) in dual.presumptions]
        dual.acronym.negate()
        return dual

    def get_letters(self):
        letters = []
        for param in self.parameters:
            letters += param.get_letters()
        for pres in self.presumptions:
            letters += pres[1].get_letters()
        return letters

    def get_first_indefinite(self, node):
        for let in self.get_letters():
            if let not in node.let_definite:
                return let
        return None

    def is_equality(self):
        if len(self.parameters) == 2:
            if self.acronym.is_equality():
                return True
        return False

    def replace(self, var1, var2):
        mod_copy = self.copy()
        for index in range(len(mod_copy.parameters)):
            mod_copy.parameters[index] = mod_copy.parameters[index].replace(var1, var2)
        mod_presumptions = []
        for pre in mod_copy.presumptions:
            mod_presumptions.append((pre[0], pre[1].replace(var1, var2)))
        mod_copy.presumptions = mod_presumptions
        return mod_copy

    def check_admissible(self, node, new_prop=False):
        if self.presumptions == []:
            return self.check_admissible_unquantified(node, new_prop)
        else:
            return self.check_admissible_quantified(node)

    def check_admissible_unquantified(self, node, new_prop=False):
        if not new_prop:
            if self.acronym.char not in node.let_adjective:
                if self.acronym.char != "=":
                    return False
        for let in self.get_letters():
            if let not in node.let_definite:
                return False
        return True

    def check_admissible_quantified(self, node, new_prop=False):
        hypothesis = self.presumptions[0][1]
        conclusion = self.copy()
        conclusion.presumptions = conclusion.presumptions[1:]
        if hypothesis.check_admissible(node, new_prop) and conclusion.check_admissible(node, new_prop):
            return True
        else:
            if not hypothesis.presumptions:
                indef = []
                for let in hypothesis.get_letters():
                    if let not in node.let_definite and let not in indef:
                        indef.append(let)
                if len(indef) == 1:
                    conc = conclusion.replace(indef[0], node.let_definite[0])
                    return conc.check_admissible(node, new_prop)
            return False

    def copy(self):
        return copy.deepcopy(self)




