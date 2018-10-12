from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from src.Python3Listener import Python3Listener
from src.Python3Lexer import Python3Lexer
from src.Python3Parser import Python3Parser
from antlr4.tree.Trees import Trees
from antlr4.tree import Tree
from antlr4.Token import Token
from antlr4.Utils import escapeWhitespace
from antlr4.tree.Tree import RuleNode, ErrorNode, TerminalNode, Tree, ParseTree, TerminalNodeImpl
from io import StringIO
import json

# class Python3GrammarListener(Python3Listener):
#     def enterSmall_stmt(self, ctx):
#         print(ctx.child(0))

# def handleExpression(expr):
# #     adding = True
# #     value = 0
#     for child in expr.getChildren():
#         print(child)


def getNodeText(t:Tree, ruleNames:list=None, recog=None):
    if recog is not None:
        ruleNames = recog.ruleNames
    if ruleNames is not None:
        if isinstance(t, RuleNode):
            if t.getAltNumber()!=0: # should use ATN.INVALID_ALT_NUMBER but won't compile
                return ruleNames[t.getRuleIndex()]+":"+str(t.getAltNumber())
            return ruleNames[t.getRuleIndex()]
        elif isinstance( t, ErrorNode):
            return str(t)
        elif isinstance(t, TerminalNode):
            if t.symbol is not None:
                return t.symbol.text
    # no recog for rule names
    payload = t.getPayload()
    if isinstance(payload, Token ):
        return payload.text
    return str(t.getPayload())


def toStringTree(t:Tree, ruleNames:list=None, recog=None):
        if recog is not None:
            ruleNames = recog.ruleNames
        s = escapeWhitespace(getNodeText(t, ruleNames), False)
        if t.getChildCount()==0:
            return s
        with StringIO() as buf:
            buf.write("(")
            buf.write(s)
            buf.write(' ')
            for i in range(0, t.getChildCount()):
                if i > 0:
                    buf.write(' ')
                buf.write(toStringTree(t.getChild(i), ruleNames))
            buf.write(")")
            return buf.getvalue()


# def traverse(subtree, data, ruleNames):
#     if isinstance(subtree, TerminalNodeImpl):
#         token = subtree.getSymbol()
#         data['Type'] = token.type
#         data['Value'] = token.text
#     else:
#         child_nodes = {}#[]
#         name = ruleNames[subtree.getRuleIndex()] # getNodeText(subtree, ruleNames=ruleNames, recog=None)
#         data[name] = child_nodes

#         for i in range(subtree.getChildCount()):
#             # inside = {}
#             # child_nodes.append(inside)
#             traverse(subtree.getChild(i), child_nodes, ruleNames)#inside, ruleNames)
def walk(subtree, ruleNames):
    if isinstance(subtree, TerminalNodeImpl):
        token = subtree.getSymbol()
        return {'Type': token.type, 'Value': token.text}
    elif isinstance(subtree, ErrorNode):
        # return str(subtree)
        print('I was here')
        return None
    else:
        child_nodes = []
        name = ruleNames[subtree.getRuleIndex()]

        for i in range(subtree.getChildCount()):
            child_nodes.append(walk(subtree.getChild(i), ruleNames))
        if len(child_nodes) == 1:
            return {name: child_nodes[0]}
        else:
            return {name: child_nodes}


def main(): 
    i_stream = FileStream('in.txt')

    lexer = Python3Lexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    t_stream.fill()
#     print("TOKENS")
#     for token in t_stream.tokens:
#         if token.text != '<EOF>':
#             type_name = Python3Parser.symbolicNames[token.type]
#             tabs = 5 - len(type_name) // 4
#             sep = "\t" * tabs
#             print("    %s%s%s" % (type_name, sep,
#                                   token.text.replace(" ", u'\u23B5').replace("\n", u'\u2936')))
    py_parser = Python3Parser(t_stream)
    built_tree = py_parser.file_input()

    # print(toStringTree(built_tree, None, py_parser))
    
    result = walk(built_tree, Python3Parser.ruleNames)
    with open('out.txt', 'w') as out:
        out.write(json.dumps(result, indent=2, ensure_ascii=False))



#     print(*tree.getChildren())
#     print(tree.getChild(0).invokingState)
#     print(Python3Parser.ruleNames[tree.getChild(0).invokingState])
#     while tree.getChild(0):
#         tree = tree.getChild(0)
#     print(tree.getText())
#     print(*tree.parentCtx.getChildren())
#     listener = Python3Listener()
#     walker = ParseTreeWalker()
#     printer = Python3GrammarListener()
#     walker.walk(printer, tree)
# print(Trees.toStringTree(built_tree, None, py_parser)) GOOD
    
#     handleExpression(tree)
#     print(len(Python3Parser.literalNames) + len(Python3Parser.symbolicNames) + len(Python3Parser.ruleNames))
#     print(tree.toString(ruleNames=Python3Parser.ruleNames, stop=None))

    # print(toStringTree(built_tree, Python3Parser.ruleNames, None))


    # print(tree.toStringTree(ruleNames=Python3Parser.ruleNames))


    # result = {} # GOOD
    # traverse(built_tree, result, Python3Parser.ruleNames)
    # result = {}

if __name__ == '__main__':
   main()