import unittest
from tokenizer_gen import Token, Tokenizer


class MyTestCase(unittest.TestCase):
    def test_singletoken(self):
        """ String with one token """
        t = Tokenizer()
        res = list(t.i_tokenize("мама"))
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], Token)
        self.assertEqual(res[0].tok, "мама")
        self.assertEqual(res[0].f_ch, 0)
        self.assertEqual(res[0].l_ch, 3)
        self.assertEqual(res[0].typ, "alph")

    def test_lastalph(self):
        """ String that ends with alphabetical symbol """
        t = Tokenizer()
        res = list(t.i_tokenize("то есть"))
        self.assertEqual(len(res), 3)
        self.assertIsInstance(res[0], Token)
        self.assertIsInstance(res[1], Token)
        self.assertIsInstance(res[2], Token)
        self.assertEqual(res[0].tok, "то")
        self.assertEqual(res[1].tok, " ")
        self.assertEqual(res[2].tok, "есть")
        self.assertEqual(res[0].f_ch, 0)
        self.assertEqual(res[1].f_ch, 2)
        self.assertEqual(res[2].f_ch, 3)
        self.assertEqual(res[0].l_ch, 1)
        self.assertEqual(res[1].l_ch, 2)
        self.assertEqual(res[2].l_ch, 6)
        self.assertEqual(res[0].typ, "alph")
        self.assertEqual(res[1].typ, "space")
        self.assertEqual(res[2].typ, "alph")

    def test_lastnotalph(self):
        """ String that ends with non-alphabetical symbol """
        t = Tokenizer()
        res = list(t.i_tokenize("то есть "))
        self.assertEqual(len(res), 4)
        self.assertIsInstance(res[0], Token)
        self.assertIsInstance(res[1], Token)
        self.assertEqual(res[0].tok, "то")
        self.assertEqual(res[2].tok, "есть")
        self.assertEqual(res[0].f_ch, 0)
        self.assertEqual(res[1].f_ch, 2)
        self.assertEqual(res[2].f_ch, 3)
        self.assertEqual(res[3].f_ch, 7)
        self.assertEqual(res[0].l_ch, 1)
        self.assertEqual(res[1].l_ch, 2)
        self.assertEqual(res[2].l_ch, 6)
        self.assertEqual(res[3].f_ch, 7)
        self.assertEqual(res[0].typ, "alph")
        self.assertEqual(res[1].typ, "space")
        self.assertEqual(res[2].typ, "alph")
        self.assertEqual(res[3].typ, "space")


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
        self.assertEqual(len(res), 5)
        self.assertIsInstance(res[0], Token)
        self.assertIsInstance(res[1], Token)
        self.assertIsInstance(res[2], Token)
        self.assertIsInstance(res[3], Token)
        self.assertIsInstance(res[4], Token)
        self.assertEqual(res[0].tok, "token")
        self.assertEqual(res[1].tok, "123")
        self.assertEqual(res[2].tok, "toj")
        self.assertEqual(res[3].tok, ",")
        self.assertEqual(res[4].tok, " ")
        self.assertEqual(res[0].f_ch, 0)
        self.assertEqual(res[1].f_ch, 5)
        self.assertEqual(res[2].f_ch, 8)
        self.assertEqual(res[3].f_ch, 11)
        self.assertEqual(res[4].f_ch, 12)
        self.assertEqual(res[0].l_ch, 4)
        self.assertEqual(res[1].l_ch, 7)
        self.assertEqual(res[2].l_ch, 10)
        self.assertEqual(res[3].l_ch, 11)
        self.assertEqual(res[4].l_ch, 12)
        self.assertEqual(res[0].typ, "alph")
        self.assertEqual(res[1].typ, "digit")
        self.assertEqual(res[2].typ, "alph")
        self.assertEqual(res[3].typ, "punct")
        self.assertEqual(res[4].typ, "space")

    def test_symbol(self):
        t = Tokenizer()
        res = list(t.alph_tokenize('b'))
        gold = [Token('b', 0, 0, "alph")]
        self.assertEqual(res, gold)


if __name__ == '__main__':
    unittest.main()
