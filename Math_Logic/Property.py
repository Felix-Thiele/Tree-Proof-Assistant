import copy

from Math_Logic import Statement

"""
In this version of the program, an Abbreviation is an acronym followed py parameters. They are represented 
in a way, such that each letter is seperated by a comma.
"""


class Property:
    def __init__(self, Property):
        self.contraction = Statement.Statement(Property[:Property.find(":")])
        self.expansion = Statement.Statement(Property[Property.find(":")+1:])

    def __repr__(self):
        return repr(self.contraction)+" : "+repr(self.expansion)

    # syntax 4.5 (Property)
    def check_admissible(self, node):
        if self.contraction.acronym.char not in node.let_adjective and self.contraction.acronym.char in node.let_active:
            return False
        copy_expansion = self.expansion.copy()
        first_def = node.let_definite[0]
        for letter in self.contraction.parameters:
            if letter in node.let_definite:
                return False
            copy_expansion = copy_expansion.replace(letter, first_def)
        if copy_expansion.check_admissible(node, new_prop=True):
            return True
        return False

    # syntax 4.6 (Modified copy of a property)
    def check_modified_copy(self, other):
        if self.contraction.acronym == other.contraction.acronym:
            if len(self.contraction.parameters) == len(other.contraction.parameters):
                copystatement = self.expansion.copy()
                for index in range(len(self.contraction.parameters)):
                    copystatement = copystatement.replace(self.contraction.parameters[index],
                                                          other.contraction.parameters[index])
                if copystatement == other.expansion:
                    return True
        return False

