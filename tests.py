import unittest
from main import *

class TestStringMethods(unittest.TestCase):

    #Tokeniser(unit) tests
    def test_a_and_b_tokenisation(self):
        self.assertEqual(HPCTokenizer("a&b"), ['a', '&', 'b'])

    def test_a_or_b_tokenisation(self):
        self.assertEqual(HPCTokenizer("a|b|c"), ['a', '|', 'b', '|', 'c'])

    def test_longer_tokenisation(self):
        self.assertEqual(HPCTokenizer("a&(b|c)"), ['a', '&', '(', 'b', '|', 'c', ')'])
        self.assertEqual(HPCTokenizer("(a&b)|(b&c)"), ['(', 'a', '&', 'b', ')', '|', '(','b', '&', 'c', ')'])

    def test_word_tokenisation(self):
        self.assertEqual(HPCParser("apple&banana"), ['apple', '&', 'banana'])
        self.assertEqual(HPCParser("apple|banana|cucumber"), ['apple', '|', 'banana', '|', 'cucumber'])

    #Test failure
    def test_unexpected_symbols(self):
        with self.assertRaises(Exception):
            HPCParsing("(a&.b")
            HPCParsing("(a&b)?")
            HPCParsing("a/b")
            HPCParsing("!a&b")


    #Integration testing
    def test_a_and_b_integration(self):
        self.assertEqual(HPCParser("a&b"), ['a', '&', 'b'])

    def test_a_or_b_integration(self):
        self.assertEqual(HPCParser("a|b|c"), ['a', '|', 'b', '|', 'c'])

    def test_brackets_integration(self):
        self.assertEqual(HPCParser("a&(b|c)"), ['a', '&', ['b', '|', 'c']])
        self.assertEqual(HPCParser("(a&b)|(b&c)"), [['a', '&', 'b'], '|', ['b', '&', 'c']])

    def test_nested_brackets_integration(self):
        self.assertEqual(HPCParser("a&(b|c)"), ['a', '&', ['b', '|', 'c']])
        self.assertEqual(HPCParser("(((a)&b))|(b&(c|d))"), [[[['a'], '&', 'b']], '|', ['b', '&', ['c', '|', 'd']]])
        


    def test_leading_bracket(self):
        with self.assertRaises(Exception):
            HPCParser("(a&b|(b&c)")

    def test_ending_bracket(self):
        with self.assertRaises(Exception):
            HPCParser("(a&b))|(b&c)")

    def test_neighbouring_logic(self):
        with self.assertRaises(Exception):
            HPCParser("a||c")
            HPCParser("(a&b)|&(b&c)")
            HPCParser("(a&b)&&(b&c)")
            HPCParser("(a&b)&|(b&c)")
            HPCParser("(a&b) & | (b&c)")

    def test_starting_logic(self):
        with self.assertRaises(Exception):
            HPCParser("|(b&c)")
            HPCParser("&(b&c)")
            HPCParser("(&b)")
            HPCParser("&b")

    def test_ending_logic(self):
        with self.assertRaises(Exception):
            HPCParser("(b&c)|")
            HPCParser("(b&)")
            HPCParser("&(b&c)&")
            HPCParser("b&")

    #Testing expressions that aren't just 1 letter
    def test_word_parsing(self):
        self.assertEqual(HPCParser("apple&banana"), ['apple', '&', 'banana'])
        self.assertEqual(HPCParser("apple|banana|cucumber"), ['apple', '|', 'banana', '|', 'cucumber'])
        self.assertEqual(HPCParser("apple&(banana|cucumber)"), ['apple', '&', ['banana', '|', 'cucumber']])
        self.assertEqual(HPCParser("(apple&banana)|(banana&cucumber)"), [['apple', '&', 'banana'], '|', ['banana', '&', 'cucumber']])



    #Failure states
    #Test recursive depth of the program
    def test_extreme_nesting(self):
        with self.assertRaises(Exception):
            self.assertEqual(HPCParser('('*1001 + "a&b" + ')'*1001), [])

if __name__ == '__main__':
    unittest.main()