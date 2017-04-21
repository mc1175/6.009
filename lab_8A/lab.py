"""6.009 Lab 8A: carlae Interpreter"""

import sys


class EvaluationError(Exception):
    """Exception to be raised if there is an error during evaluation."""
    pass


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
    """
    word_list = []
    current_word = ''
    append = True
    for character in source:
        # deals with comments
        if character == ';':
            append = False
        elif character == '\n':
            append = True


        if append: # append if string is not a comment

            if character == '(' or character == ')': # end current word, append word then append paren
                if len(current_word) != 0:
                    word_list.append(current_word)
                    current_word = ''
                word_list.append(character)

            elif character == ' ' or character == '\n': # end of current word or line
                if len(current_word) != 0:
                    word_list.append(current_word)
                    current_word = ''
            else:
                current_word += character

    if len(current_word) != 0: # append last word
        word_list.append(current_word)

    return word_list


##############################################################################################
def convert_to_number(token):
    try:
        if '.' in token:
            return float(token)
        else:
            return int(token)
    except:
        return token

def check_balanced_parens(tokens):
    l_parens = 0
    r_parens = 0
    for token in tokens:
        if l_parens < r_parens:
            raise SyntaxError
        if token == '(':
            l_parens += 1
        elif token == ')':
            r_parens += 1

    if l_parens - r_parens != 0:
        raise SyntaxError
    else:
        return None

def parse_recurse(tokens):
    if len(tokens) == 1:
        return (convert_to_number(tokens[0]),1)

    token_list = []
    list_length = 0
    i = 1 # skip left paren

    while i<len(tokens):
        if tokens[i] == ')':  # return sublist and number of elements in sublist (including l and r parens)
            return token_list, list_length + 2  # +2 for left and right parentheses
        elif tokens[i] == '(':
            x,length = parse_recurse(tokens[i:]) # look forward starting at i
            token_list.append(x)
            list_length += length # recursively add length of sublist
            i += length # advance by number of elements in sublist
        else:
            token_list.append(convert_to_number(tokens[i]))
            i += 1
            list_length += 1
    return token_list, list_length

##############################################################################################

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    check_balanced_parens(tokens)

    return parse_recurse(tokens)[0]



def multiply(list):
    x = 1
    for elt in list:
        x *= elt
    return x

def divide(list):
    numerator = list[0]
    denominator = multiply(list[1:])
    return numerator/denominator

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': multiply,
    '/': divide,
}


def evaluate(tree):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if type(tree) == int or type(tree) == float:
        return tree
    elif tree[0] in carlae_builtins:
        return carlae_builtins[tree[0]]( evaluate(arg) for arg in tree[1:] )
    else:
        raise EvaluationError

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)
    user_input = input('>>>')
    while user_input.lower() != 'quit':
        try:
            tokens = tokenize(user_input)
            try:
                x = parse(tokens)
                try:
                    print(evaluate(x))
                except:
                    print('EvaluationError')
            except:
                print('ParseError')
        except:
            print("TokenizeError")
        user_input = input('>>>')

