import unittest
from main import *

class TestStringMethods(unittest.TestCase):

    #Unit tests
    def test_unexpected_symbols(self):
        with self.assertRaises(ParseError):
            HPCParsing("(a&.b")
            HPCParsing("(a&b)?")

    def test_a_and_b(self):
        self.assertEqual(HPCTokenizer("a&b"), ['a', '&', 'b'])
        self.assertEqual(HPCTokenizer("a|b|c"), ['a', '|', 'b', '|', 'c'])
        self.assertEqual(HPCTokenizer("a&(b|c)"), ['a', '&', '(', 'b', '|', 'c', ')'])
        self.assertEqual(HPCTokenizer("(a&b)|(b&c)"), ['(', 'a', '&', 'b', ')', '|', '(','b', '&', 'c', ')'])



    #Integration testing
    def test_a_and_b(self):
        self.assertEqual(HPCParser("a&b"), ['a', '&', 'b'])
        self.assertEqual(HPCParser("a|b|c"), ['a', '|', 'b', '|', 'c'])
        self.assertEqual(HPCParser("a&(b|c)"), ['a', '&', ['b', '|', 'c']])
        self.assertEqual(HPCParser("(a&b)|(b&c)"), [['a', '&', 'b'], '|', ['b', '&', 'c']])

    def test_nested_brackets(self):
        self.assertEqual(HPCParser("a&(b|c)"), ['a', '&', ['b', '|', 'c']])
        self.assertEqual(HPCParser("(((a)&b))|(b&(c|d))"), [[[['a'], '&', 'b']], '|', ['b', '&', ['c', '|', 'd']]])
        

    def test_leading_bracket(self):
        with self.assertRaises(TypeError):
            HPCParser("(a&b|(b&c)")

    def test_ending_bracket(self):
        with self.assertRaises(ParseError):
            HPCParser("(a&b))|(b&c)")

    def test_neighbouring_logic(self):
        with self.assertRaises(ParseError):
            HPCParser("(a&b)||(b&c)")
            HPCParser("(a&b)|&(b&c)")
            HPCParser("(a&b)&&(b&c)")
            HPCParser("(a&b)&|(b&c)")
            HPCParser("(a&b) & | (b&c)")

        #self.assertEqual(HPCParser("(a&b)||(b&c)"), ("error, two logic operators can't be together", -1))
        #self.assertEqual(HPCParser("(a&b)|&(b&c)"), ("error, two logic operators can't be together", -1))
        #self.assertEqual(HPCParser("(a&b)&&(b&c)"), ("error, two logic operators can't be together", -1))
        #self.assertEqual(HPCParser("(a&b)&|(b&c)"), ("error, two logic operators can't be together", -1))
        #self.assertEqual(HPCParser("(a&b) & | (b&c)"), ("error, two logic operators can't be together", -1))

    def test_starting_logic(self):
        with self.assertRaises(ParseError):
            HPCParser("|(b&c)")
            HPCParser("&(b&c)")
            HPCParser("(&b)")
            HPCParser("&b")

    def test_ending_logic(self):
        with self.assertRaises(TypeError):
            HPCParser("(b&c)|")
            HPCParser("(b&)")
            HPCParser("&(b&c)&")
            HPCParser("b&")

    def test_long_expressions(self):
        self.assertEqual(HPCParser("apple&banana"), ['apple', '&', 'banana'])
        self.assertEqual(HPCParser("apple|banana|cucumber"), ['apple', '|', 'banana', '|', 'cucumber'])
        self.assertEqual(HPCParser("apple&(banana|cucumber)"), ['apple', '&', ['banana', '|', 'cucumber']])
        self.assertEqual(HPCParser("(apple&banana)|(banana&cucumber)"), [['apple', '&', 'banana'], '|', ['banana', '&', 'cucumber']])

    def test_nested_expressions(self):
        self.assertEqual(HPCParser('('*1001 + "a&b" + ')'*1001), ("error", -1))


if __name__ == '__main__':
    unittest.main()