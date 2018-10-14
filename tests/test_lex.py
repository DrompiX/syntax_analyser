from unittest import TestCase
from launcher import lex, FileStream
from src.Python3Lexer import InputStream


class TestLex(TestCase):

    def test_lex1(self):
        in_code = "import sys"
        i_stream = InputStream(in_code)
        t_stream = lex(i_stream)
        tokens = [t.text for t in t_stream.tokens]
        true_tokens = ['import', 'sys', '<EOF>']
        self.assertEqual(true_tokens, tokens)
        print('[Test 1] - PASSED')
    

    def test_lex2(self):
        in_code = "print(a)"
        i_stream = InputStream(in_code)
        t_stream = lex(i_stream)
        tokens = [t.text for t in t_stream.tokens]
        true_tokens = ['print', '(', 'a', ')', '<EOF>']
        self.assertEqual(true_tokens, tokens)
        print('[Test 2] - PASSED')
    

    def test_lex3(self):
        in_code = "@app.route()"
        i_stream = InputStream(in_code)
        t_stream = lex(i_stream)
        tokens = [t.text for t in t_stream.tokens]
        true_tokens = ['@', 'app', '.', 'route', '(', ')', '<EOF>']
        self.assertEqual(true_tokens, tokens)
        print('[Test 3] - PASSED')

    
    def test_lex4(self):
        in_code = "import re\nre.match(a, var_a)"
        i_stream = InputStream(in_code)
        t_stream = lex(i_stream)
        tokens = [t.text for t in t_stream.tokens]
        true_tokens = ['import', 're', '\n', 're', '.', 'match',
                       '(', 'a', ',', 'var_a', ')', '<EOF>']
        self.assertEqual(true_tokens, tokens)
        print('[Test 4] - PASSED')

    
    def test_lex5(self):
        in_code = "if x > 1:\nprint('hey')\nelse:\nprint('hello')"
        i_stream = InputStream(in_code)
        t_stream = lex(i_stream)
        tokens = [t.text for t in t_stream.tokens]
        true_tokens = ['if', 'x', '>', '1', ':', '\n', 'print', 
                       '(', "'hey'", ')', '\n', 'else', ':', 
                       '\n', 'print', '(', "'hello'", ')', '<EOF>']
        self.assertEqual(true_tokens, tokens)
        print('[Test 5] - PASSED')

    def run_lex_tests(self):
        self.test_lex1()
        self.test_lex2()
        self.test_lex3()
        self.test_lex4()
        self.test_lex5()
