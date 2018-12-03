from Math_Logic import ParseStr

"""This file contains 3 classes. 
First is Letter, which saves any number of chars
Then there is Acronym, which also saves an acronym. This acronym can be negated
Last there is Term. Terms are functional terms, which are saved in a tree structure.
"""


class Term:

    def __init__(self, termstr):
        # a Term is a function, which in turn can be a function of a function
        self.functions = []
        for func in ParseStr.split_functions(termstr)[:-1]:
            self.functions.append(Term(func))
        self.object = Letter(ParseStr.split_functions(termstr)[-1])

    def __repr__(self):
        return_str = ""
        end_str = ""
        for func in self.functions:
            return_str += repr(func) + "("
            end_str += ")"
        return return_str+repr(self.object)+end_str

    def __eq__(self, other):
        try:
            return self.functions == other.functions and self.object == other.object
        except:
            return repr(self).strip() == str(other).strip()

    def __hash__(self):
        return hash(repr(self))

    def is_functional(self):
        if self.functions == []:
            return False
        return True

    def is_definite(self, node):
        for let in self.get_letters():
            if let not in node.let_definite:
                return False
        return True

    def get_letters(self):
        letters = []
        letters.append(self.object)
        for func in self.functions:
            letters += func.get_letters()
        return letters

    def replace(self, var1, var2):
        if var1.__class__.__name__ == 'Term' and var2.__class__.__name__ == 'Term':
            if var1.is_functional():
                if len(self.functions) > len(var1.functions):
                    pass
                else:
                    if self.functions[-len(var1.functions):] == var1.functions:
                        if self.object == var1.object:
                            self.functions = self.functions[:-len(var1.functions)] + var2.functions
                            self.object = var2.object
                for func in self.functions:
                    func.replace_letters(var1, var2)
            else:
                if self.object == var1.object:
                    self.functions += var2.functions
                    self.object = var2.object
                for func in self.functions:
                    func.replace(var1, var2)
        elif var1.__class__.__name__ == 'Letter' and var2.__class__.__name__ == 'Term':
            if self.object == var1:
                self.object = var2.object
                self.functions.append(var2.functions)
            for func in self.functions:
                func.replace(var1, var2)
        elif var1.__class__.__name__ == 'Term' and var2.__class__.__name__ == 'Letter':
            if var1.is_functional():
                if len(self.functions) > len(var1.functions):
                    pass
                else:
                    if self.functions[-len(var1.functions):] == var1.functions:
                        if self.object == var1.object:
                            self.functions = self.functions[:-len(var1.functions)]
                            self.object = var2.object
                for func in self.functions:
                    func.replace(var1, var2)
            else:
                if self.object == var1.object:
                    self.object = var2
                for func in self.functions:
                    func.replace(var1, var2)
        elif var1.__class__.__name__ == 'Letter' and var2.__class__.__name__ == 'Letter':
            if self.object == var1:
                self.object = var2
            for func in self.functions:
                func.replace(var1, var2)
        return self


class Acronym:
    def __init__(self, char):
        self.char = char.strip()
        if char[0] == "!":
            self.char = self.char[1:]
            self.dual = True
        else:
            self.dual = False

    def __repr__(self):
        if self.dual:
            return "!" + self.char
        return self.char

    def __eq__(self, other):
        return self.char == other.char and self.dual == other.dual

    def __hash__(self):
        return hash(repr(self))

    def is_equality(self):
        if self.char == "=" and not self.dual:
            return True
        return False

    def is_inequality(self):
        if self.char == "=" and self.dual:
            return True
        return False

    def is_relation(self):
        return self.is_equality() or self.is_inequality()

    def negate(self):
        self.dual = not self.dual


class Letter:
    def __init__(self, char):
        self.char = char.strip()

    def __repr__(self):
        return self.char

    def __eq__(self, other):
        try:
            return self.char == other.char
        except:
            return str(self.char).strip() == str(other).strip()

    def __hash__(self):
        return hash(repr(self))

    def get_letters(self):
        return [self]

