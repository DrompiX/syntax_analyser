import tests.test_lex as test_lex
import tests.test_tree_to_json as test_tree_to_json

def run_tests():
    lex_tester = test_lex.TestLex()
    lex_tester.run_lex_tests()

    json_tester = test_tree_to_json.TestTreeToJson()
    json_tester.run_json_tests()