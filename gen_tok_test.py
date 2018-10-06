"""Unittest for tokenizer_gen module"""
import unittest
from tokenizer_gen import Token, Tokenizer

class MyTestCase(unittest.TestCase):
    def test_singletoken(self):
        """ String with one token """
        t = Tokenizer()
        res = list(t.i_tokenize("мама"))
        gold = [Token("мама", 0, 3, "alph")]
        self.assertEqual(res, gold)

    def test_lastalph(self):
        """ String that ends with alphabetical symbol """
        t = Tokenizer()
        res = list(t.i_tokenize("то есть"))
        gold = [Token("то", 0, 1, "alph"), Token(" ", 2, 2, "space"),
                Token("есть", 3, 6, "alph")]
        self.assertEqual(res, gold)

    def test_lastnotalph(self):
        """ String that ends with non-alphabetical symbol """
        t = Tokenizer()
        res = list(t.i_tokenize("то есть "))
        gold = [Token("то", 0, 1, "alph"), Token(" " , 2, 2, "space"),
                Token("есть", 3, 6, "alph"), Token(" ", 7, 7, "space")]
        self.assertEqual(res, gold)

    def test_empty(self):
        """ Empty string """
        t = Tokenizer()
        res = list(t.i_tokenize(""))
        self.assertEqual(len(res), 0)

    def test_ex(self):
        """ Not a string object """
        t = Tokenizer()
        with self.assertRaises(TypeError):
            list(t.i_tokenize(["j"]))

    def test_num(self):
        """ Non-alphabetical tokens """
        t = Tokenizer()
        res = list(t.i_tokenize("token123toj, "))
        gold = [Token("token", 0, 4, "alph"), Token("123", 5, 7, "digit"),
                Token("toj", 8, 10, "alph"), Token(",", 11, 11, "punct"),
                Token(" ", 12, 12, "space")]
        self.assertEqual(res, gold)

    def test_symbol(self):
        t = Tokenizer()
        res = list(t.alph_tokenize('b'))
        gold = [Token('b', 0, 0, "alph")]
        self.assertEqual(res, gold)


if __name__ == '__main__':
    unittest.main()
