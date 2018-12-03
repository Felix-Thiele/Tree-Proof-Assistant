from Math_Logic.Term import Term, Acronym

"""
This file is a collection of string parsing helper methods.
"""

# takes a statement str and splits it into its presumptions and claim, (the quantified parts and the unquantified part)
def split_presumptions(statestr):
    dict = {"[": "existential", "{": "universal"}
    statements, types = [], []
    index, len_statestr = 0, len(statestr)
    while index < len_statestr:
        if statestr[index] in ["[", "{"]:
            close = find_closing_bracket(statestr, index)
            statements.append(statestr[index+1:close])
            types.append(dict[statestr[index]])
            statestr = statestr[close+1:]
            index, len_statestr = -1, len(statestr)
        index += 1
    if statestr != "":
        statements.append(statestr)
        types.append("claim")
    return statements, types

# this method takes a unquantified str and slices it so that is ready to be converted to a statement.
def readstr(str):
    if "!=" in str:
        str = str.replace("!=", ",")
        str = "!=," + str
    elif "=" in str:
        str = str.replace("=", ",")
        str = "=," + str
    abb_letters = str.split(",")
    acronym = Acronym(abb_letters[0])
    parameters = []
    for letter in abb_letters[1:]:
        parameters.append(Term(letter))
    return acronym, parameters




# takes a functional term and splits it into its functions
def split_functions(funcstr):
    functions = []
    index, len_funcstr = 0, len(funcstr)
    cur_func = ""
    while index < len_funcstr:
        if funcstr[index] == "(":
            close = find_closing_bracket(funcstr, index)
            if close == len(funcstr) - 1:
                functions.append(cur_func + funcstr[:index])
                funcstr = funcstr[index + 1:-1]
                cur_func = ""
            else:
                cur_func += funcstr[:close + 1]
                funcstr = funcstr[close + 1:]
            index, len_funcstr = -1, len(funcstr)
        index += 1
    functions.append(funcstr)
    return functions

# takes the index of an opening bracket, and finds the position of closing one
def find_closing_bracket(str, open_index):
    br_open = str[open_index]
    assert br_open in ["[", "(", "{"], "given char is not a bracket"
    dict = {"[": "]", "(": ")", "{": "}"}
    br_close = dict[br_open]
    count = 0
    for index, char in enumerate(str[open_index:]):
        if char == br_open:
            count += 1
        elif char == br_close:
            count -= 1
        if count == 0:
            return index + open_index

# checkes if property string is valid
def check_valid_prop_string(str):
    return True