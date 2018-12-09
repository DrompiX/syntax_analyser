from antlr4 import FileStream, CommonTokenStream
from src.Python3Lexer import Python3Lexer
from src.Python3Parser import Python3Parser
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.error.ErrorListener import ErrorListener
import json


class FileErrorListener(ErrorListener):
    """Class for storing errors which occured during the syntax analysis"""

    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append("line " + str(line) + ":" + str(column) + " " + msg)


def walk(subtree, rule_names):
    """ Function for converting tree to dictionary
    
    Function takes subtree and array of names and recursively
    goes through each node and returns dictionary 
    (possibly array of dictionaries back)

    Args:
        @subtree - root of subtree to be walked through
        @rule_names - corresponding to states rule names

    Returnes: dict representation of the tree
    """
    if isinstance(subtree, TerminalNodeImpl):
        token = subtree.getSymbol()
        token_name = Python3Parser.symbolicNames[token.type]
        return {'Type': token_name, 'Value': token.text}
    else:
        child_nodes = []
        name = rule_names[subtree.getRuleIndex()]

        for i in range(subtree.getChildCount()):
            child_nodes.append(walk(subtree.getChild(i), rule_names))
        if len(child_nodes) == 1:
            return {name: child_nodes[0]}
        else:
            return {name: child_nodes}


def lex(i_stream):
    """Makes lexical analysis
    
    Returns: stream of tokens
    """
    lexer = Python3Lexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    t_stream.fill()
    return t_stream


def parse(t_stream):
    """Handles parsing
    
    Params:
        t_stream: stream of tokens to parse

    Returns: 
        resulting tree
        error handler (with possible errors stored inside)
    """
    py_parser = Python3Parser(t_stream)
    py_parser.removeErrorListeners()

    error_listener = FileErrorListener()
    py_parser.addErrorListener(error_listener)

    built_tree = py_parser.file_input()

    return built_tree, error_listener


def tree_to_json(built_tree, error_listener):
    """Converts tree to json

    Params:
        built_tree - tree to be converted
        error_listener - error hadling object
    
    Returns:
        json, if tree was constructed without errors
        array of errors, otherwise
        
    """
    if len(error_listener.errors) > 0:
        return '\n'.join(["Syntax errors were found"] + error_listener.errors)
    else:
        result = walk(built_tree, Python3Parser.ruleNames)
        return json.dumps(result, indent=2, ensure_ascii=False)


def launch():
    i_stream = FileStream('in.txt', encoding='utf-8')
    t_stream = lex(i_stream)
    built_tree, error_listener = parse(t_stream)

    result = tree_to_json(built_tree, error_listener)
    with open('out.txt', 'w') as f_out:
        f_out.write(result)


if __name__ == '__main__':
    from tests.run_tests import run_tests
    run_tests()
    launch()
