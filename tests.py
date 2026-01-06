import unittest
from main import *

class TestStringMethods(unittest.TestCase):

    def test_a_and_b(self):
        self.assertEqual(HPCParser("a&b"), (['a', '&', 'b'], 3))
        self.assertEqual(HPCParser("a|b|c"), (['a', '|', 'b', '|', 'c'], 5))
        self.assertEqual(HPCParser("a&(b|c)"), (['a', '&', ['b', '|', 'c']], 7))
        self.assertEqual(HPCParser("(a&b)|(b&c)"), ([['a', '&', 'b'], '|', ['b', '&', 'c']], 11))

    def test_nested_brackets(self):
        self.assertEqual(HPCParser("a&(b|c)"), (['a', '&', ['b', '|', 'c']], 7))
        self.assertEqual(HPCParser("(((a)&b))|(b&(c|d))"), ([[[['a'], '&', 'b']], '|', ['b', '&', ['c', '|', 'd']]], 19))

    def test_leading_bracket(self):
        self.assertEqual(HPCParser("(a&b|(b&c)"), ("Error, unclosed brackets", -1))

    def test_ending_bracket(self):
        self.assertEqual(HPCParser("(a&b))|(b&c)"), ("Error, unclosed brackets", -1))

    def test_neighbouring_logic(self):
        self.assertEqual(HPCParser("(a&b)||(b&c)"), ("error, two logic operators can't be together", -1))
        self.assertEqual(HPCParser("(a&b)|&(b&c)"), ("error, two logic operators can't be together", -1))
        self.assertEqual(HPCParser("(a&b)&&(b&c)"), ("error, two logic operators can't be together", -1))
        self.assertEqual(HPCParser("(a&b)&|(b&c)"), ("error, two logic operators can't be together", -1))
        self.assertEqual(HPCParser("(a&b) & | (b&c)"), ("error, two logic operators can't be together", -1))

    def test_starting_logic(self):
        self.assertEqual(HPCParser("|(b&c)"), ("error, a logic operators can't be at the start/end", -1))
        self.assertEqual(HPCParser("&(b&c)"), ("error, a logic operators can't be at the start/end", -1))
        self.assertEqual(HPCParser("(&b)"), ("error, a logic operators can't be at the start/end", -1))
        self.assertEqual(HPCParser("&b"), ("error, a logic operators can't be at the start/end", -1))

    def test_ending_logic(self):
        self.assertEqual(HPCParser("(b&c)|"), ("error, a logic operators can't be at the start/end", -1))
        self.assertEqual(HPCParser("(b&)"), ("error, a logic operators can't be at the start/end", -1))
        self.assertEqual(HPCParser("&(b&c)&"), ("error, a logic operators can't be at the start/end", -1))
        self.assertEqual(HPCParser("b&"), ("error, a logic operators can't be at the start/end", -1))

    def test_long_expressions(self):
        self.assertEqual(HPCParser("apple&banana"), (['apple', '&', 'banana'], 12))
        self.assertEqual(HPCParser("apple|banana|cucumber"), (['apple', '|', 'banana', '|', 'cucumber'], 21))
        self.assertEqual(HPCParser("apple&(banana|cucumber)"), (['apple', '&', ['banana', '|', 'cucumber']], 23))
        self.assertEqual(HPCParser("(apple&banana)|(banana&cucumber)"), ([['apple', '&', 'banana'], '|', ['banana', '&', 'cucumber']], 32))

    def test_nested_expressions(self):
        self.assertEqual(HPCParser('('*1001 + "a&b" + ')'*1001), ("error", -1))


if __name__ == '__main__':
    unittest.main()