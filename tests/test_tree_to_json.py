from unittest import TestCase
from launcher import lex, parse, tree_to_json, FileStream


class TestTreeToJson(TestCase):

    def test_tree_to_json1(self):
        i_stream = FileStream('tests/test1.1.txt', encoding='utf-8')
        t_stream = lex(i_stream)
        built_tree, error_listener = parse(t_stream)
        json_result = tree_to_json(built_tree, error_listener)
        json_result = json_result.replace("\\r", '')

        with open('tests/test1.1_correct_out.txt', 'r') as correct_out:
            correct_output = correct_out.read().replace("\\r\\n", '\\n')
            self.assertEqual(correct_output, json_result)  
            print('[Test 6] - PASSED')  


    def test_tree_to_json2(self):
        i_stream = FileStream('tests/test1.2.txt', encoding='utf-8')
        t_stream = lex(i_stream)
        built_tree, error_listener = parse(t_stream)
        json_result = tree_to_json(built_tree, error_listener)
        json_result = json_result.replace("\\r", '')
        
        with open('tests/test1.2_out.txt', 'w') as f:
            f.write(json_result)

        with open('tests/test1.2_correct_out.txt', 'r') as correct_out:
            correct_output = correct_out.read().replace("\\r", '')
            self.assertEqual(correct_output, json_result.replace("\\r", ''))  
            print('[Test 7] - PASSED')  
                
    
    def run_json_tests(self):
        self.test_tree_to_json1()
        self.test_tree_to_json2()
